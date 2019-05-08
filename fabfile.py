"""
SDK de Extensões do Colibri.
Modo de uso:
 > fab comando[:parametro1,parametro2,parametro3]
Solicite ajuda de um comando para maiores detalhes:
 > fab ajuda:comando
"""
import importlib
import os
import sys
import shutil
import glob
import fnmatch
import compileall
import zipfile
import json
import unicodedata
import locale
from types import ModuleType

import requests
import codecs
import string
import warnings
try:
    from ConfigParser import RawConfigParser
except ImportError:
    from configparser import RawConfigParser
from collections import namedtuple
from fabric.api import task, local, puts, prefix, hide
from fabric.context_managers import _setenv, settings
from fabric import state
from fabric.main import show_commands, display_command
from subprocess import call
import subprocess
from registry import get_value, KEY_READ


VERSAO_SDK = '1.0'
PY3 = sys.version_info > (3,)
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
_abs = lambda *x: os.path.join(BASE_PATH, *x)

sys.path.insert(0, BASE_PATH)

deve_gerar_config = False
try:
    from config_empacotar import CAMINHO_EXT_DEV, \
        SIGLA_EMPRESA, NOME_EMPRESA
except Exception as e:
    CAMINHO_EXT_DEV = _abs('examples')
    SIGLA_EMPRESA = None
    NOME_EMPRESA = None
    deve_gerar_config = True

Dependency = namedtuple('Dependency', 'name link predicate post')

ENV_NAME = 'colibri'
WORKON = r'workon {}'.format(ENV_NAME)
WORKON_HOME = os.environ.get('WORKON_HOME')
if not WORKON_HOME:
    puts('Por favor crie a variável de ambiente WORKON_HOME conforme documentação')
    exit(1)
WORKON_HOME = os.path.join(WORKON_HOME, ENV_NAME)
with hide('output','running','warnings'):
    PYTHON36 = local(
        'py -3.6 -c "import sys; import os; print(os.path.dirname(sys.executable))"',
        capture=True
    )
TCL_PATH = os.path.join(PYTHON36, 'tcl')
INNO_SETUP_DOWNLOAD = r'https://s3.amazonaws.com/ncr-colibri/install/innosetup-unicode.exe'
INNO_REG_PATH = u'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Inno Setup 5_is1'
INNO_REG_KEY = u'InstallLocation'
COLIBRI_REG_PATH = u'HKEY_LOCAL_MACHINE\\Software\\NCR\\Colibri'
COLIBRI_REG_KEY = u'NCRColibri'
DEP_CACHE_DIR = '_cache'
DEP_DEST_DIR = r'{}\Lib\site-packages'.format(WORKON_HOME)
CHUNK_SIZE = 1024
try:
    CAMINHO_INNO = get_value(INNO_REG_PATH, INNO_REG_KEY, KEY_READ)
except:
    CAMINHO_INNO = None


class FakeColibriModule(ModuleType):
    def __init__(self):
        super().__init__('colibri')

    @staticmethod
    def callback(um_plugin, um_evento, um_contexto):
        pass

    @staticmethod
    def assinar_evento(um_plugin, um_evento):
        pass

    @staticmethod
    def obter_configs(um_plugin, uma_maquina):
        return '{"configs":{}}'

    @staticmethod
    def gravar_config(um_plugin, uma_config, maquina_id, um_valor):
        pass

    @staticmethod
    def mostrar_teclado(um_plugin, dados):
        return '{"retorno":false, "resposta":''}'

    @staticmethod
    def mostrar_mensagem(um_plugin, dados):
        pass


class SemLicencaException(Exception):
    pass


# A função original em fabric.context_managers  não suporta espaços no nome
def lcd(path):
    which = 'lcwd'
    if state.env.get(which) and not path.startswith('/') \
            and not path.startswith('~'):
        new_cwd = state.env.get(which) + '/' + path
    else:
        new_cwd = path
    return _setenv({which: new_cwd})


def obter_caminho_extensao(pasta=''):
    caminho = os.path.normpath(os.path.join(CAMINHO_EXT_DEV, pasta))
    return caminho

