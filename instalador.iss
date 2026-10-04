[Setup]
AppName=Sistema de Chamada
AppVersion=1.0.0
DefaultDirName={autopf}\Sistema de Chamada
DefaultGroupName=Sistema de Chamada
OutputDir=instalador
OutputBaseFilename=SistemaChamada-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "dist\SistemaChamada.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Sistema de Chamada"; Filename: "{app}\SistemaChamada.exe"
Name: "{autodesktop}\Sistema de Chamada"; Filename: "{app}\SistemaChamada.exe"

[Run]
Filename: "{app}\SistemaChamada.exe"; Description: "Executar Sistema de Chamada"; Flags: nowait postinstall skipifsilent