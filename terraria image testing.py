import numpy as np
import cv2
from mss import mss
from PIL import Image

import pytesseract

bounding_box = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}

sct = mss()

def ocr(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)[1]

    ocr_result = pytesseract.image_to_string(img, lang='eng', \
           config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789/')

    return ocr_result

while True:
    sct_img = sct.grab(bounding_box)
    screen_cap = np.array(sct_img)
    boss_hp_image = screen_cap[995:1020, 850:1070]
    player_hp_image = screen_cap[0:28, 1655:1767]
    print("Player: " + ocr(player_hp_image))
    print("Boss:" + ocr(boss_hp_image))

    looky_here_area = screen_cap[160:970]

    blue, green, red, not_sure = cv2.split(looky_here_area)

    red = cv2.blur(red, (10, 10))
    red = cv2.threshold(red, 50, 255, cv2.THRESH_BINARY)[1]

    red = cv2.bitwise_not(red)
    red = cv2.resize(red, (80, 45))

    cv2.imshow('screen', red)

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break