putsc = lambda x: puts("{:*^80}".format(x))


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    if PY3:
        return only_ascii.decode('ascii')
    return only_ascii


def input(strmsg):
    if PY3:
        import builtins
        return builtins.input(strmsg)
    return raw_input(remove_accents(strmsg)).decode(
        sys.stdin.encoding or locale.getpreferredencoding(True)
    )


def should_install_pywin32():
    """
    Predicate function that must return True if the package win32 is required.
    """
    with prefix(WORKON):
        res = local(
            'python -c "exec(\'try: import win32com'
            '\\nexcept: print(1)\')"',
            capture=True
        )
    # res will have value 1 if python could not import win32com
    return bool(res.strip())


def post_install_pywin32():
    post_script_dir = _abs('SCRIPTS')
    if not os.path.exists(post_script_dir):
        return
    post_script = _abs(r'SCRIPTS\pywin32_postinstall.py')
    puts("Aviso: **** Se o comando a seguir falhar, execute-o como administrador")
    with prefix(WORKON):
        local('python "{}" -install'.format(post_script))
    shutil.rmtree(post_script_dir)


DEP_INSTALLERS = (
    Dependency(
        name='pywin32-221.win32-py3.6.exe',
        link='http://iweb.dl.sourceforge.net/project/pywin32/pywin32/'
             'Build%20221/pywin32-221.win32-py3.6.exe',
        predicate=should_install_pywin32,
        post=post_install_pywin32
    ),
)


@task
def iniciar_ambiente():
    """
    Monta ambiente de Python do Colibri.

    Será criado o ambiente virtual colibri para uso do SDK e dos plugins em Python.
    """
    putsc(" iniciando ambiente com dependencias ")
    _iniciar_virtualenv()
    local('pip install requests')

    with prefix(WORKON):
        local(r'python -m pip install pip --upgrade')
        _download()
        _instalar_dependencias()
        local(r'pip install -r {}'.format(_abs('requirements_dev.txt')))

        link_tkinter()

@task
def configurar_empresa(caminho=None, empresa=None, sigla=None):
    """
    Configura os dados da empresa.

    Os dados da empresa são solicitados de forma interativa e são essenciais para a criação das extensões.
    """
    putsc('Configuração inicial do ambiente de desenvolvedor')
    global CAMINHO_EXT_DEV, SIGLA_EMPRESA, NOME_EMPRESA

    cam = caminho or input(
        u'Entre o caminho completo da pasta dos seus projetos\nEste é o diretório onde deverão ficar todos seus projetos de extensões\n'
        u'(Default: {})\n>'.format(
            CAMINHO_EXT_DEV))
    cam = os.path.abspath(cam)
    if cam and not os.path.exists(cam):
        print(f'Pasta não existe: {cam}')
        exit(0)
    CAMINHO_EXT_DEV = cam or CAMINHO_EXT_DEV

    if not empresa:
        while True:
            empresa = input(u'Entre com o nome da empresa\n>').strip()
            if len(empresa):
                break
    NOME_EMPRESA = empresa

    if sigla:
        SIGLA_EMPRESA = sigla
    else:
        if PY3:
            lista = ''.join(filter(lambda x: x.isalnum() or x == ' ', remove_accents(NOME_EMPRESA))).split()
        else:
            lista = filter(lambda x: x.isalnum() or x == ' ', remove_accents(NOME_EMPRESA)).split()

        MAX_SIGLA = 10
        if len(lista) == 1:
            SIGLA_EMPRESA = lista[0][:MAX_SIGLA].upper()
        else:
            SIGLA_EMPRESA = ''.join([k[0] for k in lista[:MAX_SIGLA]]).upper()

        while True:
            cam = input(u'Entre com uma Sigla para a Empresa (Max. {} letras/numeros)\nDefault: {}\n>'.format(MAX_SIGLA, SIGLA_EMPRESA)).strip()
            if PY3:
                if len(cam) == 0 or (len(cam) < MAX_SIGLA and cam.isalnum()):
                    try:
                        cam.encode('ASCII')
                        break
                    except UnicodeEncodeError:
                        pass
            else:
                if len(cam) == 0 or (len(cam) < MAX_SIGLA and cam.isalnum()):
                    break
            print('Prefixo inválido: ', cam)
        SIGLA_EMPRESA = cam or SIGLA_EMPRESA

    contents = "# coding: utf-8\n" \
               "CAMINHO_EXT_DEV = '{}'\n" \
               "NOME_EMPRESA = '{}'\nSIGLA_EMPRESA = '{}'\n".format(
        CAMINHO_EXT_DEV.replace('\\','\\\\'), NOME_EMPRESA, SIGLA_EMPRESA
    )
    with codecs.open(_abs(r'config_empacotar.py'), 'w', 'utf-8') as out:
        out.write(contents)


