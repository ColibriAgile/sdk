object formNotificacao: TformNotificacao
  Left = 0
  Top = 0
  Anchors = [akLeft]
  Caption = 'Notifica'#231#227'o de evento'
  ClientHeight = 461
  ClientWidth = 485
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Tahoma'
  Font.Style = []
  KeyPreview = True
  OldCreateOrder = False
  Position = poScreenCenter
  OnCreate = FormCreate
  OnKeyPress = FormKeyPress
  OnShow = FormShow
  DesignSize = (
    485
    461)
  PixelsPerInch = 96
  TextHeight = 13
  object Label1: TLabel
    Left = 16
    Top = 16
    Width = 24
    Height = 13
    Caption = 'Tipo:'
  end
  object edEvento: TEdit
    Left = 16
    Top = 40
    Width = 460
    Height = 21
    Anchors = [akLeft, akTop, akRight]
    ReadOnly = True
    TabOrder = 0
  end
  object Button1: TButton
    Left = 20
    Top = 428
    Width = 75
    Height = 25
    Anchors = [akLeft, akBottom]
    Caption = 'Copiar'
    TabOrder = 1
    OnClick = Button1Click
  end
  object Contin: TButton
    Left = 402
    Top = 428
    Width = 75
    Height = 25
    Anchors = [akRight, akBottom]
    Caption = 'Continuar'
    Default = True
    ModalResult = 1
    TabOrder = 2
  end
  object ckNaoExibir: TCheckBox
    Left = 16
    Top = 401
    Width = 193
    Height = 17
    Anchors = [akLeft, akBottom]
    Caption = 'N'#227'o exibir mais eventos desse tipo'
    TabOrder = 3
  end
  object Erro: TButton
    Left = 321
    Top = 428
    Width = 75
    Height = 25
    Anchors = [akRight, akBottom]
    Caption = 'Erro'
    TabOrder = 4
    OnClick = ErroClick
  end
  object PageControl1: TPageControl
    Left = 16
    Top = 67
    Width = 461
    Height = 328
    ActivePage = tabContexto
    Anchors = [akLeft, akTop, akRight, akBottom]
    TabOrder = 5
    object tabContexto: TTabSheet
      Caption = 'Contexto'
      object mmoContexto: TJvHLEditor
        AlignWithMargins = True
        Left = 3
        Top = 3
        Width = 447
        Height = 294
        Cursor = crIBeam
        BorderStyle = bsNone
        Lines.Strings = (
          '{'
          '    "monitor": true,'
          '    "devolver_impressao": true,'
          '    "configuracao": "TJSONObject",'
          '    "num": 11,'
          '    "col": 40,'
          '    "consumacao": 0,'
          '    "sistema": "NCR Colibri",'
          '    "total_da_conta": 6.5,'
          '    "txt_consumacao": "Consuma'#231#227'o",'
          '    "operador": "SUPER USUARIO",'
          '    "operacao": {'
          '      "consumidor": null,'
          '      "dataExpedicao": -2209154400000,'
          '      "totais": {'
          '        "taxaDeEntregaCalculada": 0,'
          '        "subtotalParaDesconto": 5,'
          '        "consumacao": 0,'
          '        "servicoInformado": -1,'
          '        "entradaMaxima": 0,'
          '        "desconto": 0,'
          '        "servico": 0.5,'
          '        "outros": 0,'
          '        "descontoInfo": {'
          '          "valores": null,'
          '          "percentual": 0,'
          '          "fixo": 0'
          '        },'
          '        "subtotal": 5,'
          '        "subtotalParaServico": 5,'
          '        "entrada": 0,'
          '        "troco": 0,'
          '        "total": 0,'
          '        "acrescimo": 0,'
          '        "taxaDeEntrega": 1,'
          '        "pago": 0,'
          '        "pctServico": 10,'
          '        "consumacaoMaxima": 0,'
          '        "diferencaDeConsumacao": 0,'
          '        "percentualDeDesconto": 0,'
          '        "taxaDeEntregaInformada": 1'
          '      },'
          '      "numeroDePessoas": 1,'
          '      "funcionarioExpedicao": null,'
          '      "itensDoMovimento": {'
          '        "itens": {'
          '          "itens": [],'
          '          "quantidade": 0'
          '        },'
          '        "tipodeItens": 1'
          '      },'
          '      "operacaoID": {'
          '        "valor": "9B5E36F6-7892-E411-BEBE-4C80935C7997"'
          '      },'
          '      "itensConsolidadosDaOperacao": {'
          '        "itens": ['
          '          {'
          '            "local_producao": 0,'
          '            "dummyalterado": 0,'
          '            "combo_id": 0,'
          '            "DataCancelamento": -2209154400000,'
          '            "ValorDoServico": 0.5,'
          '            "VendaDeOrigem": 0,'
          '            "Transferido": false,'
          '            "FuncionarioLancou": 1,'
          '            "Contador": 1,'
          '            "unidade": "UN    ",'
          '            "AceitaDesconto": true,'
          '            "canceladoAntesDaProducao": false,'
          '            "Impresso": true,'
          '            "permiteQtdFracionada": false,'
          '            "MotivoDeCancelamentoID": -1,'
          '            "LocalDeEntrega": "",'
          '            "id": 1,'
          '            "codigo": "1001",'
          '            "FuncionarioTransferiu": 0,'
          '            "DataLancamento": 1420200896000,'
          '            "ticketOrigem": "",'
          '            "quantidade": 1,'
          '            "canceladoDepoisDaProducao": false,'
          '            "cobraServico": true,'
          '            "Enviado": true,'
          '            "observacao": "",'
          '            "FuncionarioAutorizou": 0,'
          '            "descricao": "AGUA COM GAS",'
          '            "item_id": {'
          '              "valor": "750AE1A8-2A06-4EC1-A2A8-BFF6AAEB14BC"'
          '            },'
          '            "Indice": 1,'
          '            "preco": 5,'
          '            "FuncionarioCancelou": 0'
          '          }'
          '        ],'
          '        "quantidade": 1'
          '      },'
          '      "COOConferencia": 0,'
          '      "consumos": {'
          '        "itens": ['
          '          {'
          '            "_Flags": 0,'
          '            "venda": null,'
          '            "ticket": {'
          '              "DataDeAbertura": -2209154400000,'
          '              "localDeEntrega": "",'
          '              "percentualDeServico": 10,'
          '              "garcom": null,'
          '              "CodigoDoPai": 0,'
          '              "ticketPaiID": {'
          '                "valor": "00000000-0000-0000-0000-000000000000"'
          '              },'
          '              "venda": {'
          '                "nome_amigavel": "Ficha 7",'
          '                "subtotalParaDesconto": 5,'
          '                "VendaID": {'
          
            '                  "valor": "9C5E36F6-7892-E411-BEBE-4C80935C7997' +
            '"'
          '                },'
          '                "Transferida": false,'
          '                "FuncionarioQueAbriu": 0,'
          '                "operacaoIDOrigem": {'
          
            '                  "valor": "00000000-0000-0000-0000-000000000000' +
            '"'
          '                },'
          '                "NumeroDeFechamentos": 0,'
          '                "itens": {'
          '                  "itens": ['
          '                    {'
          '                      "local_producao": 0,'
          '                      "dummyalterado": 1,'
          '                      "combo_id": 0,'
          '                      "DataCancelamento": -2209154400000,'
          '                      "ValorDoServico": 0.5,'
          '                      "VendaDeOrigem": 0,'
          '                      "Transferido": false,'
          '                      "FuncionarioLancou": 1,'
          '                      "Contador": 1,'
          '                      "unidade": "UN    ",'
          '                      "AceitaDesconto": true,'
          '                      "canceladoAntesDaProducao": false,'
          '                      "Impresso": true,'
          '                      "permiteQtdFracionada": false,'
          '                      "MotivoDeCancelamentoID": -1,'
          '                      "LocalDeEntrega": "",'
          '                      "id": 1,'
          '                      "codigo": "1001",'
          '                      "FuncionarioTransferiu": 0,'
          '                      "DataLancamento": 1420200896000,'
          '                      "ticketOrigem": "",'
          '                      "quantidade": 1,'
          '                      "canceladoDepoisDaProducao": false,'
          '                      "cobraServico": true,'
          '                      "Enviado": true,'
          
            '                      "observacao": "com mostarda\r\nsem cebola"' +
            ','
          '                      "FuncionarioAutorizou": 0,'
          '                      "descricao": "AGUA COM GAS",'
          '                      "item_id": {'
          
            '                        "valor": "750AE1A8-2A06-4EC1-A2A8-BFF6AA' +
            'EB14BC"'
          '                      },'
          '                      "Indice": 1,'
          '                      "preco": 5,'
          '                      "FuncionarioCancelou": 0'
          '                    }'
          '                  ],'
          '                  "quantidade": 1'
          '                },'
          '                "operacaoID": {'
          
            '                  "valor": "9B5E36F6-7892-E411-BEBE-4C80935C7997' +
            '"'
          '                },'
          '                "subtotalDosItens": 5,'
          '                "NumeroDeChamada": 0,'
          '                "subtotalParaServico": 5,'
          '                "Cancelada": false,'
          '                "PerfilID": 0,'
          '                "data_abertura": 1420200896000,'
          '                "itensConsolidados": {'
          '                  "itens": ['
          '                    {'
          '                      "local_producao": 0,'
          '                      "dummyalterado": 0,'
          '                      "combo_id": 0,'
          '                      "DataCancelamento": -2209154400000,'
          '                      "ValorDoServico": 0.5,'
          '                      "VendaDeOrigem": 0,'
          '                      "Transferido": false,'
          '                      "FuncionarioLancou": 1,'
          '                      "Contador": 1,'
          '                      "unidade": "UN    ",'
          '                      "AceitaDesconto": true,'
          '                      "canceladoAntesDaProducao": false,'
          '                      "Impresso": true,'
          '                      "permiteQtdFracionada": false,'
          '                      "MotivoDeCancelamentoID": -1,'
          '                      "LocalDeEntrega": "",'
          '                      "id": 1,'
          '                      "codigo": "1001",'
          '                      "FuncionarioTransferiu": 0,'
          '                      "DataLancamento": 1420200896000,'
          '                      "ticketOrigem": "",'
          '                      "quantidade": 1,'
          '                      "canceladoDepoisDaProducao": false,'
          '                      "cobraServico": true,'
          '                      "Enviado": true,'
          '                      "observacao": "",'
          '                      "FuncionarioAutorizou": 0,'
          '                      "descricao": "AGUA COM GAS",'
          '                      "item_id": {'
          
            '                        "valor": "750AE1A8-2A06-4EC1-A2A8-BFF6AA' +
            'EB14BC"'
          '                      },'
          '                      "Indice": 1,'
          '                      "preco": 5,'
          '                      "FuncionarioCancelou": 0'
          '                    }'
          '                  ],'
          '                  "quantidade": 1'
          '                },'
          '                "numeroDaVenda": 45,'
          '                "codDoTicket": "7",'
          '                "LimiteDeConsumo": 0,'
          '                "ticketID": {'
          
            '                  "valor": "3A813A3A-FE00-E311-A612-782BCBBEF5EF' +
            '"'
          '                },'
          '                "observacao": "trazer card'#195#161'pio",'
          '                "cliente": {'
          
            '                  "valor": "00000000-0000-0000-0000-000000000000' +
            '"'
          '                }'
          '              },'
          '              "ModoDeVenda": 4,'
          '              "PerfilID": 0,'
          '              "codigo": 7,'
          '              "estado": "consumindo",'
          '              "codigoBarra": "\u00007",'
          '              "nome": "ficha 7",'
          '              "apelido": "",'
          '              "vendaID": {'
          '                "valor": "9C5E36F6-7892-E411-BEBE-4C80935C7997"'
          '              },'
          '              "LimiteDeConsumo": 0,'
          '              "ticketID": {'
          '                "valor": "3A813A3A-FE00-E311-A612-782BCBBEF5EF"'
          '              },'
          '              "cliente": null,'
          '              "ativo": true,'
          '              "praca": 0'
          '            }'
          '          }'
          '        ],'
          '        "quantidade": 1'
          '      },'
          '      "troco": {'
          '        "valorMaximoEmContraVale": 0,'
          '        "formasDisponiveis": 0,'
          '        "valorMaximoEmRepique": 0,'
          '        "repique": 0,'
          '        "valorMaximoEmDinheiro": 0,'
          '        "contraVale": 0,'
          '        "dinheiro": 0,'
          '        "totalDoTroco": 0'
          '      },'
          '      "entregador": null,'
          '      "ECFConferencia": 0,'
          '      "descricao": ""'
          '    },'
          '    "versao": "1.0.1.12",'
          '    "garcom": "SUPER USUARIO",'
          '    "gerencial": "Conf. de conta",'
          '    "pgtoparciais": {'
          '      "itens": {'
          '        "itens": [],'
          '        "quantidade": 0'
          '      },'
          '      "tipodeItens": 1'
          '    },'
          '    "desconto": 0,'
          '    "servico": 0.5,'
          '    "maquina": "MATRIX-NOTE",'
          '    "subtotal_da_operacao": 5,'
          '    "UF": "SP",'
          '    "entrega": 1,'
          '    "entrada": 0,'
          '    "txt_servico": "Servi'#231'o",'
          '    "dataContabil": "14/08/14",'
          '    "numero": 1,'
          '    "saldo": 6.5,'
          '    "selecao": "*sem filtro*",'
          '    "loja": "CIRQUE DU SOLEIL",'
          '    "hora": "10:15",'
          '    "data": "02/01/15",'
          '    "relatorio_id": "1/11",'
          '    "movimento": "14/08/14",'
          '    "aplicativo": "colibriServer",'
          '    "operacao_id": "{9B5E36F6-7892-E411-BEBE-4C80935C7997}",'
          '    "pagoParcial": 0,'
          '    "diasemana": "sexta-feira",'
          '    "txt_entrega": "Entrega",'
          '    "txt_entrada": "Entrada"'
          ' }')
        ReadOnly = True
        Completion.ItemHeight = 13
        Completion.CRLF = '/n'
        Completion.Separator = '='
        TabStops = '3 5'
        BracketHighlighting.Active = True
        BracketHighlighting.BorderColor = clNone
        BracketHighlighting.Color = clYellow
        BracketHighlighting.FontColor = clBlack
        BracketHighlighting.WordPairs.Strings = (
          '{=}'
          '[=]')
        BracketHighlighting.StringEscape = #39#39
        Align = alClient
        Color = 3223859
        Font.Charset = DEFAULT_CHARSET
        Font.Color = clWindowText
        Font.Height = -13
        Font.Name = 'Consolas'
        Font.Style = []
        Highlighter = hlJScript
        Colors.Comment.Style = [fsItalic]
        Colors.Comment.ForeColor = clNavy
        Colors.Comment.BackColor = 3354929
        Colors.Number.ForeColor = clWhite
        Colors.Number.BackColor = 3354929
        Colors.Strings.ForeColor = 6721187
        Colors.Strings.BackColor = 3354929
        Colors.Symbol.ForeColor = clWhite
        Colors.Symbol.BackColor = 3354929
        Colors.Reserved.Style = [fsBold]
        Colors.Reserved.ForeColor = 4164298
        Colors.Reserved.BackColor = 3354929
        Colors.Identifier.ForeColor = clBlack
        Colors.Identifier.BackColor = 3354929
        Colors.Preproc.ForeColor = clGreen
        Colors.Preproc.BackColor = 3354929
        Colors.FunctionCall.ForeColor = clWindowText
        Colors.FunctionCall.BackColor = 3354929
        Colors.Declaration.ForeColor = clWindowText
        Colors.Declaration.BackColor = 3354929
        Colors.Statement.Style = [fsBold]
        Colors.Statement.ForeColor = clWindowText
        Colors.Statement.BackColor = 3354929
        Colors.PlainText.ForeColor = clWindowText
        Colors.PlainText.BackColor = 3354929
      end
    end
    object tabModificadores: TTabSheet
      Caption = 'Modificadores'
      ImageIndex = 1
      object Panel1: TPanel
        Left = 0
        Top = 259
        Width = 453
        Height = 41
        Align = alBottom
        TabOrder = 0
        object btnPrepMod: TButton
          Left = 3
          Top = 3
          Width = 166
          Height = 25
          Caption = 'Montar modificadores'
          TabOrder = 0
          OnClick = btnPrepModClick
        end
      end
      object mmoModificadores: TJvHLEditor
        AlignWithMargins = True
        Left = 3
        Top = 3
        Width = 447
        Height = 253
        Cursor = crIBeam
        BorderStyle = bsNone
        Completion.ItemHeight = 13
        Completion.CRLF = '/n'
        Completion.Separator = '='
        TabStops = '3 5'
        BracketHighlighting.Active = True
        BracketHighlighting.BorderColor = clNone
        BracketHighlighting.Color = clYellow
        BracketHighlighting.FontColor = clBlack
        BracketHighlighting.WordPairs.Strings = (
          '{=}'
          '[=]')
        BracketHighlighting.StringEscape = #39#39
        Align = alClient
        Color = 3223859
        Font.Charset = DEFAULT_CHARSET
        Font.Color = clWindowText
        Font.Height = -13
        Font.Name = 'Consolas'
        Font.Style = []
        Highlighter = hlJScript
        Colors.Comment.Style = [fsItalic]
        Colors.Comment.ForeColor = clNavy
        Colors.Comment.BackColor = 3354929
        Colors.Number.ForeColor = clWhite
        Colors.Number.BackColor = 3354929
        Colors.Strings.ForeColor = 6721187
        Colors.Strings.BackColor = 3354929
        Colors.Symbol.ForeColor = clWhite
        Colors.Symbol.BackColor = 3354929
        Colors.Reserved.Style = [fsBold]
        Colors.Reserved.ForeColor = 4164298
        Colors.Reserved.BackColor = 3354929
        Colors.Identifier.ForeColor = clBlack
        Colors.Identifier.BackColor = 3354929
        Colors.Preproc.ForeColor = clGreen
        Colors.Preproc.BackColor = 3354929
        Colors.FunctionCall.ForeColor = clWindowText
        Colors.FunctionCall.BackColor = 3354929
        Colors.Declaration.ForeColor = clWindowText
        Colors.Declaration.BackColor = 3354929
        Colors.Statement.Style = [fsBold]
        Colors.Statement.ForeColor = clWindowText
        Colors.Statement.BackColor = 3354929
        Colors.PlainText.ForeColor = clWindowText
        Colors.PlainText.BackColor = 3354929
      end
    end
  end
  object JvFormStorage1: TJvFormStorage
    AppStorage = JvAppIniFileStorage1
    AppStoragePath = '%FORM_NAME%\'
    StoredValues = <>
    Left = 224
    Top = 408
  end
  object JvAppIniFileStorage1: TJvAppIniFileStorage
    StorageOptions.BooleanStringTrueValues = 'TRUE, YES, Y'
    StorageOptions.BooleanStringFalseValues = 'FALSE, NO, N'
    FileName = 'bin\plugins\contexto\contexto.ini'
    Location = flCustom
    DefaultSection = 'padrao'
    SubStorages = <>
    Left = 264
    Top = 408
  end
end
