; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "NCR Plugin de Contextos do Colibri"
#define MyAppVersion "1.0"
#define MyAppPublisher "NCR Food Service"
#define MyAppURL "http://www.colibri.com.br"


[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{272CE42E-99BD-41C5-9918-FBA00C37912F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={reg:HKLM\Software\Wyse Sistemas\Colibri 8,InstallDir|{sd}\Colibri 8\}
OutputDir=..\..\tools\contextos
OutputBaseFilename=instaladorPluginContextos
Compression=lzma
SolidCompression=yes
;DisableDirPage=yes
DefaultGroupName=Colibri 8
DisableProgramGroupPage=yes
DirExistsWarning=no

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Files]
Source: "eventos.json"; DestDir: "{app}\bin\plugins\contextos"; Flags: ignoreversion
Source: "plugin.contextos.col"; DestDir: "{app}\bin\plugins\contextos"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files
