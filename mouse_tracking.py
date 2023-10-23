import numpy as np
import cv2
from mss import mss
import math
import time
from pynput.mouse import Button, Controller as MouseController

mouse = MouseController()

bounding_box = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
sct = mss()

time.sleep(1)
mouse.press(Button.left)

while True:
    sct_img = sct.grab(bounding_box)
    screen_cap = np.array(sct_img)

    visible_area = screen_cap[160:920]

    blue, green, red, not_sure = cv2.split(visible_area)

    red = cv2.blur(red, (10, 10))
    blue = cv2.blur(blue, (10, 10))
    green = cv2.blur(green, (10, 10))
    average = (blue + green) / 2
    red = red - average
    red = cv2.blur(red, (50, 50))
    red = cv2.threshold(red, 100, 255, cv2.THRESH_BINARY)[1]

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
        cursor = (int(960 + 100 * math.cos(angle)), int(540 + 100 * math.sin(angle)))
        mouse.position = cursor
    except:
        print("Error")

    # display the image
    cv2.imshow("Image", inverted)


    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break