# coding: utf-8
from __future__ import unicode_literals
import os
import sys
import shutil
import glob
import fnmatch
import compileall
import zipfile
import json
from importlib import import_module
from ConfigParser import RawConfigParser
from collections import namedtuple
from fabric.api import task, local, puts, prefix, hide
from fabric.context_managers import shell_env, _setenv, settings
from fabric import state
from distutils.dir_util import copy_tree

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
_abs = lambda *x: os.path.join(BASE_PATH, *x)

sys.path.insert(0, BASE_PATH)

try:
    from config_empacotar import CAMINHO_PLUGINS_DEV, CAMINHO_NCR_COLIBRI, \
        PREFIXO_EMPRESA
    CAMINHO_PLUGINS_DEST = os.path.join(CAMINHO_NCR_COLIBRI, 'plugins')
    deve_gerar_config= False
except Exception as e:
    deve_gerar_config= True


Dependency = namedtuple('Dependency', 'name link predicate post')

TCL_PATH = r'c:\python27\tcl'
ENV_NAME = 'colibri'
WORKON = r'workon {}'.format(ENV_NAME)
WORKON_HOME = os.environ.get('WORKON_HOME')
WORKON_HOME = os.path.join(WORKON_HOME, ENV_NAME) if WORKON_HOME else ENV_NAME

DEP_CACHE_DIR = '_cache'
DEP_DEST_DIR = r'{}\Lib\site-packages'.format(WORKON_HOME)
CHUNK_SIZE = 1024


# A função original em fabric.context_managers  não suporta espaços no nome
def lcd(path):
    which = 'lcwd'
    if state.env.get(which) and not path.startswith('/') \
            and not path.startswith('~'):
        new_cwd = state.env.get(which) + '/' + path
    else:
        new_cwd = path
    return _setenv({which: new_cwd})


def obter_caminho_plugin(pasta=''):
    caminho = os.path.normpath(os.path.join(CAMINHO_PLUGINS_DEV, pasta))
    return caminho

putsc = lambda x: puts(" {:*^80}".format(x))


def should_install_pywin32():
    """
    Predicate function that must return True if the package win32 is required.
    """
    res = local(
        'python -c "exec(\'try: import win32com'
        '\\nexcept: print 1\')"',
        capture=True
    )
    # res will have value 1 if python could not import win32com
    return bool(res.strip())