def _iniciar_virtualenv():
    res = local(WORKON, capture=True)
    criar = False
    if 'does not exist' in res:
        puts('virtualenv nao existe, criando...')
        criar = True
    else:
        with prefix(WORKON):
            res = local('python -c "from __future__ import print_function;'
                        'import sys;print(sys.version)"', capture=True)
        puts('virtual env em ' + res)
        if res.startswith('2.7'):
            puts('Versão 2.7, apagando...')
            shutil.rmtree(WORKON_HOME, True)
            puts('criando...')
            criar = True
    if criar:
        local('py -3 -m venv {} --copies'.format(WORKON_HOME))


def _download_file(url, dest_file):
    response = requests.get(url, stream=True)
    _makedirs(dest_file)
    temp_file = dest_file + '.tmp'
    with open(temp_file, 'wb') as out:
        for block in response.iter_content(CHUNK_SIZE):
            if not block:
                break
            out.write(block)
    os.rename(temp_file, dest_file)


def _download():
    puts("*** baixando dependencias")

    for dep in DEP_INSTALLERS:
        if dep.predicate and not dep.predicate():
            puts("{} skipped".format(dep.name))
            continue
        puts("Downloading {}".format(dep.name))
        dest_file = _abs(DEP_CACHE_DIR, dep.name)
        if os.path.exists(dest_file):
            puts('- File {} already exists'.format(dest_file))
            continue
        _download_file(dep.link, dest_file)


def _instalar_dependencias():
    putsc(" instalando dependencias ")
    import zipfile

    for dep in DEP_INSTALLERS:
        if dep.predicate and not dep.predicate():
            puts("{} skipped".format(dep.name))
            continue
        installer_name = _abs(DEP_CACHE_DIR, dep.name)
        puts("Installing {}".format(installer_name))

        if not os.path.exists(installer_name):
            raise IOError('- File {} not exists.'.format(installer_name))
        f = zipfile.ZipFile(installer_name)

        for name in f.namelist():
            new_name = name.replace('PLATLIB', DEP_DEST_DIR).replace('/', '\\')
            new_name = _abs(new_name)
            _makedirs(new_name)
            with open(new_name, 'wb') as out:
                out.write(f.read(name))

        puts('  running post install...')
        if dep.post:
            dep.post()


def _makedirs(filename):
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def _criar_link(origem, destino):
    """
    Utilitário para criar links simbólicos entre diretórios.
    """
    if os.path.exists(destino):
        local('rmdir /S /Q "%s"' % destino)
    comando = 'mklink /J "%s" "%s"' % (destino, origem)
    local(comando)


def link_tkinter():
    for pasta in os.listdir(TCL_PATH):
        cam = os.path.join(TCL_PATH, pasta)
        if os.path.isdir(cam):
            _criar_link(cam, os.path.join(WORKON_HOME, 'lib', pasta))


