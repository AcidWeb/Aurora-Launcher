import os
import shutil
import winreg
import subprocess
import win32file
import Constants

# Enviroment setup
k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Control Panel\\International', 0, winreg.KEY_ALL_ACCESS)
kDecimalOrg = winreg.QueryValueEx(k, 'sDecimal')[0]
kThousandOrg = winreg.QueryValueEx(k, 'sThousand')[0]
winreg.SetValueEx(k, 'sDecimal', 0, 1, '.')
winreg.SetValueEx(k, 'sThousand', 0, 1, ' ')
if Constants.IS_PORTABLE:
    p = subprocess.Popen('regsvr32 /s ' + os.path.join(os.getcwd(), 'MSSTDFMT.DLL'))
    p.wait()
if os.path.isfile(os.path.join(os.getcwd(), 'Stevefire.mdb.4')):
    shutil.copyfile(os.path.join(os.getcwd(), 'Stevefire.mdb.4'), os.path.join(os.getcwd(), 'Stevefire.mdb.5'))
if os.path.isfile(os.path.join(os.getcwd(), 'Stevefire.mdb.3')):
    shutil.copyfile(os.path.join(os.getcwd(), 'Stevefire.mdb.3'), os.path.join(os.getcwd(), 'Stevefire.mdb.4'))
if os.path.isfile(os.path.join(os.getcwd(), 'Stevefire.mdb.2')):
    shutil.copyfile(os.path.join(os.getcwd(), 'Stevefire.mdb.2'), os.path.join(os.getcwd(), 'Stevefire.mdb.3'))
shutil.copyfile(os.path.join(os.getcwd(), 'Stevefire.mdb'), os.path.join(os.getcwd(), 'Stevefire.mdb.2'))
os.remove(os.path.join(os.getcwd(), 'Stevefire.mdb'))
p = subprocess.Popen(os.path.join(os.getcwd(), 'Tools', 'JETCOMP.exe')
                     + ' -src:"' + os.path.join(os.getcwd(), 'Stevefire.mdb.2')
                     + '" -dest:"' + os.path.join(os.getcwd(), 'Stevefire.mdb') + '" -w' + Constants.DATABASE_PASSWORD)
p.wait()
try:
    win32file.CreateSymbolicLink(os.path.splitdrive(os.getcwd())[0] + os.path.sep + 'Logs',
                                 os.path.join(os.getcwd(), 'Logs'), 1)
except:
    pass

# Starting Aurora
p = subprocess.Popen(os.path.join(os.getcwd(), 'Aurora.exe'))
p.wait()

# Cleanup
if Constants.IS_PORTABLE:
    p = subprocess.Popen('regsvr32 /s /u ' + os.path.join(os.getcwd(), 'MSSTDFMT.DLL'))
    p.wait()
try:
    os.remove(os.path.splitdrive(os.getcwd())[0] + os.path.sep + 'Logs')
except:
    pass
winreg.SetValueEx(k, 'sDecimal', 0, 1, kDecimalOrg)
winreg.SetValueEx(k, 'sThousand', 0, 1, kThousandOrg)
k.Close()
