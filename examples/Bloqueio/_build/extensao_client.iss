#ifndef AppName
  #define AppName "Nome"
  #define AppVersion "1.0.0.0"
  #define ExtensionName "Nome"
#endif

#define PastaIncludes ".\"
#include PastaIncludes + "colibri_includes.iss"


[Setup]
AppCopyright=Copyright 2017
AppName={#AppName}
AppVersion={#AppVersion} 
AppPublisher=NCR Corporation
DefaultDirName={code:PastaNCRColibri|c:\NCR Colibri}
OutputDir=_build\pacote
OutputBaseFilename={#ExtensionName}_{#AppVersion}_client
Uninstallable=no
UsePreviousAppDir=no
SourceDir=..

[Files]
Source: "client\*"; DestDir: "{app}\plugins\{#ExtensionName}\"; Flags: skipifsourcedoesntexist ignoreversion recursesubdirs restartreplace overwritereadonly; Excludes: "leia-me.txt"
Source: reports\*; DestDir: "{app}\plugins\{#ExtensionName}\reports"; Flags: skipifsourcedoesntexist ignoreversion recursesubdirs restartreplace overwritereadonly
Source: templates\*; DestDir: "{app}\plugins\{#ExtensionName}\templates"; Flags: skipifsourcedoesntexist ignoreversion recursesubdirs restartreplace overwritereadonly
Source: extras\*; DestDir: "{app}\plugins\{#ExtensionName}"; Flags: skipifsourcedoesntexist ignoreversion recursesubdirs restartreplace overwritereadonly

[InstallDelete]
Type: filesandordirs; Name: "{app}\plugins\{#ExtensionName}\templates"
Type: filesandordirs; Name: "{app}\plugins\{#ExtensionName}\reports"
