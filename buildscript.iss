; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "AACSpeakHelper"
#define MyAppVersion "2.4.0"
#define MyAppPublisher "Ace Centre"
#define MyAppURL "https://acecentre.org.uk"
#define MyAppExeName "client.exe"

#define MICROSOFT_TOKEN "{#MICROSOFT_TOKEN}"
#define MICROSOFT_REGION "{#MICROSOFT_REGION}"
#define GOOGLE_CREDS_PATH "{#GOOGLE_CREDS_PATH}"
#define MICROSOFT_TOKEN_TRANS "{#MICROSOFT_TOKEN_TRANS}"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{E38A71DA-9390-48E3-9F70-52D77EE41F98}
ChangesEnvironment=yes
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\Ace Centre\AACSpeakHelper
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
DisableDirPage=yes
; Uncomment the following line to run in non administrative install mode (install for current user only.)
PrivilegesRequired=lowest
;PrivilegesRequiredOverridesAllowed=dialog
OutputBaseFilename=AACSpeakHelper
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\client\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\client\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\AACSpeakHelperServer\AACSpeakHelperServer.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\AACSpeakHelperServer\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "assets\translate.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "settings.cfg"; DestDir: "{userappdata}\Ace Centre\AACSpeakHelper"; Flags: ignoreversion
Source: "dist\Configure AACSpeakHelper\Configure AACSpeakHelper.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\Configure AACSpeakHelper\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\CreateGridset\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "assets\translate.ico"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs
Source: "assets\translate_loading.ico"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs
Source: "assets\TranslateAndTTS DemoGridset.gridset"; DestDir: "{userappdata}\Ace Centre\AACSpeakHelper"; Flags: ignoreversion
Source: "dist\AACSpeakHelperServer\config.enc"; DestDir: "{app}\_libs"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Configure {#MyAppName}"; Filename: "{app}\Configure AACSpeakHelper.exe"
Name: "{group}\Settings File"; Filename: "{userappdata}\AACSpeakHelper\settings.cfg"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{autodesktop}\Configure AACSpeakHelper"; Filename: "{app}\Configure AACSpeakHelper.exe"; Tasks: desktopicon
Name: "{userstartup}\AACSpeakHelperServer.exe"; Filename: "{app}\AACSpeakHelperServer.exe"; WorkingDir: "{app}"

[Run]
Filename: "{app}\CreateGridset.exe"
Filename: "{cmd}"; Parameters: "start""/b""cmd""/c""echo|set /p=Hello World|clip"; Flags: nowait skipifsilent
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent unchecked
Filename: "{app}\AACSpeakHelperServer.exe"; Flags: nowait postinstall skipifsilent
Filename: "{app}\Configure AACSpeakHelper.exe"; Flags: nowait postinstall skipifsilent
