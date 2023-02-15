import pyautogui as gui
import time
import subprocess


def click(x, y): gui.click(x, y)


def wait(t): time.sleep(t)


def open_chrome():
    gui.keyDown('command')
    gui.keyDown('space')
    gui.keyUp('space')
    gui.keyUp('command')
    wait(0.5)
    gui.write('Google Chrome')
    gui.press('enter')


# Youtube
def upload_to_youtube():
    gui.hotkey('command', 't')
    wait(1)
    gui.write('studio.youtube.com')
    gui.press('enter')
    wait(20)
    gui.press('tab', presses=36)
    wait(1)
    gui.press('enter')
    wait(1)
    gui.press('enter')
    wait(1)
    gui.press('tab', presses=3)
    wait(1)
    gui.press('enter')
    wait(1)
    gui.press('down')
    wait(1)
    gui.press('enter')
    wait(5)
    click(1194, 905)
    wait(1)
    click(1194, 905)
    wait(1)
    click(1194, 905)
    wait(1)
    gui.press('down', presses=2)
    click(1194, 905)


def upload_to_ig():
    gui.hotkey('command', 't')
    wait(1)
    gui.write('www.instagram.com')
    gui.press('enter')
    wait(20)
    gui.press('tab', presses=8)
    gui.press('enter')
    wait(1)
    gui.press('tab', presses=1)
    gui.press('enter')
    wait(1)
    gui.press('down')
    gui.press('enter')
    wait(5)
    gui.press('tab', presses=2)
    gui.press('enter')
    wait(1)
    gui.press('tab', presses=2)
    gui.press('enter')
    wait(1)
    gui.press('tab', presses=2)
    gui.press('enter')


# TikTok
def upload_to_tiktok():
    gui.hotkey('command', 't')
    wait(1)
    gui.write('https://www.tiktok.com/upload')
    gui.press('enter')
    wait(20)
    gui.press('tab', presses=5)
    gui.press('enter')
    wait(1)
    gui.press('down')
    gui.press('enter')
    wait(40)
    gui.press('tab', presses=8)
    gui.press('enter')


# Run PHP Script
out = subprocess.call("docker-compose run php81-service php index.php", shell=True)
wait(1)
if out == 0:
    open_chrome()
    upload_to_youtube()
    upload_to_ig()
    upload_to_tiktok()
else:
    print("PHP script failed :(")