@task
def preparar_extensao(nome_extensao):
    """
    Cria os arquivos basicos para deploy da extensão.
    A coleta de informações da extensão será feita de forma interativa.

    * nome_extensao: Corresponde ao nome da extensão localizada em sua pasta de projetos
            ou a um caminho completo ou relativo à pasta de projetos.
            Neste caso, o nome padrão da extensão será o último segmento do caminho.
    """
    if deve_gerar_config:
        configurar_empresa()

    if '\\' in nome_extensao or '/' in nome_extensao:
        so_o_nome = os.path.split(nome_extensao)[1]
    else:
        so_o_nome = nome_extensao

    caminhodest = obter_caminho_extensao(nome_extensao + '/_build')
    if os.path.exists(caminhodest):
        puts(' Já existe a pasta _build no destino, extensão já foi preparada')
        return

    putsc('Informações da extensão')
    while True:
        tipo_ext = input(
            'A extensão será instalada no servidor (S), nas estações (E) ou em ambos (A)?\n'
            'Default: A\n>'
        ).upper() or 'A'
        if tipo_ext in ['A', 'E', 'S']:
            break
        print('Escolha inválida\n')

    if tipo_ext != 'S':
        python = input(
            'É uma extensão do tipo plugin em Python? (S/N)\n'
            'Isso irá criar o arquivo versao.py, necessário para a geração automática da versão\n'
            'baseada no conteúdo de versao.ini\n'
            'Default: N\n>'
        ).upper() == 'S'
    else:
        python = False
    def_nome = so_o_nome.capitalize()
    while True:
        validos = string.ascii_letters + string.digits + '_'
        nome = input(
            'Nome da extensão (letras, números ou _):\n'
            'Default: {}\n>'.format(def_nome)
        ) or def_nome
        if all(c in validos for c in nome):
            break
        puts('Nome inválido')
    nome_exibicao = input('Nome de exibicao da extensão:\n>')
    while True:
        produto = input('Produto: (pos/cbo/master)\nDefault: pos\n').strip() or 'pos'
        if produto in ['pos', 'cbo', 'master']:
            break
        print('Escolha inválida\n')

    _preparar_extensao(caminhodest, tipo_ext, nome, produto, nome_exibicao, nome_extensao, python)


def _preparar_extensao(caminhodest, tipo_ext, nome, produto, nome_exibicao, nome_extensao, python):
    if tipo_ext == 'E':
        _ig_pattern = shutil.ignore_patterns('*server.iss')
    elif tipo_ext == 'S':
        _ig_pattern = shutil.ignore_patterns('*client.iss')
    else:
        _ig_pattern = None
    shutil.copytree(_abs('_templates\\_build'), caminhodest, ignore=_ig_pattern)
    if tipo_ext != 'E':
        dest = obter_caminho_extensao(nome_extensao) + '/server'
        if not os.path.exists(dest):
            shutil.copytree(_abs('_templates\\server'), dest)
    if tipo_ext != 'S':
        dest = obter_caminho_extensao(nome_extensao) + '/client'
        if not os.path.exists(dest):
            shutil.copytree(_abs('_templates\\client'), dest)
    if python:
        shutil.copy2(_abs('_templates\\python\\versao.py'),
                     os.path.join(caminhodest, '..\\versao.py'))
        shutil.copy2(_abs('_templates\\python\\__init__.py'),
                     os.path.join(caminhodest, '..\\__init__.py'))
    shutil.copy2(_abs('_templates\\versao.ini'),
                 os.path.join(caminhodest, '..\\versao.ini'))
    # Grava o manifesto.server
    with codecs.open(_abs('_templates\\_build\\pacote\\manifesto.server'), 'r', 'utf-8') as ma:
        manifesto = json.load(ma)
    manifesto['sigla_empresa'] = SIGLA_EMPRESA
    manifesto['empresa'] = NOME_EMPRESA
    manifesto['nome'] = SIGLA_EMPRESA + '-' + nome
    manifesto['nome_exibicao'] = nome_exibicao
    manifesto['produto'] = produto
    manifesto['versao_sdk'] = VERSAO_SDK
    if tipo_ext == 'S':
        manifesto['arquivos'] = list(filter(lambda a: a['destino'] == 'server', manifesto['arquivos']))
    elif tipo_ext == 'E':
        manifesto['arquivos'] = list(filter(lambda a: a['destino'] == 'client', manifesto['arquivos']))
    with codecs.open(os.path.join(caminhodest, 'pacote\\manifesto.server'), 'w+', 'utf-8') as ma:
        json.dump(manifesto, ma, indent=2)


