object frmConfig: TfrmConfig
  Left = 0
  Top = 0
  BorderStyle = bsDialog
  Caption = 'Parametriza'#231#227'o do Plugin'
  ClientHeight = 174
  ClientWidth = 297
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Segoe UI'
  Font.Style = []
  OldCreateOrder = False
  Position = poOwnerFormCenter
  PixelsPerInch = 96
  TextHeight = 13
  object btOK: TButton
    Left = 51
    Top = 136
    Width = 75
    Height = 25
    Caption = '&Aplicar'
    ModalResult = 1
    TabOrder = 0
  end
  object btCancel: TButton
    Left = 187
    Top = 136
    Width = 75
    Height = 25
    Caption = '&Fechar'
    TabOrder = 1
    OnClick = btCancelClick
  end
end
