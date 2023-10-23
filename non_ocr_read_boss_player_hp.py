import numpy as np
import cv2
from mss import mss


bounding_box = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
sct = mss()
while True:
    sct_img = sct.grab(bounding_box)
    screen_cap = np.array(sct_img)


    if cv2.threshold(screen_cap[984, 617], 150, 255, cv2.THRESH_BINARY)[1][0][0] == 255:
        print("yes")

    looky_here_area = screen_cap[995:1015, 655:1275]

    blue, green, red, _ = cv2.split(looky_here_area)

    red = cv2.blur(red, (5, 5))
    red = cv2.threshold(red, 50, 255, cv2.THRESH_BINARY)[1]

    # red = cv2.bitwise_not(red)
    red = cv2.resize(red, (100, 10))

    index = 0
    for pixel in red[5, :]:
        if (pixel == 0):
            # print(index)
            break
        index += 1

    cv2.imshow('screen', red)

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break