def obter_caminho_client(nome_extensao):
    caminhodest = obter_caminho_extensao(nome_extensao)
    client = os.path.join(caminhodest, 'client')
    if os.path.exists(client):
        return client
    return caminhodest


def _validar_plugin_py(caminho):
    sys.path.append(caminho)
    sys.modules['colibri'] = FakeColibriModule()
    try:
        for arq in os.listdir(caminho):
            if arq.lower().endswith('.py'):
                try:
                    m = arq.rsplit('.', 1)[0].replace('/', '.')
                    dic = importlib.import_module(m)
                    if not {"PLUGIN_NAME", "PLUGIN_VERSION"}.issubset(dic.__dict__.keys()):
                        continue
                except Exception:
                    pass
                try:
                    if 'obter_dados_licenca' not in dic.__dict__:
                        raise SemLicencaException(
                            f'Função obter_dados_licenca não encontrada no plugin em\n {caminho}'
                        )

                    dados_licenca = dic.obter_dados_licenca('')
                    _validar_dados_licenca(dados_licenca, caminho, 'obter_dados_licenca')
                except SemLicencaException:
                    raise
                except Exception:
                    pass
    finally:
        del sys.modules['colibri']


@task
def empacotar_plugin_py(nome_extensao):
    """
    Empacotar plugin Python em um arquivo COP.

    Gera o arquivo 'cop' com o plugin empacotado em um arquivo cop para uso do Colibri.
    * nome_extensao: Corresponde ao nome da extensão localizada em sua pasta de projetos.
    """
    ext_pluginpy = '.cop'
    caminho = obter_caminho_extensao(nome_extensao)
    caminhodest = obter_caminho_client(nome_extensao)

    _validar_plugin_py(caminho)
    # Removo os arquivos compilados da origem (*.pyo, *.pyc)
    for root, dirnames, filenames in os.walk(caminho):
        for filename in fnmatch.filter(filenames, '*.py?'):
            arq = os.path.join(root, filename)
            os.unlink(arq)

    # Compilo os pythons, isso dá eficiência pois o pacote já terá bytecodes
    compileall.compile_dir(caminho, ddir='.' + nome_extensao, force=True)
    # Apago os arquivos .cop do diretório de destino do plugin
    for arq in glob.glob(os.path.join(caminhodest, '*.cop')):
        os.unlink(arq)
    # Agora gero o zip com o diretório dentro referente a este pacote
    zipdest = os.path.join(
        caminhodest, 'plugin.' + nome_extensao.lower() + ext_pluginpy)
    print('Gerando: ' + zipdest)
    with zipfile.ZipFile(zipdest, "w") as arqzip:
        for root, dirnames, filenames in os.walk(caminho):
            for filename in fnmatch.filter(filenames, '*.py*'):
                arq = os.path.join(root, filename)
                dest = nome_extensao + '\\' + arq[len(caminho):]
                arqzip.write(arq, dest)


def compilar_inno(nome_extensao, versao):
    """
    Compila o inno setup para a extensão.
    :param nome_extensao:
    :param versao:
    :return:
    """

    if CAMINHO_INNO == None:
        puts('Inno setup não encontrado. Execute:\n\n >fab instalar_innosetup\n')
        exit(-1)

    for f in glob.glob(obter_caminho_extensao(nome_extensao + '/_build/pacote/*.exe')):
        os.unlink(f)

    try:

        with open(
                obter_caminho_extensao(
                    nome_extensao + '\\_build\\pacote\\manifesto.server'
                ), 'r') as ma:
            json_ma = json.load(ma)
            nome = json_ma['nome']
            nome_exibicao = json_ma.get('nome_exibicao') or nome
    except:
        raise
        nome_exibicao = nome_extensao
        nome = nome_extensao

    def parametros():
        params = dict(
            AppName=nome_exibicao,
            AppVersion=versao,
            ExtensionName=nome,
        )
        return ' '.join(
            '/d{}=\"{}\"'.format(k, v) for k, v in params.items()
            )

    try:
        with lcd(obter_caminho_extensao(nome_extensao)):
            for arq_iss in glob.glob(obter_caminho_extensao(nome_extensao + '/_build/extensao*.iss')):
                local(
                    '"' +os.path.join(CAMINHO_INNO, 'iscc') + '"' +
                    r' {params} "{iss}"'.format(
                        iss=arq_iss,
                        params=parametros()
                    )
                )
    except:
        puts("Falha ao executar o inno setup compiler. Verifique se esta "
             "instalado no path e eh a versao unicode.")
        raise

