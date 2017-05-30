library DelphiXE;

uses
  IOutils,
  System.SysUtils,
  winapi.windows,
  plugin.api in '..\src\plugin.api.pas',
  form.config in '..\ui\form.config.pas' {frmConfig};

{$E col}
{$R *.res}
{$DEFINE DEBUGVIEW}


exports
  Ativar,
  AtribuirObtencaoDeFuncoes,
  Configurar,
  ConfigurarDB,
  Desativar,
  Notificar,
  ObterDadosFabricante,
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


