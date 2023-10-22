from mss import mss
import cv2

from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
import time

import numpy as np



class GameEnvironment:
    keyboard = KeyboardController()
    mouse = MouseController()
    
    def __init__(self):
        self.bounding_box = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
        self.sct = mss()

    def reset(self):
        self.keyboard.press('t')
        time.sleep(0.1)
        self.keyboard.release('t')

        self.mouse.position = (960, 1070)
        time.sleep(0.1)
        self.mouse.press(Button.left)
        time.sleep(0.1)
        self.mouse.release(Button.left)

        time.sleep(0.2)
        self.mouse.position = (630, 1030)
        time.sleep(0.1)
        self.mouse.press(Button.left)
        time.sleep(0.1)
        self.mouse.release(Button.left)
        time.sleep(0.1)
        self.mouse.press(Button.left)
        time.sleep(0.1)
        self.mouse.release(Button.left)
        time.sleep(0.2)

        self.mouse.position = (960, 980)
        time.sleep(0.1)
        self.mouse.press(Button.left)
        time.sleep(0.1)
        self.mouse.release(Button.left)

        time.sleep(0.2)
        self.mouse.position = (960, 540)

        time.sleep(0.1)
        self.keyboard.press('4')
        time.sleep(0.1)
        self.keyboard.release('4')
        time.sleep(0.2)
        self.mouse.press(Button.left)
        time.sleep(0.1)
        self.mouse.release(Button.left)


        time.sleep(0.2)
        self.keyboard.press('1')
        time.sleep(0.1)
        self.keyboard.release('1')

    def step(self, action):
        sct_img = self.sct.grab(self.bounding_box)
        screen_cap = np.array(sct_img)
        looky_here_area = screen_cap[160:970]
        _, _, red, _ = cv2.split(looky_here_area)
        red = cv2.blur(red, (10, 10))
        red = cv2.threshold(red, 50, 255, cv2.THRESH_BINARY)[1]
        red = cv2.bitwise_not(red)
        red = cv2.resize(red, (800, 500))
        state = red.flatten()

        print(action)

        return state, 1, False