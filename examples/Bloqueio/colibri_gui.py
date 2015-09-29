# coding: utf-8
import types
import win32gui
import win32ui
from threading import Thread

FW_COLIBRI = ('TApplication', "NCR Colibri POS")
FW_GER_PLUGINS = ('TformPrincipal', 'NCR Colibri - Gerenciador de plugins')


def mfc_do_modal(dlg):
    """
    Executa um diálogo modal MFC em um thread separado.
    Necessário para abrir diálogos a partir do Colibri.
    :param dlg: Diálog MFC
    :return: Resultado da DoModal
    """
    r = dict()

    # Executa o modal e guarda o retorno em r['ret']
    def _DoModal():
        r['ret'] = dlg.DoModal()

    t = Thread(target=_DoModal)
    t.start()
    t.join()
    return r.get('ret')


def tk_como_modal(tk, fw_janela=FW_COLIBRI):
    """
    Emula um diálogo modal.
    Desabilita a janela 'parent' e programa a sua reabilitação para antes
        do fechamento do diálogo.
    Altera a função tk.destroy para reabilitar a tela principal
    :param tk: janela do Tk
    :param fw_janela: Dados para FindWindow da janela 'parent'
    """

    # janela fica sobre as outras
    tk.attributes('-topmost', 1)

    # Procuro a janela do Colibri
    h = win32gui.FindWindow(*fw_janela)

    if h:
        #desabilita a janela do Colibri
        win32gui.EnableWindow(h, False)

        # Ao finalizar, habilita a janela do Colibri e depois destrói
        destroy_org = tk.destroy

        #substituo a tk.destroy por essa aqui, que reabilita a janela
        def finaliza(self):
            win32gui.EnableWindow(h, True)
            destroy_org()
        tk.destroy = types.MethodType(finaliza, tk.__class__)

        # A destruição da janela pelo clique no [X]
        # invoca a função de finalização
        tk.wm_protocol('WM_DELETE_WINDOW', finaliza)


def tk_botao_default (janela, bt):
    """
    Define o botão default do diálogo
    """
    bt.configure(default='active')
    janela.bind('<Return>', lambda e: bt.invoke())
