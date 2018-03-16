#ifndef AppName
  #define AppName "Nome"
  #define AppVersion "1.0.0.0"
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
OutputBaseFilename={#AppName}_{#AppVersion}_client
Uninstallable=no
UsePreviousAppDir=no
SourceDir=..

[Files]
Source: "client\*"; DestDir: "{app}\plugins\{#AppName}\"; Flags: skipifsourcedoesntexist ignoreversion recursesubdirs restartreplace overwritereadonly; Excludes: "leia-me.txt"
Source: reports\*; DestDir: "{app}\plugins\{#AppName}\reports"; Flags: skipifsourcedoesntexist ignoreversion recursesubdirs restartreplace overwritereadonly
Source: extras\*; DestDir: "{app}\plugins\{#AppName}"; Flags: skipifsourcedoesntexist ignoreversion recursesubdirs restartreplace overwritereadonly
