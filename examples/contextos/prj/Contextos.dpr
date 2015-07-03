library Contextos;

uses
  IOutils,
  System.SysUtils,
  winapi.windows,
{$ifdef USAR_CODESITE}
  logs.codesite,
{$endif}
  plugin.api in '..\src\plugin.api.pas',
  form.config in '..\ui\form.config.pas' {frmConfig},
  form.notificacao in '..\ui\form.notificacao.pas' {formNotificacao},
  form.mensagemerro in '..\ui\form.mensagemerro.pas' {formMensagemErro};

{$E col}
{$R *.res}
{$DEFINE DEBUGVIEW}


exports
  Ativar,
  AtribuirObtencaoDeFuncoes,
  Atualizar,
  Configurar,
  ConfigurarDB,
  Desativar,
  Notificar,
  ObterErro,
  ObterMacro,
  ObterNome,
  ObterVersao,
  RegistrarAssinaturas,
  VerificarVersao;

var
  SaveDllProc: Pointer;

procedure Init_Destroy(Reason: Integer);
begin
  if Reason = DLL_PROCESS_DETACH then
  begin
    DllProc := SaveDllProc;
  end;
end;

begin
end.


