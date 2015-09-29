# coding: utf-8
import json
from pywin.mfc import dialog
import win32ui
import win32con
from dialog_mfc import DlgLiberaMesa
from dialog_tk import liberar_mesa
from colibri_gui import mfc_do_modal


try:
    from colibri import assinar_evento, obter_configs, gravar_config
except ImportError:
    """ Permite testar os scripts fora do colibri
    """
    def assinar_evento(um_plugin, um_evento):
        pass
    def obter_configs(um_plugin, uma_maquina):
        return '{"configs":{"url":{"valor":"http://127.0.0.1:4545/"}}}'
    def gravar_config(um_plugin, uma_config, maquina_id, um_valor):
        pass


# Nome e versão do Plugin, obrigatórios
PLUGIN_NAME = u'Bloqueio de Mesas'.encode('cp1252')
PLUGIN_VERSION = '1.0.0.0'

DADOS_FABRICANTE = {
    "fabricante":
        {
            "empresa": "Empresa",
            "desenvolvedor": "Equipe",
            "termos_da_licenca": "",
            "direitos_de_copia": "",
            "marcas_registradas": "",
        },
    "suporte":
        {
            "email": "suporte@empresa.com",
            "url": "",
            "telefone": "(99)9999-9999"
        },
}


def retornar(**kwargs):
    return json.dumps(kwargs).decode('utf-8').encode('cp1252')


# Funções obrigatórias
def obter_dados_fabricante():
    return retornar(**DADOS_FABRICANTE)


bloqueadas = []
def notificar(evento, contexto):
    global bloqueadas
    try:
        if evento == 'EventoDeTicket.AoSelecionarTicket':
            dados = json.loads(contexto)
            if int(dados.get('codigo', 0)) in bloqueadas:
                win32ui.MessageBox("Mesa bloqueada: " + dados.get('codigo', 0),
                                   "Plugin de Mesas", win32con.MB_OK)
                return retornar(acao='abort', erro='Mesa bloqueada')
            # Utilize os dados aqui
        elif evento == 'EventoDeUIDePlugin.LiberarMesa':
            dlg = DlgLiberaMesa()
            mfc_do_modal(dlg)
            mesa = dlg.retorno
            if mesa:
                try:
                    bloqueadas.remove(mesa)
                    win32ui.MessageBox(u"Mesa liberada: " + str(mesa), "Plugin de Mesas", win32con.MB_OK)
                except ValueError:
                    win32ui.MessageBox(u"Mesa não estava bloquada : " + str(mesa), "Plugin de Mesas", win32con.MB_OK)
        elif evento == 'EventoDeUIDePlugin.BloquearMesa':
            mesa = liberar_mesa('Bloquear mesa')
            if mesa:
                win32ui.MessageBox("Mesa bloqueada: " + str(mesa), "Plugin de Mesas", win32con.MB_OK)
                bloqueadas.append(mesa)
    except Exception as erro:
        return retornar(erro=str(erro))
    return ''


def registrar_assinaturas():
    assinar_evento(PLUGIN_NAME, 'EventoDeTicket.AoSelecionarTicket')
    assinar_evento(PLUGIN_NAME, 'EventoDeUIDePlugin.LiberarMesa')
    assinar_evento(PLUGIN_NAME, 'EventoDeUIDePlugin.BloquearMesa')


def verificar_versao(informacao):
    info = json.loads(informacao)
    if info['versao'] >= 2000:
        return retornar(erro='Não suporta versão >= 2000')
    return ''  # Nenhuma objeção a essa versão


def obter_macro(uma_macro):
    exemplo_macros = {'hab_liberar': len(bloqueadas) > 0,
                      'bloqueadas': ', '.join(str(a) for a in bloqueadas)}
    try:
        return retornar(valor=exemplo_macros[uma_macro])
    except KeyError:
        return retornar(erro='Macro desconhecida')

def configurar(maquinas):
    url = json.loads(obter_configs(PLUGIN_NAME, 0))['configs'].get('url', {}).get('valor', 'http://127.0.0.1:7070/')
    url = dialog.GetSimpleInput(u"url do serviço", url, u"Configuração")
    if url is not None:
        gravar_config(PLUGIN_NAME, 'url', 0, url)
