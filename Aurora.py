import os
import sys
import shutil
import subprocess
import winreg
import win32file
import win32gui
import pygame
import logging
import time
import random
import configparser
import argparse


def window_handler(hwnd, windows):
    windows.append((hwnd, win32gui.GetWindowText(hwnd)))


def show_image(img=None, tips=None):
    if tips is None:
        pygame.display.quit()
        if not img:
            image = pygame.image.load(open('Splash.png', 'rb'))
            screen = pygame.display.set_mode(image.get_size(), pygame.NOFRAME)
            screen.blit(image, (0, 0))
            font = pygame.font.Font('Aurora.ttf', 9)
            text = font.render(wcfg.wrapper_version, 1, (255, 255, 255))
            screen.blit(text, (398, 204))
        else:
            image = pygame.image.load(open(os.path.join('Background', img), 'rb'))
            x = (wcfg.dinfo.current_w - image.get_size()[0]) // 2
            y = (wcfg.dinfo.current_h - image.get_size()[1]) // 2
            wcfg.screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
            wcfg.screen.blit(image, (x, y))
        pygame.display.set_icon(pygame.image.load(open('Aurora.png', 'rb')))
        pygame.display.set_caption('Aurora Wrapper')
        pygame.display.update()
    else:
        image = pygame.image.load(open(os.path.join('Background', img), 'rb'))
        x = (wcfg.dinfo.current_w - image.get_size()[0]) // 2
        y = (wcfg.dinfo.current_h - image.get_size()[1]) // 2
        wcfg.screen.blit(image, (x, y))
        if tips:
            font = pygame.font.Font('Aurora.ttf', 12)
            font.set_bold(True)
            text = font.render('M - enable/disable music   , - volume down   . - volume up', 1, (255, 255, 255))
            wcfg.screen.blit(text, ((wcfg.dinfo.current_w // 2) - (text.get_width() // 2), wcfg.dinfo.current_h - 15))
        pygame.display.update()


def change_volume(up):
    volume = round(pygame.mixer.music.get_volume(), 2)
    if up:
        if volume < 1.0:
            volume += 0.05
    else:
        if volume > 0.1:
            volume -= 0.05
    pygame.mixer.music.set_volume(round(volume, 2))
    icfg['DEFAULT']['MusicVolume'] = str(round(volume, 2))


# Initialization
logging.basicConfig(filename='Aurora.log', filemode='w', level=logging.INFO)
logging.info('Initialization')
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(os.path.abspath(sys.executable)))
else:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.environ['SDL_VIDEO_CENTERED'] = '1'
icfg = configparser.ConfigParser()
icfg.read('Aurora.ini')
wcfg = argparse.Namespace()
if os.path.isfile('unins000.exe'):
    wcfg.portable = False
else:
    wcfg.portable = True
wcfg.registry = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Control Panel\\International', 0, winreg.KEY_ALL_ACCESS)
wcfg.playlist = []
wcfg.aurora_window = []
wcfg.dbpassword = ''
wcfg.wrapper_version = '7.10 - 2.4'
wcfg.background = random.choice(os.listdir('Background'))
pygame.init()
wcfg.clock = pygame.time.Clock()
wcfg.dinfo = pygame.display.Info()

# Display splash
logging.info('Displaying splash')
show_image()

# Load music
logging.info('Loading music')
for ogg in os.listdir('Music'):
    if ogg.endswith('.ogg'):
        wcfg.playlist.append(os.path.join('Music', ogg))
random.shuffle(wcfg.playlist)
if len(wcfg.playlist) > 0:
    pygame.mixer.music.load(wcfg.playlist[0])
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    pygame.mixer.music.set_volume(float(icfg['DEFAULT']['MusicVolume']))
    pygame.mixer.music.play()
if int(icfg['DEFAULT']['MusicDisabled']):
    wcfg.mpaused = 1
    pygame.mixer.music.pause()
else:
    wcfg.mpaused = 0

# Database backup
logging.info('Compacting database')
try:
    shutil.move('Stevefire.mdb', 'Stevefire.mdb.2')
except PermissionError:
    logging.error('Aurora already running!')
    sys.exit()
if os.path.isfile('Stevefire.mdb.4'):
    shutil.copyfile('Stevefire.mdb.4', 'Stevefire.mdb.5')
if os.path.isfile('Stevefire.mdb.3'):
    shutil.copyfile('Stevefire.mdb.3', 'Stevefire.mdb.4')
shutil.copyfile('Stevefire.mdb.2', 'Stevefire.mdb.3')
subprocess.Popen(os.path.join('Tools', 'JETCOMP.exe') + ' -src:"Stevefire.mdb.2" -dest:"Stevefire.mdb" -w' +
                 wcfg.dbpassword).wait()

# Enviroment setup
logging.info('Setting environment')
if 'regdecimal' not in icfg['DEFAULT'].keys():
    icfg['DEFAULT']['regdecimal'] = '"' + winreg.QueryValueEx(wcfg.registry, 'sDecimal')[0] + '"'
    icfg['DEFAULT']['regthousand'] = '"' + winreg.QueryValueEx(wcfg.registry, 'sThousand')[0] + '"'
winreg.SetValueEx(wcfg.registry, 'sDecimal', 0, 1, '.')
winreg.SetValueEx(wcfg.registry, 'sThousand', 0, 1, ' ')
if wcfg.portable:
    subprocess.Popen('regsvr32 /s MSSTDFMT.DLL').wait()
try:
    win32file.CreateSymbolicLink(os.path.splitdrive(os.getcwd())[0] + os.path.sep + 'Logs',
                                 os.path.join(os.getcwd(), 'Logs'), 1)
except:
    pass

# Starting Aurora
logging.info('Starting Aurora')
time.sleep(1)
show_image(wcfg.background)
wcfg.aurora = subprocess.Popen('Aurora.exe')
time.sleep(1)
win32gui.EnumWindows(window_handler, wcfg.aurora_window)
for i in wcfg.aurora_window:
    if i[1] == "Aurora":
        wcfg.aurora_window = i[0]
        break

# Main event loop
logging.info('Entering main event loop')
while wcfg.aurora.poll() is None:
    wcfg.clock.tick(5)
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            wcfg.playlist.append(wcfg.playlist.pop(0))
            pygame.mixer.music.load(wcfg.playlist[0])
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume())
            pygame.mixer.music.play()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_m and len(wcfg.playlist) > 0:
            if wcfg.mpaused:
                wcfg.mpaused = 0
                pygame.mixer.music.unpause()
            else:
                wcfg.mpaused = 1
                pygame.mixer.music.pause()
            icfg['DEFAULT']['MusicDisabled'] = str(wcfg.mpaused)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_PERIOD:
            change_volume(True)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_COMMA:
            change_volume(False)
        elif event.type == pygame.ACTIVEEVENT:
            if event.gain and event.state == 6:
                show_image(wcfg.background, True)
            elif event.state == 2:
                show_image(wcfg.background, False)
            pygame.event.clear()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            show_image(wcfg.background, False)
            pygame.event.clear()
            win32gui.ShowWindow(wcfg.aurora_window, 5)
            win32gui.SetForegroundWindow(wcfg.aurora_window)
        elif event.type == pygame.QUIT:
            wcfg.aurora.terminate()

# Cleanup
logging.info('Starting cleanup')
if wcfg.portable:
    subprocess.Popen('regsvr32 /s /u MSSTDFMT.DLL').wait()
try:
    os.remove(os.path.splitdrive(os.getcwd())[0] + os.path.sep + 'Logs')
except:
    pass
winreg.SetValueEx(wcfg.registry, 'sDecimal', 0, 1, icfg['DEFAULT']['regdecimal'][1:-1])
winreg.SetValueEx(wcfg.registry, 'sThousand', 0, 1, icfg['DEFAULT']['regthousand'][1:-1])
wcfg.registry.Close()
with open('Aurora.ini', 'w') as configfile:
    icfg.write(configfile)
