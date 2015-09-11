unit plugin.api;

interface

type
  // Ponteiros de função
  ProcAssinarEvento = procedure (umPlugin, umIdentificador: PChar); stdcall;
  ProcCallBack = procedure(umPlugin, umTipo, umValor: PChar); stdcall;
  ProcAlocarBuffer = function(Buffer: PChar): PChar; stdcall;
  ProcGravarConfig =  procedure(umPlugin, umaConfig: PChar; umaMaquina:Integer; umValor: PChar=nil); stdcall;
  ProcLiberarBuffer = procedure(Buffer: PChar);stdcall;
  ProcObterConfigs = function(umPlugin:PChar; umaMaquina:Integer): Pchar; stdcall;
  ProcObterFuncao = function (nomeFuncao: PChar):Pointer; stdcall;

  // Funções Exportadas da DLL
  function ObterDadosFabricante(): PChar; stdcall;
  procedure Ativar(umaMaquina:Integer); stdcall; export;
  procedure AtribuirObtencaoDeFuncoes(_ObterFuncao: ProcObterFuncao); stdcall; export;
  function Atualizar(): PChar; stdcall;
  procedure Configurar(dictMaquinas:PChar); stdcall; export;
  procedure ConfigurarDB (const umServidor, umBanco, umUsuario, umaSenha, umProvedor: PChar); stdcall;
  procedure Desativar(umaMaquina:Integer); stdcall; export;
const
  FABRICANTE =
   '{"fabricante":{' +
       '"empresa":"NCR Corporation",' +
       '"desenvolvedor":"Equipe Colibri Agile",' +
       '"termos_da_licenca":"",' +
       '"direitos_de_copia":"",' +
       '"marcas_registradas":"Colibri® é marca registrada da NCR Corporation"' +
    '}, "suporte":{' +
       '"email":"suporte.canais@ncr.com",' +
       '"url":"",' +
       '"telefone":"(11)3323-3731"' +
    '}}';
  function Notificar(evento, informacao: PChar): PChar; stdcall;
  function ObterMacro (umaMacro: PChar): PChar; stdcall;
  function ObterNome(): PChar; stdcall;
  function ObterVersao(): PChar; stdcall;
  procedure RegistrarAssinaturas(AssinarEvento: ProcAssinarEvento); stdcall; export;
  function VerificarVersao(informacao:PChar): PChar; stdcall; export;

  // Não exportadas
  function ObterCaminhoDoPlugin: string;

var
  ObterFuncao: ProcObterFuncao;
  AlocarBuffer: ProcAlocarBuffer;
  LiberarBuffer: ProcLiberarBuffer;
  CallBack: ProcCallBack;
  ObterConfigs: ProcObterConfigs;
  GravarConfig: ProcGravarConfig;

const
  LOG_SESSAO = 'plugin.contextos';
  NOME_PLUGIN = 'plugin.contextos';

implementation

uses
  System.Classes,
  Winapi.Windows,
  system.SysUtils,
  suporte.superobj,
{$ifdef USAR_CODESITE}
  suporte.log,
{$endif}
  System.StrUtils,
  System.IOUtils,
  form.config,
  form.notificacao;

var
  params : ISuperObject;
  mostrarNotificacao: Boolean;
  ListaNaoExibir: TStringList;
{$ifndef USAR_CODESITE}
  LogFilename: string;
{$endif}

function Notificar(evento, informacao: PChar): PChar;
var
  stringList: TStringList;
  modificadores: string;
  naoExibir: Boolean;
  ultimoErro: string;
  acao: string;
  resultado: ISuperObject;
