; Inno Setup Script for Ecoute AI Research Assistant

#define MyAppName "Ecoute AI Research Assistant"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "Ecoute"
#define MyAppExeName "Ecoute.exe"

[Setup]
AppId={{8D4F5A3C-9B2E-4F7D-A1C8-6E3B9F2D7A4C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\Ecoute
DefaultGroupName=Ecoute
AllowNoIcons=yes
OutputDir=dist
OutputBaseFilename=EcouteSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\Ecoute\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\Ecoute\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;

  // Check if FFmpeg is installed
  if not FileExists(ExpandConstant('{sys}\ffmpeg.exe')) then
  begin
    if MsgBox('FFmpeg is required but not found. Would you like to see installation instructions?', mbConfirmation, MB_YESNO) = IDYES then
    begin
      ShellExec('open', 'https://ffmpeg.org/download.html', '', '', SW_SHOW, ewNoWait, ResultCode);
    end;
  end;
end;