def gerar_cmpkg(nome_extensao, versao, develop=True):
    """
    Gera um pacote cmpkg para a extensão.
    :param nome_extensao:
    :param versao:
    :param develop:
    :return:
    """
    pasta = obter_caminho_extensao(nome_extensao + '/_build/pacote')
    pasta_saida= obter_caminho_extensao(nome_extensao + '/_build/temp')
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
    if not os.path.exists(pasta + '/manifesto.server'):
        shutil.copy2('manifesto.server', pasta)
    with prefix(WORKON):
        local(
            'python -m colibri_packaging "{pasta}" --pasta_saida "{pasta_saida}" '
            '--versao {versao} --develop {develop}'.format(
                pasta=pasta, pasta_saida=pasta_saida, 
                versao=versao, nome=nome_extensao, develop=develop
            )
        )


@task
def empacotar(nome_extensao, develop=True, build_number=None):
    """
    Empacota a extensão para MarketPlace/Colibri Master.
    Para os plugins python, gera o arquivo COP.
    A versão do empacotamento será extraída dos plugins gerados ou do versao.ini.

    * nome_extensao: Corresponde ao nome da extensão localizada em sua pasta de projetos.
    * develop: Forneça F para pacotes que não são de desenvolvimento.
    * build_number: Número de build a ser usado, se não fornecido será utilizado o valor disponível.

    Exemplos:
        > fab empacotar:MinhaExtensao,build_number=6
        > fab empacotar:MinhaExtensao,develop=F,build_number=6
    """
    if not 'colibri' in os.getenv('VIRTUAL_ENV', ''):
        with prefix(WORKON):
            local(f'fab empacotar:{nome_extensao},{str(develop).lower()}'
                  f'{("," + str(build_number)) if build_number is not None else ""}')
    else:
        _empacotar(nome_extensao, develop, build_number)


def _validar_repo():
    try:
        ret = subprocess.run(['git', 'remote', 'update'], cwd=BASE_PATH, shell=True, stdout=subprocess.PIPE)
        if ret.returncode == 0:
            ret = subprocess.run(['git', 'status', '-uno'], cwd=BASE_PATH, shell=True, stdout=subprocess.PIPE)
            if ret.returncode == 0 and b'Your branch is behind' in ret.stdout:
                puts('*' * 80)
                putsc('Atualize o SDK')
                puts('*' * 80)
                exit(1)
        else:
            puts(f' Falhou acesso ao git com erro: {ret.returncode}')
    except Exception as e:
        puts(f' Falhou ao validar o repositório: {e}')


def _empacotar(nome_extensao, develop, build_number):
    _validar_repo()
    empacotar_scripts(nome_extensao)
    try:
        versaoinfo = __ler_versaoinfo(nome_extensao, develop, build_number)
        if versaoinfo is None:
            exit(1)
        versao = '{majorversion}.{minorversion}.{release}.{build}'.format(**versaoinfo)
        # É um plugin em python? Entao eu devo gerar as versões do plugin
        if os.path.exists(obter_caminho_extensao(nome_extensao + '\\versao.py')):
            __gerar_versoes_py(nome_extensao, versaoinfo)
            empacotar_plugin_py(nome_extensao)
    except SemLicencaException as e:
        puts(80 * '-')
        puts(str(e))
        puts(80 * '-')
        exit(1)

    compilar_inno(nome_extensao, versao)
    gerar_cmpkg(nome_extensao, versao, versaoinfo['develop'])


