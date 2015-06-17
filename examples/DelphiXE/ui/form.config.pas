unit form.config;

interface

uses
  Winapi.Windows,
  Winapi.Messages,
  System.SysUtils,
  System.Variants,
  System.Classes,
  Vcl.Graphics,
  Vcl.Controls,
  Vcl.Forms,
  Vcl.Dialogs,
  Vcl.StdCtrls;

type
  TfrmConfig = class(TForm)
    btOK: TButton;
    btCancel: TButton;
    procedure btCancelClick(Sender: TObject);
  public
    class function Executar(informacao:PChar): Integer;
  end;

implementation

{$R *.dfm}

procedure TfrmConfig.btCancelClick(Sender: TObject);
begin
  ModalResult:= mrClose;
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

end.
