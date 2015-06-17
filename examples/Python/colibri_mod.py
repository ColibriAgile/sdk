# coding: utf-8

"""

Importa funções do colibri.
Caso não consiga, cria as funções para permitir testes fora do Colibri

"""
try:
    from colibri import callback, assinar_evento, obter_configs, gravar_config
except ImportError:
    """ Permite testar os scripts fora do colibri
    """
    def callback(um_plugin, um_tipo, um_valor):
        pass

    def assinar_evento(um_plugin, um_identificador):
        pass

    def obter_configs(um_plugin, uma_maquina):
        return '{"configs":{}}'

    def gravar_config(um_plugin, uma_config, maquina_id, um_valor):
        pass

