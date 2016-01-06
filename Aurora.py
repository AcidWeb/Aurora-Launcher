import os
import sys
import shutil
import winreg
import subprocess
import win32file
import pygame

# Initialization
VERSION = '2.0'
REG = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Control Panel\\International', 0, winreg.KEY_ALL_ACCESS)
DATABASE_PASSWORD = ''
CWD = os.getcwd()
if os.path.isfile(os.path.join(CWD, 'unins000.exe')):
    IS_PORTABLE = False
else:
    IS_PORTABLE = True
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.display.set_caption('Aurora')
clock = pygame.time.Clock()

# Display splash
splash = pygame.image.load(open(os.path.join(CWD, 'Splash.png'), 'rb'))
screen = pygame.display.set_mode(splash.get_size(), pygame.NOFRAME)
screen.blit(splash, (0, 0))
pygame.display.update()

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
aurora = subprocess.Popen(os.path.join(CWD, 'Aurora.exe'))

# Main event loop
while aurora.poll() is None:
    clock.tick(1)

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
