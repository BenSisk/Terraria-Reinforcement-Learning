from mss import mss
import cv2

from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
import time

import numpy as np

import pytesseract


class GameEnvironment:
    keyboard = KeyboardController()
    mouse = MouseController()
    previous_player_hp = 0
    previous_boss_hp = 0
    image_size = (192, 81)
    BossDespawnCount = 0

    
    def __init__(self):
        self.bounding_box = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
        self.sct = mss()

    def reset(self):
        self.mouse.release(Button.left)
        time.sleep(1)
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

        time.sleep(15)

        self.keyboard.press('t')
        time.sleep(0.1)
        self.keyboard.release('t')

        time.sleep(4)

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
        
        time.sleep(1)
        self.mouse.press(Button.left)

    def step(self, action):
        
        if (action == 0):
            self.keyboard.press(Key.space)
            time.sleep(0.01)
            self.keyboard.release(Key.space)
        elif (action == 1):
            self.keyboard.press('a')
            time.sleep(0.01)
            self.keyboard.release('a')
        elif (action == 2):
            self.keyboard.press('s')
            time.sleep(0.01)
            self.keyboard.release('s')
        elif (action == 3):
            self.keyboard.press('d')
            time.sleep(0.01)
            self.keyboard.release('d')
        elif (action == 4):
            self.mouse.position = (760, 540)
        elif (action == 5):
            self.mouse.position = (760, 340)
        elif (action == 6):
            self.mouse.position = (960, 340)
        elif (action == 7):
            self.mouse.position = (1160, 340)
        elif (action == 8):
            self.mouse.position = (1160, 540)
        elif (action == 9):
            self.mouse.position = (1160, 740)
        elif (action == 10):
            self.mouse.position = (960, 740)
        elif (action == 11):
            self.mouse.position = (760, 740)

        screen = self.get_screen()
        state = self.red_and_flatten(screen)
        player_hp, boss_hp = self.get_hp(screen)

        reward = 0
        done = False

        if (player_hp == -1 or boss_hp == -1):
            reward = 0
        elif (player_hp == 0):
            reward = -1000
            done = True
        elif (boss_hp == 0):
            reward = 1000
            done = True
        
        

        if (player_hp < self.previous_player_hp):
            reward = reward - 1
        if (boss_hp < self.previous_boss_hp):
            reward = reward + 1

        if (player_hp != -1):
            self.previous_player_hp = player_hp

        if (boss_hp == -1):
            self.BossDespawnCount += 1
        else:
            self.previous_boss_hp = boss_hp
            self.BossDespawnCount = 0
        
        if (self.BossDespawnCount > 5):
            reward = -1000
            done = True

        return state, reward, done

    def red_and_flatten(self, img):
        visible_area = img[160:970]
        _, _, red, _ = cv2.split(visible_area)
        red = cv2.blur(red, (10, 10))
        red = cv2.threshold(red, 50, 255, cv2.THRESH_BINARY)[1]
        red = cv2.bitwise_not(red)
        red = cv2.resize(red, self.image_size)
        state = red.flatten()
        return state

    def get_screen(self):
        sct_img = self.sct.grab(self.bounding_box)
        screen = np.array(sct_img)
        return screen
    
    def get_hp(self, img):
        boss_hp = self.ocr(image=(img[995:1020, 850:1070]))
        player_hp = self.ocr(image=(img[0:28, 1655:1767]))
        return player_hp, boss_hp
    
    def ocr(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)[1]

        ocr_result = pytesseract.image_to_string(image, lang='eng', \
            config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789/')
        
        try:
            ocr_result = ocr_result.split('/')[0]
            ocr_result = int(ocr_result)
        except:
            ocr_result = -1
            print("Error parsing OCR result: ", ocr_result)
        return ocr_result