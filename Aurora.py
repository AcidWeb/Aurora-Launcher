import os
import shutil
import winreg
import subprocess
import win32file

REG = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Control Panel\\International', 0, winreg.KEY_ALL_ACCESS)
DATABASE_PASSWORD = ''
CWD = os.getcwd()
if os.path.isfile(os.path.join(CWD, 'unins000.exe')):
    IS_PORTABLE = False
else:
    IS_PORTABLE = True

# Enviroment setup
regDecimalOrg = winreg.QueryValueEx(REG, 'sDecimal')[0]
regThousandOrg = winreg.QueryValueEx(REG, 'sThousand')[0]
winreg.SetValueEx(REG, 'sDecimal', 0, 1, '.')
winreg.SetValueEx(REG, 'sThousand', 0, 1, ' ')
if IS_PORTABLE:
    p = subprocess.Popen('regsvr32 /s "' + os.path.join(CWD, 'MSSTDFMT.DLL') + '"')
    p.wait()
if os.path.isfile(os.path.join(CWD, 'Stevefire.mdb.4')):
    shutil.copyfile(os.path.join(CWD, 'Stevefire.mdb.4'), os.path.join(CWD, 'Stevefire.mdb.5'))
if os.path.isfile(os.path.join(CWD, 'Stevefire.mdb.3')):
    shutil.copyfile(os.path.join(CWD, 'Stevefire.mdb.3'), os.path.join(CWD, 'Stevefire.mdb.4'))
if os.path.isfile(os.path.join(CWD, 'Stevefire.mdb.2')):
    shutil.copyfile(os.path.join(CWD, 'Stevefire.mdb.2'), os.path.join(CWD, 'Stevefire.mdb.3'))
shutil.copyfile(os.path.join(CWD, 'Stevefire.mdb'), os.path.join(CWD, 'Stevefire.mdb.2'))
os.remove(os.path.join(CWD, 'Stevefire.mdb'))
p = subprocess.Popen(os.path.join(CWD, 'Tools', 'JETCOMP.exe') + ' -src:"' + os.path.join(CWD, 'Stevefire.mdb.2')
                     + '" -dest:"' + os.path.join(CWD, 'Stevefire.mdb') + '" -w' + DATABASE_PASSWORD)
p.wait()
try:
    win32file.CreateSymbolicLink(os.path.splitdrive(CWD)[0] + os.path.sep + 'Logs', os.path.join(CWD, 'Logs'), 1)
except:
    pass

# Starting Aurora
p = subprocess.Popen(os.path.join(CWD, 'Aurora.exe'))
p.wait()

# Cleanup
if IS_PORTABLE:
    p = subprocess.Popen('regsvr32 /s /u "' + os.path.join(CWD, 'MSSTDFMT.DLL') + '"')
    p.wait()
try:
    os.remove(os.path.splitdrive(CWD)[0] + os.path.sep + 'Logs')
except:
    pass
winreg.SetValueEx(REG, 'sDecimal', 0, 1, regDecimalOrg)
winreg.SetValueEx(REG, 'sThousand', 0, 1, regThousandOrg)
REG.Close()