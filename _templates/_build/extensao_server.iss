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
OutputBaseFilename={#ExtensionName}_{#AppVersion}_server
Uninstallable=no
UsePreviousAppDir=no
SourceDir=..

[Files]
Source: "server\*"; DestDir: "{app}\master\colibri\{#ExtensionName}"; Flags: skipifsourcedoesntexist ignoreversion recursesubdirs restartreplace overwritereadonly; Excludes: "leia-me.txt"
