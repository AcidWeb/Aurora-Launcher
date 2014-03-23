#define MyAppName "Aurora"
#define MyAppVersion "6.3.0"
#define MyAppPublisher "Steve Walmsley"
#define MyAppExeName "Aurora.exe"

[Setup]
AppId={{90893FB5-38AE-4164-B689-3214719D0D4A}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppCopyright=Copyright (C) 2014 Steve Walmsley
DefaultDirName={pf}\{#MyAppName}
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
Source: "Tools\vcredist_x86.exe"; DestDir: "{tmp}"; Flags: ignoreversion deleteafterinstall
Source: "build\exe.win32-3.3\*"; DestDir: "{app}"; Flags: ignoreversion
Source: "Files\Base\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs
Source: "Files\Executable\{#MyAppVersion}\*"; DestDir: "{app}"; Flags: ignoreversion
Source: "Files\Base\MSSTDFMT.DLL"; DestDir: {sys}; Flags: onlyifdoesntexist regserver 32bit

[Icons]
Name: "{group}\{#MyAppName} {#MyAppVersion}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall
Filename: "{tmp}\vcredist_x86.exe"; Parameters: "/passive /Q:a /c:""msiexec /qb /i vcredist.msi"" "; StatusMsg: "Installing Microsoft Visual C++ 2010 Redistributable Package...";