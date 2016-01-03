import os
import sys
import shutil
import winreg
import subprocess
import win32file
import tkinter as tk

VERSION = '1.5'
REG = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Control Panel\\International', 0, winreg.KEY_ALL_ACCESS)
DATABASE_PASSWORD = ''
CWD = os.getcwd()
if os.path.isfile(os.path.join(CWD, 'unins000.exe')):
    IS_PORTABLE = False
else:
    IS_PORTABLE = True


def aurora(r):
    # Database backup
    try:
        shutil.move(os.path.join(CWD, 'Stevefire.mdb'), os.path.join(CWD, 'Stevefire.mdb.2'))
    except PermissionError:
        sys.exit()
    if os.path.isfile(os.path.join(CWD, 'Stevefire.mdb.4')):
        shutil.copyfile(os.path.join(CWD, 'Stevefire.mdb.4'), os.path.join(CWD, 'Stevefire.mdb.5'))
    if os.path.isfile(os.path.join(CWD, 'Stevefire.mdb.3')):
        shutil.copyfile(os.path.join(CWD, 'Stevefire.mdb.3'), os.path.join(CWD, 'Stevefire.mdb.4'))
    shutil.copyfile(os.path.join(CWD, 'Stevefire.mdb.2'), os.path.join(CWD, 'Stevefire.mdb.3'))
    subprocess.Popen(os.path.join(CWD, 'Tools', 'JETCOMP.exe') + ' -src:"' + os.path.join(CWD, 'Stevefire.mdb.2') +
                     '" -dest:"' + os.path.join(CWD, 'Stevefire.mdb') + '" -w' + DATABASE_PASSWORD).wait()

    # Enviroment setup
    regdecimalorg = winreg.QueryValueEx(REG, 'sDecimal')[0]
    regthousandorg = winreg.QueryValueEx(REG, 'sThousand')[0]
    winreg.SetValueEx(REG, 'sDecimal', 0, 1, '.')
    winreg.SetValueEx(REG, 'sThousand', 0, 1, ' ')
    if IS_PORTABLE:
        subprocess.Popen('regsvr32 /s "' + os.path.join(CWD, 'MSSTDFMT.DLL') + '"').wait()
    try:
        win32file.CreateSymbolicLink(os.path.splitdrive(CWD)[0] + os.path.sep + 'Logs', os.path.join(CWD, 'Logs'), 1)
    except:
        pass

    # Starting Aurora
    r.destroy()
    subprocess.Popen(os.path.join(CWD, 'Aurora.exe')).wait()

    # Cleanup
    if IS_PORTABLE:
        subprocess.Popen('regsvr32 /s /u "' + os.path.join(CWD, 'MSSTDFMT.DLL') + '"').wait()
    try:
        os.remove(os.path.splitdrive(CWD)[0] + os.path.sep + 'Logs')
    except:
        pass
    winreg.SetValueEx(REG, 'sDecimal', 0, 1, regdecimalorg)
    winreg.SetValueEx(REG, 'sThousand', 0, 1, regthousandorg)
    REG.Close()


if __name__ == "__main__":
    # Show splash
    root = tk.Tk()
    root.overrideredirect(True)
    w = 465
    h = 215
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    image = tk.PhotoImage(file=os.path.join(CWD, 'Splash.png'))
    root.geometry('%dx%d+%d+%d' % (w, h, (ws/2) - (w/2), (hs/2) - (h/2)))
    canvas = tk.Canvas(root, width=w, height=h, bg='black')
    canvas.create_image(w/2, h/2, image=image)
    canvas.pack()
    root.after(2000, aurora, root)
    root.mainloop()
