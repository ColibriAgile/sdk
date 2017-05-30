unit plugin.api;

interface

type
  // Ponteiros de fun��o
  ProcAssinarEvento = procedure (umPlugin, umEvento: PChar); stdcall;
  ProcCallBack = procedure(umPlugin, umEvento, umContexto: PChar); stdcall;
  ProcAlocarBuffer = function(Buffer: PChar): PChar; stdcall;
  ProcGravarConfig =  procedure(umPlugin, umaConfig: PChar; umaMaquina:Integer; umValor: PChar=nil); stdcall;
  ProcLiberarBuffer = procedure(Buffer: PChar);stdcall;
  ProcObterConfigs = function(umPlugin:PChar; umaMaquina:Integer): Pchar; stdcall;
  ProcObterFuncao = function (nomeFuncao: PChar):Pointer; stdcall;
  ProcMostrarMensagem = function(plugin, dados:PChar): Integer; stdcall;
  ProcMostrarTeclado = function(plugin, dados:PChar): PChar; stdcall;

  // Fun��es Exportadas da DLL
  function ObterDadosFabricante(): PChar; stdcall;
  procedure Ativar(umaMaquina:Integer); stdcall; export;
  procedure AtribuirObtencaoDeFuncoes(_ObterFuncao: ProcObterFuncao); stdcall; export;
  procedure Configurar(dictMaquinas:PChar); stdcall; export;
  procedure ConfigurarDB (const umServidor, umBanco, umUsuario, umaSenha, umProvedor: PChar); stdcall;
  procedure Desativar(umaMaquina:Integer); stdcall; export;
const
  FABRICANTE =
   '{"fabricante":{' +
       '"empresa":"Empresa",' +
       '"desenvolvedor":"Equipe",' +
       '"termos_da_licenca":"",' +
       '"direitos_de_copia":"",' +
       '"marcas_registradas":""' +
    '}, "suporte":{' +
       '"email":"suporte@empresa.com",' +
       '"url":"",' +
       '"telefone":"(99)9999-9999"' +
    '}}';
  function Notificar(evento, contexto: PChar): PChar; stdcall;
  function ObterMacro (umaMacro: PChar): PChar; stdcall;
  function ObterNome(): PChar; stdcall;
  function ObterVersao(): PChar; stdcall;
  procedure RegistrarAssinaturas(AssinarEvento: ProcAssinarEvento); stdcall; export;
  function VerificarVersao(informacao:PChar): PChar; stdcall; export;

var
  ObterFuncao: ProcObterFuncao;
  AlocarBuffer: ProcAlocarBuffer;
  LiberarBuffer: ProcLiberarBuffer;
  CallBack: ProcCallBack;
  ObterConfigs: ProcObterConfigs;
  GravarConfig: ProcGravarConfig;
  MostrarMensagem: ProcMostrarMensagem;
  MostrarTeclado: ProcMostrarTeclado;


implementation

uses
  System.Classes,
  Winapi.Windows,
  system.SysUtils,
  form.config;


function Notificar(evento, contexto: PChar): PChar;
begin
  Result := AlocarBuffer(PChar(''));
end;

function ObterVersao(): PChar; stdcall; export;
begin
  Result := AlocarBuffer(PChar('1.0.0.0'));
end;

function ObterNome(): PChar; stdcall; export;
begin
  Result := AlocarBuffer(PChar('plugin.delphi'));
end;


function ObterDadosFabricante(): PChar; stdcall; export;
begin
    Result := AlocarBuffer(PChar(FABRICANTE));
end;
procedure RegistrarAssinaturas(AssinarEvento: ProcAssinarEvento); stdcall; export;
begin
  // Este evento � gerado por �tens de interface (menu, bot�es) adicionados via ui.config
  AssinarEvento('plugin.delphi', PChar('EventoDeUIDePlugin.FuncaoNoPlugin'));
end;

procedure AtribuirObtencaoDeFuncoes(_ObterFuncao: ProcObterFuncao); stdcall; export;
begin
  ObterFuncao := _ObterFuncao;
  AlocarBuffer := ProcAlocarBuffer(ObterFuncao('AlocarBuffer'));
  LiberarBuffer := ProcLiberarBuffer(ObterFuncao('LiberarBuffer'));
  CallBack := ProcCallBack(ObterFuncao('CallBack'));
  ObterConfigs := ProcObterConfigs(ObterFuncao('ObterConfigs'));
  GravarConfig := ProcGravarConfig(ObterFuncao('GravarConfig'));
  MostrarMensagem := ProcMostrarMensagem(ObterFuncao('MostrarMensagem'));
  MostrarTeclado := ProcMostrarTeclado(ObterFuncao('MostrarTeclado'));
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

function VerificarVersao(informacao:PChar): PChar; export;
begin
  Result := AlocarBuffer('');
end;

procedure ConfigurarDB (const umServidor, umBanco, umUsuario, umaSenha, umProvedor: PChar); stdcall;
begin

end;

function ObterMacro (umaMacro: PChar): PChar; stdcall;
begin
  if umaMacro = 'Teste'  then
    Result := AlocarBuffer(PChar('{"valor":"ValorMacroTeste"}'))
  else
    Result := AlocarBuffer(PChar(Format('{"erro":"Macro desconhecida: %s"}', [umaMacro])))
end;


end.