def __split_versao(versao):
    chaves_versao = ['majorversion', 'minorversion', 'release', 'build']
    partes = [a if a != '*' else None for a in versao.split('.')]
    return {chave: valor for chave, valor in zip(chaves_versao, partes)}


def _validar_dados_licenca(dados_licenca, arquivo, funcao='ObterDadosLicenca'):
    try:
        dados = json.loads(dados_licenca)
    except Exception:
        raise SemLicencaException(
            f'Erro ao processar o retorno de {funcao} no plugin\n{arquivo}'
        )
    if type(dados) is not dict or dados.get('chave_extensao') in [None, 'obter_no_marketplace']:
        raise SemLicencaException(
            f'Cláusula chave_extensao não definida no retorno de {funcao} no plugin\n{arquivo}'
        )


def __obter_versao_plugin_col(nome_extensao):
    try:
        from ctypes import WinDLL, c_void_p, WINFUNCTYPE, c_wchar_p, cast

        for a in glob.glob(obter_caminho_client(nome_extensao) + r'\*.col'):
            plugin = WinDLL(a)
            def _alocar_buffer(buffer):
                return buffer
            def _obter_funcao(nome):
                try:
                    ret = cast(dict_funcoes[nome.lower()], c_void_p).value
                    return ret
                except Exception as e:
                    return cast(0, c_void_p).value
            dict_funcoes = {
                'alocarbuffer': WINFUNCTYPE(c_wchar_p, c_wchar_p)(_alocar_buffer),
                'obterfuncao': WINFUNCTYPE(c_void_p, c_wchar_p)(_obter_funcao)
            }
            plugin.AtribuirObtencaoDeFuncoes(cast(dict_funcoes['obterfuncao'], c_void_p))
            plugin.ObterVersao.restype = c_wchar_p

            if getattr(plugin, 'ObterDadosLicenca', None) is None:
                raise SemLicencaException(
                    f'Função ObterDadosLicenca não encontrada no plugin\n {a}'
                )
            plugin.ObterDadosLicenca.restype = c_wchar_p
            dados_licenca = plugin.ObterDadosLicenca(cast('', c_wchar_p))
            _validar_dados_licenca(dados_licenca, a)

            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                versao = plugin.ObterVersao()
            print(f'===> Versão extraída de {os.path.split(a)[1]}: {versao}')
            return __split_versao(versao)
    except SemLicencaException:
        raise
    except:
        pass


def __obter_versao_plugin_clr(nome_extensao):
    try:
        import clr
    except:
        return

    # Obtenho a versão do binário CLR, se existir
    try:
        for a in glob.glob(obter_caminho_client(nome_extensao) + r'\*.dll'):
            cam, nome = os.path.split(a)
            sem_ext = os.path.splitext(nome)[0]
            namespace = ''.join(sem_ext.split('.'))
            if os.path.exists(os.path.join(cam, namespace)):
                putsc(f"Você não pode ter uma pasta de nome {namespace} dentro de")
                putsc(f"sua pasta do {nome} pois impede a carga do mesmo!")
                exit(-1)

            if nome.lower().startswith('plugin.'):
                versao = None
                try:
                    sys.path.append(cam)
                    clr.AddReference(sem_ext)
                    modulo = __import__(namespace)
                    plugin = modulo.Plugin
                    versao = str(plugin.ObterVersao())

                    if getattr(plugin, 'ObterDadosLicenca', None) is None:
                        raise SemLicencaException(
                            f'Função ObterDadosLicenca não encontrada no plugin\n{a}'
                        )
                    dados_licenca = plugin.ObterDadosLicenca('')
                    _validar_dados_licenca(dados_licenca, a)

                    print(f'===> Versão extraída de {nome}: {versao}')
                except Exception as e:
                    from System.Reflection import Assembly
                    try:
                        versao = str(Assembly.LoadFile(a).GetName().Version.ToString())
                        print(f'===> Versão extraída de {nome}*(assembly): {versao}')
                        putsc(
                            f'Não foi possível obter a versão do plugin de '
                            f'{namespace}.Plugin.ObterVersao()')
                        putsc(
                            f'Versão {versao} do assembly utilizada')
                    except:
                        pass
                if versao:
                    return __split_versao(versao)
    except SemLicencaException:
        raise
    except:
        pass


