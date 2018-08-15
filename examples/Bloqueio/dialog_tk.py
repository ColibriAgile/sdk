# coding: utf-8
try:
    from tkinter import Tk, Label, Button, mainloop, Entry
    from tkinter.messagebox import showwarning
except ImportError:
    raise ImportError("tkinter")
from .colibri_gui import tk_como_modal, tk_botao_default, FW_COLIBRI_CONFIG

LETRA = "Verdana 12"


def dlg_filho_da_main():
    dlg = Tk()
    tk_como_modal(dlg, FW_COLIBRI_CONFIG)
    dlg.mainloop()


def liberar_mesa(pergunta=u"Mesa a liberar"):
    retorno = [None]

    jan = Tk()
    """
    Preparo a janela principal e a atual para
        agir como modal
    """
    tk_como_modal(jan)
    jan.title("Digite a mesa")
    jan.attributes("-toolwindow", 1)

    # Widgets
    Label(jan, text=pergunta, font=LETRA).pack()

    edt_mesa = Entry(jan, font=LETRA)
    edt_mesa.pack(padx=5)


    def resultado(event=None):
        try:
            retorno[0] = int(edt_mesa.get())
            jan.destroy()
        except ValueError:
            showwarning("Erro!", "Mesa inválida: " + edt_mesa.get())

    bt = Button(jan, text="OK", command=resultado, font=LETRA)
    tk_botao_default(jan, bt)
    bt.pack(pady=5)

    jan.resizable(width=False, height=False)
    jan.geometry('+%d+%d' % (500, 400))
    edt_mesa.focus_force()
    mainloop()
    return retorno[0]

if __name__ == '__main__':
    import threading
    t = threading.Thread(target=liberar_mesa)
    t.start()
    t.join()
