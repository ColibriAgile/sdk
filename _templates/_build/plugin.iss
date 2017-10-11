#ifndef AppName
  #define AppName "Nome"
  #define AppVersion "1.0.0.0"
  #define Extensao ".col"
#endif

#define pluginArq "plugin." + AppName + Extensao

#define PastaIncludes ".\"
#include PastaIncludes + "colibri_includes.iss"


[Setup]
AppCopyright=Copyright© 2017, NCR
AppName={#AppName}
AppVersion={#AppVersion} 
AppPublisher=NCR Corporation
AppPublisherUrl=http://www.colibri.com.br
DefaultDirName={code:PastaNCRColibri|c:\NCR Colibri}
OutputDir=_build\pacote
OutputBaseFilename={#AppName}_{#AppVersion}
Uninstallable=no
UsePreviousAppDir=no
SourceDir=..

[Files]
Source: {#pluginArq}; DestDir: "{app}\plugins\{#AppName}\"; Flags: ignoreversion recursesubdirs restartreplace overwritereadonly
Source: ..\ui.config; DestDir: "{app}\plugins\{#AppName}"; Flags: skipifsourcedoesntexist ignoreversion recursesubdirs restartreplace overwritereadonly
Source: ..\reports\*; DestDir: "{app}\plugins\{#AppName}\reports"; Flags: skipifsourcedoesntexist ignoreversion recursesubdirs restartreplace overwritereadonly
Source: ..\extras\*; DestDir: "{app}\plugins\{#AppName}"; Flags: skipifsourcedoesntexist ignoreversion recursesubdirs restartreplace overwritereadonly
