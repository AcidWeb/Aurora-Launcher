#define MyAppName "Aurora"
#define MyAppVersion "7.1.0"
#define MyAppPublisher "Steve Walmsley"
#define MyAppExeName "Aurora_Wrapper.exe"

[Setup]
AppId={{90893FB5-38AE-4164-B689-3214719D0D4A}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppCopyright=Copyright (C) 2014-2016 Steve Walmsley
DefaultDirName={sd}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputBaseFilename=Aurora_{#MyAppVersion}
SetupIconFile=Assets\Aurora.ico
SolidCompression=yes
ShowLanguageDialog=no
LanguageDetectionMethod=none
WizardImageFile=Assets\Wizard.bmp
UninstallDisplayName={#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
SignTool=SignTool /d $q{#MyAppName}$q $f

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "Tools\vc_redist.x86.exe"; DestDir: "{tmp}"; Flags: ignoreversion deleteafterinstall
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion
Source: "Files\Base\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "Files\Executable\{#MyAppVersion}\*"; DestDir: "{app}"; Flags: ignoreversion
Source: "Files\Base\MSSTDFMT.DLL"; DestDir: {sys}; Flags: onlyifdoesntexist regserver 32bit

[Icons]
Name: "{group}\{#MyAppName} {#MyAppVersion}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{tmp}\vc_redist.x86.exe"; Parameters: "/passive /norestart"; StatusMsg: "Installing Microsoft Visual C++ 2015 Redistributable Package...";