def __obter_versao_ini(nome_extensao):
    try:
        versao_ini = obter_caminho_extensao(nome_extensao + r'\versao.ini')
        with open(versao_ini, 'r') as vi:
            config = RawConfigParser()
            config.read_file(vi)
            if config.has_section('versaoinfo'):
                return dict(config.items('versaoinfo'))
    except Exception as e:
        print(str(e))
    print(f'===> Não foi possível obter a versão do "versao.ini"')


def __ler_versaoinfo(nome_extensao, develop, build):
    try:
        build = int(build)
    except:
        build = 0

    if type(develop) == str:
        develop = develop.lower() in ['true', '1', 'T']

    itens = __obter_versao_plugin_clr(nome_extensao) or \
            __obter_versao_plugin_col(nome_extensao) or \
            __obter_versao_ini(nome_extensao)

    if itens:
        if build is not None:
            itens['build'] = build
        elif itens.get('build') in [None, '*']:
            itens['build'] = 0
        itens['develop'] = develop
    return itens


def __gerar_versoes_py(nome_extensao, versaoinfo):
    try:
        contents = "MajorVersion = {majorversion}\n" \
                   "MinorVersion = {minorversion}\n" \
                   "Release = {release}\n".format(**versaoinfo)
        with open(obter_caminho_extensao(nome_extensao + r'\__version__.py'), 'w') as out:
            out.write(contents)

        contents = "Build = {build}\nDevelop = {develop}\n".format(
            **versaoinfo
        )
        with open(obter_caminho_extensao(nome_extensao + r'\__build__.py'), 'w') as out:
            out.write(contents)
    except Exception as e:
        puts('Falha ao gerar informacao de versão para o plugin Python: ' + e)


@task
def empacotar_scripts(nome_extensao):
    """
    Gera os scripts para a extensão.

    * nome_extensao: Corresponde ao nome da extensão localizada em sua pasta de projetos.
    """
    if not 'colibri' in os.getenv('VIRTUAL_ENV', ''):
        with prefix(WORKON):
            local('fab empacotar_scripts:{}'.format(nome_extensao))
    else:
        _empacotar_scripts(nome_extensao)


def _empacotar_scripts(nome_extensao):
    from colibri_packaging import CAM_7ZA
    destino = obter_caminho_extensao(nome_extensao + '\\_build\\pacote\\_scripts.zip')
    with settings(warn_only=True):
        local('del "{}"'.format(destino))

    cam_scripts = obter_caminho_extensao(nome_extensao + '\\_scripts\\')
    if not os.path.exists(cam_scripts):
        puts('Não há scripts a empacotar')
        return

    with lcd(cam_scripts):
        with settings(warn_only=True):
            retorno = local(
                CAM_7ZA +
                ' a -tzip "{destino}" -mcu *'.format(destino=destino)
            )
            if retorno == 1:
                print('Warning (Non fatal error(s)). For example, one or more files were locked by some other application, so they were not compressed.')


@task
def instalar_innosetup():
    """
    Instala innosetup unicode nesta máquina.
    """
    dest_file = _abs('isccsetup.exe')
    try:
        os.unlink(dest_file)
    except:
        pass
    putsc('Innosetup')
    puts(' Baixando...')
    puts(' Ao instalar mantenha o "Install Inno Setup Preprocessor" marcado')
    _download_file(INNO_SETUP_DOWNLOAD, dest_file)
    puts(' Instalando...')
    ret = call(dest_file, shell=True)
    if ret == 0:
        puts(' Instalado com sucesso')
        puts(' Apagando o arquivo...')
        os.unlink(dest_file)
    else:
        puts(' Falhou com erro: {}'.format(ret))
    return ret


@task(default=True)
def ajuda(comando=None):
    '''
    Exibe a ajuda para um comando "fab ajuda:nome".
    * comando: Nome do comando
    '''
    if comando is None:
        show_commands(__doc__, 'normal')
    else:
        display_command(comando)
