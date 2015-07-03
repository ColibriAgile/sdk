object frmConfig: TfrmConfig
  Left = 0
  Top = 0
  BorderStyle = bsDialog
  Caption = 'Monitor de eventos e contextos'
  ClientHeight = 472
  ClientWidth = 560
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Segoe UI'
  Font.Style = []
  OldCreateOrder = False
  Position = poOwnerFormCenter
  OnDestroy = FormDestroy
  OnShow = FormShow
  DesignSize = (
    560
    472)
  PixelsPerInch = 96
  TextHeight = 13
  object Label1: TLabel
    Left = 8
    Top = 8
    Width = 319
    Height = 13
    Caption = 'Selecione os eventos que deseja monitorar e clique em Aplicar'
  end
  object btOK: TButton
    Left = 373
    Top = 439
    Width = 75
    Height = 25
    Caption = '&Aplicar'
    TabOrder = 3
    OnClick = btOKClick
  end
  object btCancel: TButton
    Left = 477
    Top = 439
    Width = 75
    Height = 25
    Caption = '&Fechar'
    ModalResult = 2
    TabOrder = 4
  end
  object Button1: TButton
    Left = 8
    Top = 439
    Width = 97
    Height = 25
    Caption = 'Marcar todos'
    TabOrder = 1
    OnClick = Button1Click
  end
  object Button2: TButton
    Left = 111
    Top = 439
    Width = 106
    Height = 25
    Caption = 'Desmarcar todos'
    TabOrder = 2
    OnClick = Button2Click
  end
  object ckMostrarNotificacao: TCheckBox
    Left = 8
    Top = 407
    Width = 132
    Height = 17
    Caption = 'Mostrar Notifica'#231#227'o'
    TabOrder = 0
  end
  object checkTree: TJvCheckTreeView
    Left = 8
    Top = 27
    Width = 544
    Height = 374
    Anchors = [akLeft, akTop, akRight, akBottom]
    Indent = 19
    TabOrder = 5
    LineColor = clScrollBar
    Checkboxes = True
    CheckBoxOptions.Style = cbsJVCL
    CheckBoxOptions.CascadeLevels = -1
  end
end
