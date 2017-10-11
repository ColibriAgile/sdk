[Code]
function PastaNCRColibri(s:string): string;
begin
  if s = '' then
    s := '{sd}\NCR Colibri\';
  Result := ExpandConstant('{reg:HKLM32\Software\NCR\Colibri,NCRColibri|' + s +'}');
end;
