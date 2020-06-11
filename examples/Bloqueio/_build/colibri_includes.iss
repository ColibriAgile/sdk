[Code]
function PastaNCRColibri(s:string): string;
begin
  if s = '' then
    s := '{sd}\NCR Colibri\';
  Result := ExpandConstant('{reg:HKLM32\Software\NCR\Colibri,NCRColibri|' + s +'}');
end;

function InitializeUninstall(): Boolean;
var
  i:Integer;
begin
  Result:= False;
  for i:= 0 to ParamCount do
     if ParamStr(i) = '/REMOVER' then
     begin
       Result := True;
       break;
     end;

  if Result = False then
    MsgBox('Este é um componente do NCR Colibri e só pode ser desinstalado pelo desinstalador do NCR Colibri Client ou Master', mbError, MB_OK);
end;
