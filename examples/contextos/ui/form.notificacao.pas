unit form.notificacao;

interface

uses
  Winapi.Windows,
  Winapi.Messages,
  System.SysUtils,
  System.Variants,
  System.Classes,
  ClipBrd,
  Vcl.Graphics,
  Vcl.Controls,
  Vcl.Forms,
  Vcl.Dialogs,
  JvExControls,
  JvEditorCommon,
  JvEditor,
  JvHLEditor,
  Vcl.StdCtrls,
  Vcl.ExtCtrls,
  Vcl.ComCtrls,
  suporte.superobj,
  form.mensagemerro,
  JvAppStorage,
  JvAppIniStorage,
  JvComponentBase,
  JvFormPlacement,
  plugin.api;

type
  TformNotificacao = class(TForm)
    Label1: TLabel;
    edEvento: TEdit;
    Button1: TButton;
    Contin: TButton;
    ckNaoExibir: TCheckBox;
    Erro: TButton;
    PageControl1: TPageControl;
    tabContexto: TTabSheet;
    tabModificadores: TTabSheet;
    mmoContexto: TJvHLEditor;
    Panel1: TPanel;
    btnPrepMod: TButton;
    mmoModificadores: TJvHLEditor;
    JvFormStorage1: TJvFormStorage;
    JvAppIniFileStorage1: TJvAppIniFileStorage;
    procedure Button1Click(Sender: TObject);
    procedure ErroClick(Sender: TObject);
    procedure btnPrepModClick(Sender: TObject);
    procedure FormShow(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure FormKeyPress(Sender: TObject; var Key: Char);
  private
    { Private declarations }
    mensagemErro: string;
    acao: string;
  public
    { Public declarations }
    class function Executar(evento, contexto:string;out erro, modificadores, acao: string; out naoExibir:Boolean): Integer;
  end;

var
  formNotificacao: TformNotificacao;

implementation

{$R *.dfm}

procedure TformNotificacao.btnPrepModClick(Sender: TObject);
var
  obj, mods : ISuperObject;
begin
  obj := SO(mmoContexto.Lines.Text);
  mods:= obj.O['modificadores'];
  if not Assigned(mods) then
  begin
    MessageBox(Handle,'Contexto não possui modificadores', 'Erro', mrOk);
    Exit;
  end;
  // Monto um contexto apenas com os modificadores
  obj := SO('{"modificadores":{}}');
  obj.O['modificadores'] := mods;
  mmoModificadores.Lines.Text := obj.AsJson(True);
end;

procedure TformNotificacao.Button1Click(Sender: TObject);
begin
  Clipboard.AsText := mmoContexto.Lines.GetText;
end;

procedure TformNotificacao.ErroClick(Sender: TObject);
var
  form: TformMensagemErro;
  modalRes: Integer;
begin
  form := TformMensagemErro.Create(nil);
  try
    modalRes:= form.ShowModal();
    if modalRes = mrOk then
    begin
      mensagemErro := form.memoErro.Lines.Text;
      ModalResult := mrCancel;
    end
    else if modalRes = mrAbort then
    begin
      mensagemErro := form.memoErro.Lines.Text;
      acao := 'abort';
      ModalResult := mrAbort;
    end
  finally
    FreeAndNil(form);
  end;
end;

class function TformNotificacao.Executar(evento, contexto:string;out erro, modificadores, acao: string; out naoExibir:Boolean): Integer;
var
  form: TformNotificacao;
begin
  form := TformNotificacao.Create(nil);
  form.edEvento.Text := evento;
  form.mmoContexto.Lines.Text := contexto;
  try
    Result := form.ShowModal();
    erro := form.mensagemErro;
    modificadores := form.mmoModificadores.Lines.Text;
    naoExibir := form.ckNaoExibir.Checked;
    acao := form.acao;
  finally
    FreeAndNil(form);
  end;
end;


procedure TformNotificacao.FormCreate(Sender: TObject);
begin
  JvAppIniFileStorage1.FileName := IncludeTrailingPathDelimiter(ObterCaminhoDoPlugin()) + 'contextos.ini';
end;

procedure TformNotificacao.FormKeyPress(Sender: TObject; var Key: Char);
begin
  if (key = #27)  then
    ModalResult := mrCancel
  else
    inherited;
end;

procedure TformNotificacao.FormShow(Sender: TObject);
begin
  PageControl1.TabIndex := 0;
end;

end.