def should_install_pyodbc():
    """
    Predicate function that must return True if the package pyodbc is required.
    """
    res = local(
        'python -c "exec(\'try: import pyodbc'
        '\\nexcept: print 1\')"',
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
    local('python "{}" -install'.format(post_script))
    shutil.rmtree(post_script_dir)


DEP_INSTALLERS = (
    Dependency(
        name='pywin32-219.win32-py2.7.exe',
        link='http://downloads.sourceforge.net/project/pywin32/pywin32/'
             'Build%20219/pywin32-219.win32-py2.7.exe?r=&ts=1432061293'
             '&use_mirror=iweb',
        predicate=should_install_pywin32,
        post=post_install_pywin32
    ),
    Dependency(
        name='pyodbc-3.0.7.win32-py2.7.exe',
        link='https://pyodbc.googlecode.com/files/pyodbc-3.0.7.win32-py2.7.exe',
        predicate=should_install_pyodbc,
        post=None
    ),
    Dependency(
        name='pycrypto-2.6.1.win32-py2.7.exe',
        link='http://www.voidspace.org.uk/python/pycrypto-2.6.1/pycrypto-2.6.1.win32-py2.7.exe',
        predicate=None,
        post=None
    ),
)


@task
def iniciar_ambiente():
    """
    Monta ambiente de python do Colibri
    """
    putsc(" iniciando ambiente com dependencias ")
    _iniciar_virtualenv()
    local('pip install requests')

    if WORKON_HOME not in sys.executable:
        global TCL_PATH
        TCL_PATH = os.path.join(os.path.split(sys.executable)[0], 'tcl')

    with prefix(WORKON):
        _download()
        _instalar_dependencias()
        local(r'pip install -r {}'.format(_abs('requirements_dev.txt')))
        for arq in glob.glob(_abs('pythonnet-2.0\\*.*')):
            shutil.copy(arq, DEP_DEST_DIR)

        dest = os.path.join(DEP_DEST_DIR, 'yaml')
        try:
            os.mkdir(dest)
        except:
            pass
        for arq in glob.glob(_abs('yaml\\*.*')):
            shutil.copy(arq, os.path.join(dest, os.path.split(arq)[1]))

        link_tkinter()

@task
def gerar_config():
    """
    Configura os caminhos para trabalhar com plugins
    """
    putsc('Configuração dos caminhos')
    global CAMINHO_PLUGINS_DEV, CAMINHO_NCR_COLIBRI, CAMINHO_PLUGINS_DEST, \
        PREFIXO_EMPRESA
    cam = raw_input(
        'Entre a pasta base de projeto dos plugins\n(Default: {})\n>'.format(
            CAMINHO_PLUGINS_DEV))
    if cam and not os.path.exists(cam):
        print 'Pasta não existe'
        exit(0)
    CAMINHO_PLUGINS_DEV = cam or CAMINHO_PLUGINS_DEV

    cam = raw_input(
        'Entre a pasta do NCR colibri \n(Default: {})\n>'.format(
            CAMINHO_NCR_COLIBRI))
    if cam and not os.path.exists(cam):
        print 'Pasta não existe'
        exit(0)
    CAMINHO_NCR_COLIBRI = cam or CAMINHO_NCR_COLIBRI
    CAMINHO_PLUGINS_DEST = os.path.join(CAMINHO_NCR_COLIBRI, 'plugins')

    while True:
        cam = raw_input(u'Entre com um prefixo para os plugins da empresa (Max. 5 letras/numeros)\n>').strip()
        if len(cam) and cam.isalnum():
            break
        print 'Prefixo inválido: ', cam
    PREFIXO_EMPRESA = cam

    contents = "CAMINHO_PLUGINS_DEV = '{}'\nCAMINHO_NCR_COLIBRI = '{}'\n" \
               "PREFIXO_EMPRESA = '{}'\n".format(
        CAMINHO_PLUGINS_DEV, CAMINHO_NCR_COLIBRI, PREFIXO_EMPRESA
    )
    with open(_abs(r'config_empacotar.py'), 'w') as out:
        out.write(contents)
    CAMINHO_PLUGINS_DEST = os.path.join(CAMINHO_NCR_COLIBRI, 'plugins')


def _iniciar_virtualenv():
    res = local(WORKON, capture=True)
    if 'does not exist' in res:
        puts('virtualenv nao existe, criando...')
        local('mkvirtualenv {}'.format(ENV_NAME))


def _download():
    puts("*** baixando dependencias")
    import requests

    for dep in DEP_INSTALLERS:
        if dep.predicate and not dep.predicate():
            puts("{} skipped".format(dep.name))
            continue
        puts("Downloading {}".format(dep.name))
        dest_file = _abs(DEP_CACHE_DIR, dep.name)
        if os.path.exists(dest_file):
            puts('- File {} already exists'.format(dest_file))
            continue

        response = requests.get(dep.link, stream=True)
        _makedirs(dest_file)
        temp_file = dest_file + '.tmp'
        with open(temp_file, 'wb') as out:
            for block in response.iter_content(CHUNK_SIZE):
                if not block:
                    break
                out.write(block)
        os.rename(temp_file, dest_file)


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
        local('rmdir /S /Q %s' % destino)
    comando = 'mklink /J %s %s' % (destino, origem)
    local(comando)

@task
def link_tkinter():
    for pasta in os.listdir(TCL_PATH):
        cam = os.path.join(TCL_PATH, pasta)
        if os.path.isdir(cam):
            _criar_link(cam, os.path.join(WORKON_HOME, 'lib', pasta))


def preparar_plugin(caminhodest):
    if not os.path.exists(caminhodest):
        with open(_abs('_templates\\_build\\pacote\\manifesto.server'), 'r') as ma:
            manifesto = json.load(ma)
        shutil.copytree(_abs('_templates\\_build'), caminhodest)
        tipo = raw_input('Trata-se de um plugin em python? (S/N)\nDefault: S\n')
        if tipo.upper() != 'N':
            shutil.copy2(_abs('_templates\\__version__.py'),
                         os.path.join(caminhodest, '..\\__version__.py'))
            shutil.copy2(_abs('_templates\\versao.py'),
                         os.path.join(caminhodest, '..\\versao.py'))
            shutil.copy2(_abs('_templates\\__init__.py'),
                         os.path.join(caminhodest, '..\\__init__.py'))
        putsc('Informações do plugin')
        nome = raw_input('Nome do plugin:\n')
        if nome:
            manifesto['nome'] = PREFIXO_EMPRESA + '.' + nome
        nome_exibicao = raw_input('Nome de exibicao do plugin:\n')
        if nome_exibicao:
            manifesto['nome_exibicao'] = nome_exibicao
        produto = raw_input('Produto:\nDefault: pos\n')
        if produto:
            manifesto['produto'] = produto
        with open(os.path.join(caminhodest, 'pacote\\manifesto.server'), 'w+') as ma:
            json.dump(manifesto, ma)



@task
def empacotar_plugin_py(nome_plugin):
    """
    Empacotar plugin.

    Gera o arquivo 'cop' com o plugin empacotado no diretorio de binarios
    """
    ext_pluginpy = '.cop'
    caminho = obter_caminho_plugin(nome_plugin)
    caminhodest = obter_caminho_plugin(nome_plugin + '/_build')
    preparar_plugin(caminhodest)

    # Removo os arquivos compilados da origem (*.pyo, *.pyc)
    for root, dirnames, filenames in os.walk(caminho):
        for filename in fnmatch.filter(filenames, '*.py?'):
            arq = os.path.join(root, filename)
            os.unlink(arq)

    # Compilo os pythons, isso dá eficiência pois o pacote já terá bytecodes
    compileall.compile_dir(caminho, ddir='.' + nome_plugin, force=True)
    # Apago os arquivos .cop do diretório de destino do plugin
    for arq in glob.glob(os.path.join(caminhodest, '*.cop')):
        os.unlink(arq)
    # Agora gero o zip com o diretório dentro referente a este pacote
    zipdest = os.path.join(
        caminhodest, 'plugin.' + nome_plugin.lower() + ext_pluginpy)
    print('Gerando: ' + zipdest)
    with zipfile.ZipFile(zipdest, "w") as arqzip:
        for root, dirnames, filenames in os.walk(caminho):
            for filename in fnmatch.filter(filenames, '*.py*'):
                arq = os.path.join(root, filename)
                dest = nome_plugin + '\\' + arq[len(caminho):]
                arqzip.write(arq, dest)

    # copia para a pasta ncr-colibri
    cam = '../ncr-colibri/plugins/' + nome_plugin
    if not os.path.exists(cam):
        os.makedirs(cam)
    shutil.copy2(zipdest, cam)


@task
def inno(nome_plugin, versao, extensao):
    for f in glob.glob(obter_caminho_plugin(nome_plugin + '/_build/pacote/*.exe')):
        os.unlink(f)
    def parametros():
        params = dict(
            AppName=nome_plugin,
            AppVersion=versao,
            Extensao=extensao,
        )
        return ' '.join(
            '/d{}=\"{}\"'.format(k, v) for k, v in params.items()
            )

    try:
        local(
            r'iscc {params} {iss}'.format(
                iss=obter_caminho_plugin(nome_plugin + '/_build/plugin.iss'),
                params=parametros()
            )
        )
    except:
        puts("Falha ao executar o inno setup compiler. Verifique se esta "
             "instalado no path e eh a versao unicode.")
        raise

@task
def cmpkg(plugin, versao, develop=True):
    pasta = obter_caminho_plugin(plugin + '/_build/pacote')
    pasta_saida= obter_caminho_plugin(plugin + '/_build/temp')
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
    if not os.path.exists(pasta + '/manifesto.server'):
        shutil.copy2('manifesto.server', pasta)
    with prefix(WORKON):
        local(
            'python -m colibri-packaging "{pasta}" --pasta_saida "{pasta_saida}" '
            '--versao {versao} --develop {develop}'.format(
                pasta=pasta, pasta_saida=pasta_saida, 
                versao=versao, nome=plugin, develop=develop
            )
        )

def compilar_plugin_delphi(plugin):
    """
    Exemplo de compilaçao do plugin em dll
    """
    path = obter_caminho_plugin(plugin)
    p = dict(
        dcc32 = "C:\\Program Files (x86)\\Embarcadero\\RAD Studio\\9.0\\bin\\dcc32.exe" ,
        projeto = "plugin.{plugin}.dpr".format(plugin=plugin),
        delphi_lib = '"C:\\Program Files (x86)\\Embarcadero\\RAD Studio\\9.0\\lib\\Win32\\release";D:\\Vcl\\xe2bpl;D:\\Vcl\\xe2lib\\;D:\\Drive\\Vcl\\xe2bpl;D:\\Drive\\Vcl\\xe2lib\\;',
        colibri_lib = 'D:\\Vcl\\co2lib\\;D:\\Builder\\plugins\\;',
        pasta_dcu = '{path}\\dcu\\'.format(path=path),
        pasta_saida = '{path}\\_build\\'.format(path=path),
        unit_scope = 'System.Win;Data.Win;Datasnap.Win;Web.Win;Soap.Win;Xml.Win;Bde;Vcl;Vcl.Imaging;Vcl.Touch;Vcl.Samples;Vcl.Shell;System;Xml;Data;Datasnap;Web;Soap;Winapi;Data.win;'
    )
    # cria a pasta dcu
    if not os.path.exists(p['pasta_dcu']):
        os.makedirs(p['pasta_dcu'])
    # compila o projeto 
    cmd = ' "{dcc32}" {projeto} -H -B -Q -U{delphi_lib}{colibri_lib} -N{pasta_dcu} -E{pasta_saida} -NS{unit_scope}'.format(**p)
    with lcd(path + '\\prj'):
        local(cmd)

def coletar_versao_plugin_delphi(plugin):
    # Colete a versão de um arquivo do seu projeto
    return '1.0.0.0'


@task
def empacotar(plugin, develop=True, pasta_saida=None, build_number=None):
    if type(develop) == str:
        develop = develop.lower() in ['true', '1', 'T']

    empacotar_scripts(plugin)

    caminhodest = obter_caminho_plugin(plugin + '/_build')
    preparar_plugin(caminhodest)

    # É um plugin em python?
    if os.path.exists(obter_caminho_plugin(plugin + '\\__init__.py')):
        versao = _generate_buildfile_py(plugin, build_number, str(develop))
        empacotar_plugin_py(plugin)
        inno(plugin, versao, '.cop')
    else:
        versao = coletar_versao_plugin_delphi(plugin)
        compilar_plugin_delphi(plugin)
        inno(plugin, versao, '.col')
    cmpkg(plugin, versao, develop=develop)


def _generate_buildfile_py(plugin, build_number='1', develop='True'):
    try:
        build_number = int(build_number)
    except:
        build_number = 0

    contents = "Build = {}\nDevelop = {}\n".format(
        build_number, develop
    )
    with open(obter_caminho_plugin(plugin + r'\__buildnumber__.py'), 'w') as out:
        out.write(contents)

    sys.path.append(obter_caminho_plugin(plugin))
    versao = import_module('versao')
    return versao.version_info()['fileversion']


@task
def empacotar_scripts(
        plugin
    ):
    with prefix(WORKON):
        destino = obter_caminho_plugin(plugin + '\\_build\\pacote\\_scripts.zip')
        with settings(warn_only=True):
            local('del "{}"'.format(destino))

        cam_scripts = obter_caminho_plugin(plugin + '\\_scripts\\')
        if not os.path.exists(cam_scripts):
            return

        with lcd(cam_scripts):
            with settings(warn_only=True):
                retorno = local(
                    obter_caminho_plugin(r"7za.exe") +
                    ' a -tzip "{destino}" -mcu *'.format(destino=destino)
                )
                if retorno == 1:
                    print('Warning (Non fatal error(s)). For example, one or more files were locked by some other application, so they were not compressed.')




try:
    with hide('output', 'run'):
        local(r'iscc', capture=True)
except Exception as e:
    putsc(
        "Por favor instale o InnoSetup e certifique-se que o ISCC.exe está no path.")
    putsc(" Saiba mais em http://www.jrsoftware.org/isdl.php ")
    exit(-1)

if deve_gerar_config:
    CAMINHO_PLUGINS_DEV = _abs('examples')
    CAMINHO_NCR_COLIBRI = r'c:\NCR Colibri'
    PREFIXO_EMPRESA = ''
    gerar_config()
