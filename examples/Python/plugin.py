# coding: utf-8
import json
import os
from util import obter_caminho_plugin, criar_logger,  codifica_retorno
from colibri_mod import callback, assinar_evento, obter_configs, gravar_config

# Nome e versão do Plugin, obrigatórios
PLUGIN_NAME = 'Teste'
PLUGIN_VERSION = '1.0.0.0'

# Variavel privada com o erro ocorrido na notificaçao
__last_error = ''

# Logger para testes
log_file_name = os.path.join(obter_caminho_plugin(), PLUGIN_NAME + '.log')
logger = criar_logger(__name__, log_file_name)


# Funções opcionais: Implemente as que desejar
def ativar(maquina):
    logger.debug('plugin ativado na maquina: %d', maquina)


def desativar(maquina):
    logger.debug('plugin desativado na maquina: %d', maquina)

    
def atualizar():
    try:
        # Atualize seu plugin aqui
        return 1
    except Exception as error:
        return str(error)


def configurar_db(servidor, banco, usuario, senha, provedor):
    logger.debug(
        'configurar_db: servidor %s, banco %s, usuario %s, senha %s, provedor %s',
        servidor, banco, usuario, senha, provedor
    )


def configurar(maquinas):
    logger.debug('configurar: %s', maquinas)

    
def notificar(evento, informacao):
    logger.debug(
        'notificar: evento %s, informacao %s' %
        (evento, informacao)
    )
    try:
        pass  # Tratar a notificação
    except Exception as erro:
        logger.error("falha notificacao de %s: %s" % (evento, erro))
        # atualizar __last_error, em caso de erro
        global __last_error
        __last_error = str(erro)
        return 0
    return 1


def obter_erro():
    return codifica_retorno(__last_error)


def verificar_versao(informacao):
    info = json.loads(informacao)
    if info['versao'] > 2000:
        return codifica_retorno('Não suporta versão > 2000')
    return ''  # Nenhuma objeção a essa versão


def registrar_assinaturas():
    logger.debug('registrar_assinaturas')
    eventos = []  # Lista de eventos assinados pelo plugin
    for evt in eventos:
        logger.debug('assinar_evento: %s, %s', PLUGIN_NAME, evt)
        assinar_evento(PLUGIN_NAME, evt)


def obter_macro(uma_macro):
    exemplo_macros = {'nome_macro': 'valor_macro'}
    ret = exemplo_macros.get(uma_macro, uma_macro)
    logger.debug('obter_macro: %s:%s', uma_macro, ret)
    return ret
