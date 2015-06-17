unit plugin.api;

interface

type
  // Ponteiros de função
  ProcCallBack = procedure(umPlugin, umTipo, umValor: PChar); stdcall;
  ProcObterConfigs = function(umPlugin:PChar; umaMaquina:Integer): Pchar; stdcall;
  ProcGravarConfig =  procedure(umPlugin, umaConfig: PChar; global:Integer; umValor: PChar=nil); stdcall;
  ProcCopiarBuffer = function(Buffer: PChar): PChar;stdcall;
  ProcLiberarBuffer = procedure(Buffer: PChar);stdcall;
  ProcAssinarEvento = procedure (umPlugin, umIdentificador: PChar); stdcall;
  ProcObterFuncao = function (nomeCallBack: PChar):Pointer; stdcall;

  // Funções Exportadas da DLL
  function Atualizar(var retorno: PChar): Integer; stdcall;
  function Notificar(evento, informacao: PChar; var retorno: PChar): Integer; stdcall;
  function ObterErro(): PChar; stdcall; export;
  function ObterNome(): PChar; stdcall;
  function ObterVersao(): PChar; stdcall;
  procedure Ativar(umaMaquina:Integer); stdcall; export;
  procedure AtribuirObtencaoDeFuncoes(_ObterFuncao: ProcObterFuncao); stdcall; export;
  procedure Configurar(dictMaquinas:PChar); stdcall; export;
  procedure ConfigurarDB (const umServidor, umBanco, umUsuario, umaSenha, umProvedor: PChar); stdcall;
  procedure Desativar(umaMaquina:Integer); stdcall; export;
  procedure RegistrarAssinaturas(AssinarEvento: ProcAssinarEvento); stdcall; export;
  function ObterMacro (umaMacro: PChar): PChar; stdcall;
  function VerificarVersao(informacao:PChar): PChar; stdcall; export;

var
  ObterFuncao: ProcObterFuncao;
  CopiarBuffer: ProcCopiarBuffer;
  LiberarBuffer: ProcLiberarBuffer;
  CallBack: ProcCallBack;
  ObterConfigs: ProcObterConfigs;
  GravarConfig: ProcGravarConfig;


implementation

uses
  System.Classes,
  Winapi.Windows,
  system.SysUtils,
  form.config;


function Notificar(evento, informacao: PChar; var retorno: PChar): Integer;
begin
  retorno := nil;
  Result := 1;
end;

function ObterVersao(): PChar; stdcall; export;
begin
  Result := CopiarBuffer(PChar('1.0.0.0'));
end;

function ObterNome(): PChar; stdcall; export;
begin
  Result := CopiarBuffer(PChar('plugin.delphi'));
end;

procedure RegistrarAssinaturas(AssinarEvento: ProcAssinarEvento); stdcall; export;
begin
  // Assina os eventos que deseja receber

  // Este evento é gerado por ítens de interface (menu, botões) adicionados via ui.config
  AssinarEvento('plugin.delphi', PChar('EventoDeUIDePlugin.FuncaoNoPlugin'));
end;

function ObterErro(): PChar; stdcall; export;
begin
  Result := CopiarBuffer('');
end;

procedure AtribuirObtencaoDeFuncoes(_ObterFuncao: ProcObterFuncao); stdcall; export;
begin
  ObterFuncao := _ObterFuncao;
  CopiarBuffer := ProcCopiarBuffer(ObterFuncao('CopiarBuffer'));
  LiberarBuffer := ProcLiberarBuffer(ObterFuncao('LiberarBuffer'));
  CallBack := ProcCallBack(ObterFuncao('CallBack'));
  ObterConfigs := ProcObterConfigs(ObterFuncao('ObterConfigs'));
  GravarConfig := ProcGravarConfig(ObterFuncao('GravarConfig'));
end;

procedure Ativar(umaMaquina:Integer); stdcall; export;
begin

end;

procedure Desativar(umaMaquina:Integer); stdcall; export;
begin

end;

procedure Configurar(dictMaquinas:PChar); stdcall; export;
begin
  TfrmConfig.Executar(dictMaquinas);
end;

function Atualizar(var retorno: PChar): Integer;
begin
  retorno := nil;
  Result := 1;
end;

function VerificarVersao(informacao:PChar): PChar; export;
begin
  Result := CopiarBuffer('');
end;

procedure ConfigurarDB (const umServidor, umBanco, umUsuario, umaSenha, umProvedor: PChar); stdcall;
begin

end;

function ObterMacro (umaMacro: PChar): PChar; stdcall;
begin
  Result := nil;
end;


end.
