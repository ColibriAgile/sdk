object formMensagemErro: TformMensagemErro
  Left = 0
  Top = 0
  ActiveControl = memoErro
  BorderStyle = bsDialog
  Caption = 'Mensagem de erro'
  ClientHeight = 124
  ClientWidth = 466
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Tahoma'
  Font.Style = []
  OldCreateOrder = False
  Position = poScreenCenter
  OnShow = FormShow
  PixelsPerInch = 96
  TextHeight = 13
  object Label1: TLabel
    Left = 8
    Top = 8
    Width = 132
    Height = 13
    Caption = 'Digite a mensagem de erro:'
  end
  object memoErro: TMemo
    Left = 8
    Top = 27
    Width = 449
    Height = 54
    Lines.Strings = (
      'Mensagem de erro de teste')
    TabOrder = 0
  end
  object Button1: TButton
    Left = 8
    Top = 87
    Width = 105
    Height = 25
    Caption = 'Voltar'
    ModalResult = 2
    TabOrder = 1
  end
  object Button2: TButton
    Left = 352
    Top = 87
    Width = 105
    Height = 25
    Caption = 'Retornar erro'
    Default = True
    TabOrder = 3
    OnClick = Button2Click
  end
  object Button3: TButton
    Left = 160
    Top = 87
    Width = 129
    Height = 25
    Caption = 'Interromper notifica'#231#227'o'
    TabOrder = 2
    OnClick = Button3Click
  end
end
