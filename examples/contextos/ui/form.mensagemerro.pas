unit form.mensagemerro;

interface

uses
  Winapi.Windows, Winapi.Messages, System.SysUtils, System.Variants, System.Classes, Vcl.Graphics,
  Vcl.Controls, Vcl.Forms, Vcl.Dialogs, Vcl.StdCtrls;

type
  TformMensagemErro = class(TForm)
    Label1: TLabel;
    memoErro: TMemo;
    Button1: TButton;
    Button2: TButton;
    Button3: TButton;
    procedure FormShow(Sender: TObject);
    procedure Button2Click(Sender: TObject);
    procedure Button3Click(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  formMensagemErro: TformMensagemErro;

implementation

{$R *.dfm}

procedure TformMensagemErro.Button2Click(Sender: TObject);
begin
  if Length(memoErro.Lines.Text) > 0 then
    ModalResult := mrOk
  else
    MessageBox(Handle,'Forneça uma mensagem de erro', 'Erro', mrOk);
end;

procedure TformMensagemErro.Button3Click(Sender: TObject);
begin
  ModalResult := mrAbort;
end;

procedure TformMensagemErro.FormShow(Sender: TObject);
begin
  memoErro.SelectAll;
end;

end.
