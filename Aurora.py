import os
import sys
import shutil
import winreg
import subprocess
import win32file
import pygame
import random
import time

# Initialization
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(os.path.abspath(sys.executable)))
else:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
if os.path.isfile('unins000.exe'):
    portable = False
else:
    portable = True
registry = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Control Panel\\International', 0, winreg.KEY_ALL_ACCESS)
clock = pygame.time.Clock()
playlist = []
dbpassword = ''
paused = False
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.display.set_icon(pygame.image.load(open('Aurora.png', 'rb')))
pygame.display.set_caption('Aurora')

# Display splash
splash = pygame.image.load(open('Splash.png', 'rb'))
screen = pygame.display.set_mode(splash.get_size(), pygame.NOFRAME)
screen.blit(splash, (0, 0))
pygame.display.update()

# Load music
for ogg in os.listdir('Music'):
    if ogg.endswith('.ogg'):
        playlist.append(os.path.join('Music', ogg))
if len(playlist) > 0:
    pygame.mixer.music.load(random.choice(playlist))
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    pygame.mixer.music.play()

# Database backup
try:
    shutil.move('Stevefire.mdb', 'Stevefire.mdb.2')
except PermissionError:
    sys.exit()
if os.path.isfile('Stevefire.mdb.4'):
    shutil.copyfile('Stevefire.mdb.4', 'Stevefire.mdb.5')
if os.path.isfile('Stevefire.mdb.3'):
    shutil.copyfile('Stevefire.mdb.3', 'Stevefire.mdb.4')
shutil.copyfile('Stevefire.mdb.2', 'Stevefire.mdb.3')
subprocess.Popen(os.path.join('Tools', 'JETCOMP.exe') + ' -src:"Stevefire.mdb.2" -dest:"Stevefire.mdb" -w' + dbpassword).wait()

# Enviroment setup
regdecimalorg = winreg.QueryValueEx(registry, 'sDecimal')[0]
regthousandorg = winreg.QueryValueEx(registry, 'sThousand')[0]
winreg.SetValueEx(registry, 'sDecimal', 0, 1, '.')
winreg.SetValueEx(registry, 'sThousand', 0, 1, ' ')
if portable:
    subprocess.Popen('regsvr32 /s MSSTDFMT.DLL').wait()
try:
    win32file.CreateSymbolicLink(os.path.splitdrive(os.getcwd())[0] + os.path.sep + 'Logs', os.path.join(os.getcwd(), 'Logs'), 1)
except:
    pass

# Starting Aurora
time.sleep(1)
aurora = subprocess.Popen('Aurora.exe')

# Main event loop
while aurora.poll() is None:
    clock.tick(1)
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            pygame.mixer.music.load(random.choice(playlist))
            pygame.mixer.music.play()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            if paused:
                paused = False
                pygame.mixer.music.unpause()
            else:
                paused = True
                pygame.mixer.music.pause()
        elif event.type == pygame.QUIT:
            aurora.terminate()

# Cleanup
if portable:
    subprocess.Popen('regsvr32 /s /u MSSTDFMT.DLL').wait()
try:
    os.remove(os.path.splitdrive(os.getcwd())[0] + os.path.sep + 'Logs')
except:
    pass
winreg.SetValueEx(registry, 'sDecimal', 0, 1, regdecimalorg)
winreg.SetValueEx(registry, 'sThousand', 0, 1, regthousandorg)
registry.Close()