begin
  stringList := TStringList.Create;
  stringList.Text := SO(informacao).AsJSon(True);
  {$ifdef USAR_CODESITE}
  Logger(LOG_SESSAO).Debug(Format('Evento disparado <%s> com contexto', [evento]), stringList);
  {$else}
  TFile.AppendAllText(LogFilename, DateTimeToStr(Now()) + ' ' + string(evento) + ^j^m + stringList.Text);
  {$endif}

  ultimoErro := '';
  naoExibir := False;

  if mostrarNotificacao and (ListaNaoExibir.IndexOf(evento) < 0) then
    TformNotificacao.Executar(evento, stringList.Text, ultimoErro, modificadores, acao, naoExibir);

  stringList.Free;

  if naoExibir then
    ListaNaoExibir.Add(evento);
  if Assigned(params) and params.B['desmarcar_eventos'] then
    GravarConfig(NOME_PLUGIN, PChar(StringReplace(evento, '.', '_', [rfReplaceAll])), 0, nil);

  if Length(modificadores) >  0 then
    resultado := SO(modificadores)
  else
    resultado := SO();

  if ultimoErro <> '' then
    resultado.S['erro'] := ultimoErro;

  if acao <> '' then
    resultado.S['acao'] := acao;

  Result := AlocarBuffer(PChar(resultado.AsJSon(True)));
end;

function ObterVersao(): PChar; stdcall; export;
begin
  Result := AlocarBuffer(PChar('1.0.0.0'));
end;

function ObterNome(): PChar; stdcall; export;
begin
  Result := AlocarBuffer(PChar(NOME_PLUGIN));
end;

function ObterDadosFabricante(): PChar; stdcall; export;
begin
  Result := AlocarBuffer(PChar(FABRICANTE));
end;

procedure RegistrarAssinaturas(AssinarEvento: ProcAssinarEvento); stdcall; export;
var
  buffer : PChar;
  evento: string;
  obj: ISuperObject;
  f : TSuperObjectIter;
begin
  {$ifndef USAR_CODESITE}
  LogFilename := IncludeTrailingPathDelimiter(ObterCaminhoDoPlugin()) + 'log';
  ForceDirectories(LogFilename);
  LogFilename := IncludeTrailingPathDelimiter(LogFilename) + 'eventos.log';
  {$endif}
  // Obtenho os params no arquivo de config
  obj := SO(TFile.ReadAllText(IncludeTrailingPathDelimiter(ObterCaminhoDoPlugin()) + 'eventos.json'));
  params := obj.O['params'];

  ListaNaoExibir:= TStringList.Create;

  // Assina os eventos que deseja receber
  buffer := ObterConfigs(NOME_PLUGIN, 0);
  // Obtenho as configurações salvas
  obj := SO(buffer);

  mostrarNotificacao := obj.S['configs.MostrarNotificacao.valor'] = '1';
  if ObjectFindFirst(obj['configs'], f) then
    repeat
      if StartsStr('Evento_', f.key) then
      begin
        evento := StringReplace(Copy(f.key, 8, Length(f.key)-7), '_', '.', [rfReplaceAll]);
        AssinarEvento(NOME_PLUGIN, PChar(evento));
      end;
      // Este evento é gerado por ítens de interface (menu, botões) adicionados via ui.config
    until not ObjectFindNext(f);

  LiberarBuffer(buffer);
end;

procedure AtribuirObtencaoDeFuncoes(_ObterFuncao: ProcObterFuncao); stdcall; export;
begin
  ObterFuncao := _ObterFuncao;
  AlocarBuffer := ProcAlocarBuffer(ObterFuncao('AlocarBuffer'));
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

function Atualizar(): PChar;
begin
  Result := AlocarBuffer('');
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
  Result := AlocarBuffer(PChar(Format('{"erro":"Macro desconhecida: %s"}', [umaMacro])))
end;


function ObterCaminhoDoPlugin: string;
var
  buffer: array[0..MAX_PATH] of Char;
begin
  FillChar(buffer, Length(buffer)-1, #0);
  GetModuleFileName(HInstance, Buffer, Length(Buffer));
  Result := ExtractFilePath(buffer);
end;

initialization
  ListaNaoExibir:= nil;
finalization
  FreeAndNil(ListaNaoExibir);
end.
