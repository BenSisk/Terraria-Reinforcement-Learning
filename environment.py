from mss import mss
import cv2

from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
import time

import numpy as np

import math


class GameEnvironment:
    keyboard = KeyboardController()
    mouse = MouseController()
    previous_player_hp = 0
    previous_boss_hp = 0
    image_size = (192, 81)
    Low_HP_Boss = False
    startTime = 0
    previous_angle = 0

    
    def __init__(self):
        self.bounding_box = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
        self.sct = mss()

    def reset(self):
        self.mouse.release(Button.left)
        self.keyboard.release(Key.space)
        self.keyboard.release('a')
        self.keyboard.release('s')
        self.keyboard.release('d')
        self.previous_boss_hp = 0
        self.previous_player_hp = 0
        self.Low_HP_Boss = False

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
        self.mouse.position = (700, 1030)
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

        time.sleep(0.2)
        self.keyboard.press('h')
        time.sleep(0.1)
        self.keyboard.release('h')
        
        time.sleep(0.2)
        self.mouse.press(Button.left)

        self.startTime = time.time()


    def step(self, qvalues):
        if (qvalues[0] > 50):
            self.keyboard.press(Key.space)
        else:
            self.keyboard.release(Key.space)

        if (qvalues[1] > 50):
            self.keyboard.press('a')
        else:
            self.keyboard.release('a')

        if (qvalues[2] > 50):
            self.keyboard.press('s')
        else:
            self.keyboard.release('s')

        if (qvalues[3] > 50):
            self.keyboard.press('d')
        else:
            self.keyboard.release('d')

        screen = self.get_screen()
        player_alive, player_hp, boss_alive, boss_hp = self.get_hp(screen)
        x, y, angle = self.get_mr_blobby(screen[160:920])
        state = np.array([x, y])

        if (angle == -1):
            angle = self.previous_angle
        else:
            self.previous_angle = angle

        self.mouse.position = (int(960 + (100 * math.cos(angle))), int(540 + 50 +(100 * math.sin(angle))))
        
        reward = 0
        done = False

        if (player_hp < self.previous_player_hp):
            reward = reward - 3
        if (boss_hp < self.previous_boss_hp):
            reward = reward + 1

        self.previous_player_hp = player_hp
        self.previous_boss_hp = boss_hp

        if (boss_alive and boss_hp == 0):
            self.Low_HP_Boss = True
        elif (boss_alive == False and self.Low_HP_Boss):
            reward = 100
            done = True
        elif (boss_alive == False):
            reward = -100
            done = True
        
        if (player_alive == False):
            reward = -100
            done = True

        if (done):
            reward = reward - round(((time.time() - self.startTime) / 10))

        return state, reward, done


    def get_screen(self):
        sct_img = self.sct.grab(self.bounding_box)
        screen = np.array(sct_img)
        return screen
    
    def get_hp(self, screen):
        if cv2.threshold(screen[984, 617], 150, 255, cv2.THRESH_BINARY)[1][0][0] == 255:
            boss_alive = True
            # print("Boss is alive")
        else:
            boss_alive = False
            # print("Boss is dead")

        if screen[45, 1834, 2] > 150:
            player_alive = True
            # print("Player is alive")
        else:
            player_alive = False
            # print("Player is dead")

        boss_hp = self.check_hp_bar(screen[995:1015, 655:1275])
        player_hp = self.check_hp_bar(np.flip(screen[40:50, 1500:1834]))
        return player_alive, player_hp, boss_alive, boss_hp
    
    
    def check_hp_bar(self, image):
        _, _, red, _ = cv2.split(image)

        red = cv2.blur(red, (5, 5))
        red = cv2.threshold(red, 50, 255, cv2.THRESH_BINARY)[1]
        red = cv2.resize(red, (100, 1))

        index = 0
        for pixel in red[0, :]:
            if (pixel == 0):
                break
            index += 1

        return index
    
    def get_mr_blobby(self, visible_area):
        blue, green, red, _ = cv2.split(visible_area)

        blue = cv2.blur(blue, (10, 10))
        green = cv2.blur(green, (10, 10))
        average = (blue + green) / 2

        red = cv2.blur(red, (10, 10)) - average
        red = cv2.blur(red, (30, 30))
        red = cv2.threshold(red, 80, 255, cv2.THRESH_BINARY)[1]

        red = cv2.resize(red, (800, 500))

        # calculate moments of binary image
        M = cv2.moments(red)
        
        inverted = np.invert(np.array(red, dtype=np.uint8))

        try:
            # calculate x,y coordinate of center
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        

            # put text and highlight the center
            cv2.circle(inverted, (cX, cY), 5, (100, 100, 100), -1)
            cv2.putText(inverted, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 2)
        
        
            angle = math.atan2((cY - 250), (cX - 400))
            # print(angle)
            # return cX, cY, angle
            return cX, cY, angle
        except:
            # print("Error")
            return -1, -1, -1
