# coding: utf-8
import win32con
import win32ui
from pywin.mfc import dialog


ID_BTNOK = 12
ID_BTNCANCELAR = 13
ID_MESA = 14
ID_MENSAGEM = 15


class DlgLiberaMesa(dialog.Dialog):

    TITULO = u"Liberação de mesas"

    @classmethod
    def template_dlg_cfg(cls):
        style = win32con.DS_MODALFRAME | win32con.WS_POPUP | \
            win32con.WS_VISIBLE | win32con.WS_CAPTION | \
            win32con.WS_SYSMENU | win32con.DS_SETFONT

        visible = win32con.WS_CHILD | win32con.WS_VISIBLE
        tcs = visible | win32con.WS_TABSTOP
        static = visible | win32con.SS_LEFT
        edt = tcs | win32con.ES_AUTOHSCROLL | win32con.ES_LEFT | win32con.WS_BORDER
        btn = tcs | win32con.BS_VCENTER | win32con.BS_CENTER

        dlg = [
            [cls.TITULO, (0, 0, 187, 118), style, win32con.WS_EX_TOPMOST, (10, "Segoe UI")],
            ["STATIC", u"Liberar mesa:", -1,
                (15, 10, 133, 7), static],

            ["EDIT", u"", ID_MESA, (15, 20, 154, 14), edt],
            ["STATIC", u"", ID_MENSAGEM, (15, 35, 154, 50), static],
            ["BUTTON", u"&Ok", ID_BTNOK,
                (118, 92, 50, 14), btn | win32con.BS_DEFPUSHBUTTON],
            ["BUTTON", u"&Cancelar", ID_BTNCANCELAR, (65, 92, 50, 14), btn]
        ]

        return dlg

    def __init__(self):
        self.retorno = None
        dialog.Dialog.__init__(self, self.template_dlg_cfg())
        self.HookCommand(self.click_ok, ID_BTNOK)
        self.HookCommand(self.click_cancelar, ID_BTNCANCELAR)

    def OnInitDialog(self):
        rc = dialog.Dialog.OnInitDialog(self)
        self.butOK = self.GetDlgItem(ID_BTNOK)
        self.butCancel = self.GetDlgItem(ID_BTNCANCELAR)
        self.edtMensagem = self.GetDlgItem(ID_MENSAGEM)
        self.edtMesa = self.GetDlgItem(ID_MESA)

        return rc

    def click_ok(self, id, code):
        try:
            self.retorno = int(self.edtMesa.GetWindowText())
            self.EndDialog(win32con.IDCANCEL)
        except Exception as e:
            self.MessageBox(e.message, 'Erro!', win32con.MB_OK)

    def click_cancelar(self, id, code):
        self.EndDialog(win32con.IDCANCEL)


def configs_property_page():
    page1 = dialog.PropertyPage(win32ui.LoadDialogResource(win32ui.IDD_PROPDEMO1))
    page2 = dialog.PropertyPage(win32ui.LoadDialogResource(win32ui.IDD_PROPDEMO2))
    ps = dialog.PropertySheet('Property Sheet/Page Demo', None, [page1, page2])
    ps.DoModal()


if __name__ == '__main__':
    d = DlgLiberaMesa()
    d.DoModal()
