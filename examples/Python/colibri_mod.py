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
    def callback(um_plugin, um_evento, um_contexto):
        pass

    def assinar_evento(um_plugin, um_evento):
        pass

    def obter_configs(um_plugin, uma_maquina):
        return '{"configs":{}}'

    def gravar_config(um_plugin, uma_config, maquina_id, um_valor):
        pass

# funções do GP 1001
try:
    from colibri import mostrar_teclado, mostrar_mensagem
except ImportError:
    def mostrar_teclado(um_plugin, dados):
        return '{"retorno":false, "resposta":''}'
    def mostrar_mensagem(um_plugin, dados):
        pass


