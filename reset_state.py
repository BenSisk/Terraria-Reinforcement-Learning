from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
import time

keyboard = KeyboardController()
mouse = MouseController()

def reset():
    keyboard.press('t')
    time.sleep(0.1)
    keyboard.release('t')

    mouse.position = (960, 1070)
    time.sleep(0.1)
    mouse.press(Button.left)
    time.sleep(0.1)
    mouse.release(Button.left)

    time.sleep(0.2)
    mouse.position = (630, 1030)
    time.sleep(0.1)
    mouse.press(Button.left)
    time.sleep(0.1)
    mouse.release(Button.left)
    time.sleep(0.1)
    mouse.press(Button.left)
    time.sleep(0.1)
    mouse.release(Button.left)
    time.sleep(0.2)

    mouse.position = (960, 980)
    time.sleep(0.1)
    mouse.press(Button.left)
    time.sleep(0.1)
    mouse.release(Button.left)

    time.sleep(0.2)
    mouse.position = (960, 540)

    time.sleep(0.1)
    keyboard.press('4')
    time.sleep(0.1)
    keyboard.release('4')
    time.sleep(0.2)
    mouse.press(Button.left)
    time.sleep(0.1)
    mouse.release(Button.left)


    time.sleep(0.2)
    keyboard.press('1')
    time.sleep(0.1)
    keyboard.release('1')


time.sleep(5)
reset()