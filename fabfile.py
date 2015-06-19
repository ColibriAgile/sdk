# coding: utf-8
from __future__ import unicode_literals
import os
import sys
import shutil
import glob
import compileall
import zipfile
from collections import namedtuple
from fabric.api import task, local, puts, prefix
from config_empacotar import CAMINHO_PLUGINS_DEV, CAMINHO_PLUGINS_DEST

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
_abs = lambda *x: os.path.join(BASE_PATH, *x)

Dependency = namedtuple('Dependency', 'name link predicate post')

sys.path.insert(0, BASE_PATH)

ENV_NAME = 'colibri'
WORKON = r'workon {}'.format(ENV_NAME)
WORKON_HOME = os.environ.get('WORKON_HOME')
WORKON_HOME = os.path.join(WORKON_HOME, ENV_NAME) if WORKON_HOME else ENV_NAME

DEP_CACHE_DIR = '_cache'
DEP_DEST_DIR = r'{}\Lib\site-packages'.format(WORKON_HOME)
CHUNK_SIZE = 1024


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
)


@task
def iniciar_ambiente():
    putsc(" iniciando ambiente com dependencias ")
    _iniciar_virtualenv()
    local('pip install requests')

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


@task
def empacotar_plugin_py(nome_plugin, caminhodest=None):
    """
    Gera o arquivo 'cop' com o plugin empacotado no diretório de binários
    """
    EXT_PLUGINPY = '.cop'
    caminho = os.path.join(CAMINHO_PLUGINS_DEV, nome_plugin)
    caminhodest = caminhodest or os.path.join(CAMINHO_PLUGINS_DEST, nome_plugin)

    # Removo os arquivos compilados da origem (*.pyo, *.pyc)
    for arq in glob.glob(os.path.join(caminho, '*.py[co]')):
        os.unlink(arq)
    # Compilo os pythons, isso dá eficiência pois o pacote já terá bytecodes
    compileall.compile_dir(caminho, force=True)
    # Apago o diretório de destino do plugin
    shutil.rmtree(caminhodest, True)
    # Copio tudo, exceto arquivos py, pyo, pyd e arquivos de IDE
    print('Copiando de '+ caminho+ ' para '+ caminhodest)
    shutil.copytree(
        caminho,
        caminhodest,
        ignore=shutil.ignore_patterns('.idea', '*.py', '*.py[co]')
    )
    # Agora gero o zip com o diretório dentro referente a este pacote
    zipdest = os.path.join(caminhodest, 'plugin.'+nome_plugin.lower() + EXT_PLUGINPY)
    print('Gerando: '+ zipdest)
    with zipfile.ZipFile(zipdest, "w") as arqzip:
        for arq in glob.glob(os.path.join(caminho, '*.py*')):
            dest = nome_plugin + '\\' + arq[len(caminho):]
            arqzip.write(arq, dest)