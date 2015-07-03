unit form.config;

interface

uses
  Winapi.Windows,
  Winapi.Messages,
  System.SysUtils,
  System.StrUtils,
  System.Variants,
  System.Classes,
  System.IOUtils,
  Vcl.Graphics,
  Vcl.Controls,
  Vcl.Forms,
  Vcl.Dialogs,
  Vcl.StdCtrls,
  Vcl.ComCtrls,
  JvExComCtrls,
  JvComCtrls,
  JvCheckTreeView,
  suporte.superobj,
  plugin.api;

type
  TfrmConfig = class(TForm)
    btOK: TButton;
    btCancel: TButton;
    Button1: TButton;
    Button2: TButton;
    Label1: TLabel;
    ckMostrarNotificacao: TCheckBox;
    checkTree: TJvCheckTreeView;
    procedure FormShow(Sender: TObject);
    procedure Button1Click(Sender: TObject);
    procedure Button2Click(Sender: TObject);
    procedure FormDestroy(Sender: TObject);
    procedure btOKClick(Sender: TObject);
  private
    Selecionadas : TStringList;
  public
    class function Executar(informacao:PChar): Integer;
  end;

implementation

{$R *.dfm}

procedure TfrmConfig.Button1Click(Sender: TObject);
var
  node : TTreeNode;
begin
  for node in checkTree.Items do
    checkTree.Checked[node] := True;
end;

procedure TfrmConfig.Button2Click(Sender: TObject);
var
  node : TTreeNode;
begin
  for node in checkTree.Items do
    checkTree.Checked[node] := False;
end;

class function TfrmConfig.Executar(informacao:PChar): Integer;
var
  form: TfrmConfig;
begin
  form := TfrmConfig.Create(nil);
  try
    Result := form.ShowModal();
  finally
    FreeAndNil(form);
  end;
end;

procedure TfrmConfig.FormDestroy(Sender: TObject);
var
  item:Integer;
begin
  for item := 0 to checkTree.Items.Count-1 do
    if Assigned(checkTree.Items.Item[item].Data) then
      StrDispose(PChar(checkTree.Items.Item[item].Data));

  FreeAndNil(Selecionadas);
end;

procedure TfrmConfig.FormShow(Sender: TObject);
var
  obj, item : ISuperObject;
  f : TSuperObjectIter;
  treeNode, subNode : TTreeNode;
  buffer: PChar;
  evento: string;
  selecionados, total : Integer;
begin
  Selecionadas := TStringList.Create();

  buffer := ObterConfigs(NOME_PLUGIN, 0);
  // Obtenho as configurações salvas
  obj := SO(buffer);

  if ObjectFindFirst(obj['configs'], f) then
    repeat
      if StartsStr('Evento_', f.key) then
      begin
        evento := Copy(f.key, 8, Length(f.key)-7);
        Selecionadas.Add(evento);
      end;
    until not ObjectFindNext(f);

  ckMostrarNotificacao.Checked := obj.S['configs.MostrarNotificacao.valor'] = '1';
  LiberarBuffer(buffer);

  // Leio os eventos existentes
  obj := SO(TFile.ReadAllText(IncludeTrailingPathDelimiter(ObterCaminhoDoPlugin()) + 'eventos.json'));
  treeNode := nil;

  if ObjectFindFirst(obj['eventos'], f) then
    repeat
      treeNode := checkTree.Items.Add(treeNode, f.key);
      selecionados := 0;
      total := 0;
      subNode := nil;

      for item in f.val do
      begin
        subNode := checkTree.Items.AddChild(treeNode, item.AsString);
        evento := f.key + '_' + item.AsString;
        subNode.Data := StrNew(PChar(evento));
        if Selecionadas.IndexOf(evento) >= 0 then
        begin
          checkTree.Checked[subNode] := True;
          selecionados := selecionados + 1;
        end;
        total := total + 1;
      end;
    if Assigned(subNode) and (selecionados = total) then
      checkTree.Checked[treeNode] := True;

    until not ObjectFindNext(f);
  ObjectFindClose(f);
  checkTree.Refresh;
end;

procedure TfrmConfig.btOKClick(Sender: TObject);
var
  node : TTreeNode;
  NovasSelecionadas : TStringList;
  valor : PChar;
  item  : Integer;
begin
  NovasSelecionadas := TStringList.Create;

  for node in checkTree.Items do
    if Assigned(node.Data) and checkTree.Checked[node] then
      NovasSelecionadas.Add(PChar(node.Data));

  // Apago as configs anteriores que não serão mais utilizadas
  for item := 0 to Selecionadas.Count-1 do
    if NovasSelecionadas.IndexOf(Selecionadas.Strings[item]) < 0 then
      GravarConfig(NOME_PLUGIN, PChar('Evento_' + Selecionadas.Strings[item]), 0, nil);

  // Gravo as configs incluídas
  for item := 0 to NovasSelecionadas.Count-1 do
    if Selecionadas.IndexOf(NovasSelecionadas.Strings[item]) < 0 then
      GravarConfig(NOME_PLUGIN, PChar('Evento_' + NovasSelecionadas.Strings[item]), 0, '1');
  FreeAndNil(Selecionadas);
  Selecionadas := NovasSelecionadas;

  if ckMostrarNotificacao.Checked then
    valor := '1'
  else
    valor := '0';
  GravarConfig(NOME_PLUGIN, 'MostrarNotificacao', 0, valor);
end;


end.
