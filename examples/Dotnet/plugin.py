import json
import os
import sys
from .colibri_mod import assinar_evento, mostrar_mensagem, callback, gravar_config, \
    mostrar_teclado, obter_configs, verificar_permissao

from .util import retornar, obter_caminho_plugin, criar_logger

logger = criar_logger(__name__, os.path.join(obter_caminho_plugin(), 'temp.log'))

try:
    import clr
    import System
    from System.Collections.Generic import Dictionary
except:
    logger.exception('Falha ao inciar crl')
    raise
try:
    sys.path.append(obter_caminho_plugin())
    clr.AddReference("PluginDotnet")
except Exception as e:
    logger.exception('Falha ao adicionar plugin')
    raise

try:
    from PluginDotnet import MeuPlugin
    from PluginDotnet import Colibri
except:
    logger.exception('Falha ao importar plugin')
    raise


# Nome e versão do Plugin, obrigatórios
try:
    PLUGIN_NAME = str(MeuPlugin.ObterNome())
    PLUGIN_VERSION = str(MeuPlugin.ObterVersao())
except:
    logger.exception('Falha ao obter nome e versão')
    raise
# Logger para testes
log_file_name = os.path.join(obter_caminho_plugin(), PLUGIN_NAME + '.log')
logger = criar_logger(__name__, log_file_name)


def configurar(maquinas):
    MeuPlugin.Configurar(System.String(str(maquinas)))


def registrar_assinaturas():
    try:
        MeuPlugin.RegistrarAssinaturas()
    except:
        logger.exception('falha ao assinar')


def notificar(um_evento, um_contexto):
    return str(MeuPlugin.Notificar(um_evento, um_contexto))

# Funções obrigatórias
def obter_dados_fabricante():
    return str(MeuPlugin.ObterDadosFabricante())


def ativar(maquina):
    try:
        MeuPlugin.Ativar(System.Int32(maquina))
    except:
        logger.exception('Falha ao ativar')


def desativar(maquina):
    try:
        MeuPlugin.Desativar(System.Int32(maquina))
    except:
        logger.exception('Falha ao desativar')


def configurar_db(servidor, banco, usuario, senha, provedor):
    logger.debug(
        'configurar_db: servidor %s, banco %s, usuario %s, senha %s, provedor %s',
        servidor, banco, usuario, senha, provedor
    )
    MeuPlugin.ConfigurarDB(
        System.String(servidor), System.String(banco), System.String(usuario),
        System.String(senha), System.String(provedor)
    )


def verificar_versao(informacao):
    info = json.loads(informacao)
    if info['versao'] >= 2000:
        return retornar(erro='Não suporta versão >= 2000')
    return ''  # Nenhuma objeção a essa versão


def atribuir_funcoes():
    """
    Atribui as funções que poderão ser chamadas de dentro do código dotnet.
    O código abaixo simplesmente redireciona as chamdas para as funções originais,
    exportadas pelo Colibri
    """
    funcoes = Dictionary[System.String, System.Object]()

    try:
        def _assinar_evento(evento):
            logger.debug('Evento assinado ' + str(evento))
            assinar_evento(PLUGIN_NAME, str(evento))
        funcoes['AssinarEvento'] = System.Action[System.String](_assinar_evento)

        def _callback(evento, contexto):
            callback(PLUGIN_NAME, str(evento), str(contexto))
        funcoes['Callback'] = System.Action[System.String, System.String](_callback)

        def _gravar_config(uma_config, maquina_id, um_valor):
            gravar_config(PLUGIN_NAME, str(uma_config), int(maquina_id), str(um_valor))
        funcoes['GravarConfig'] = System.Action[System.String, System.Int32, System.String](_gravar_config)

        def _mostrar_mensagem(dados):
            return System.Int32(mostrar_mensagem(PLUGIN_NAME, str(dados)))
        funcoes['MostrarMensagem'] = System.Func[System.String, System.Int32](_mostrar_mensagem)

        def _mostrar_teclado(dados):
            return System.String(mostrar_teclado(PLUGIN_NAME, str(dados)))
        funcoes['MostrarTeclado'] = System.Func[System.String, System.String](_mostrar_teclado)

        def _obter_configs(maquina):
            return System.String(obter_configs(PLUGIN_NAME, int(maquina)))
        funcoes['ObterConfigs'] = System.Func[System.Int32, System.String](_obter_configs)

        def _verificar_permissao(GUID, elevar):
            return System.Int32(verificar_permissao(PLUGIN_NAME, str(GUID), int(elevar)))
        funcoes['VerificarPermissao'] = System.Func[System.String, System.Int32, System.Int32](_verificar_permissao)
    except:
        logger.exception("Falha ao montar dicionário de funções")

    try:
        Colibri.AtribuirFuncoes(funcoes)
    except:
        logger.exception("Falha ao atribuir as funções")


# Atribui as funções para uso do dotnet
atribuir_funcoes()