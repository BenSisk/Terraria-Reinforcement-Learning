import numpy as np
import cv2
from mss import mss

def check_hp_bar(image, flipped=False):
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

bounding_box = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
sct = mss()
while True:
    sct_img = sct.grab(bounding_box)
    screen_cap = np.array(sct_img)

    boss_alive = False
    player_alive = False

    if cv2.threshold(screen_cap[984, 617], 150, 255, cv2.THRESH_BINARY)[1][0][0] == 255:
        boss_alive = True
        # print("Boss is alive")

    if screen_cap[45, 1834, 2] > 150:
        player_alive = True
        print("Player is alive")
    else:
        print("Player is dead")

    if(boss_alive):
        boss_hp = check_hp_bar(screen_cap[995:1015, 655:1275])
    
    player_hp_bar = check_hp_bar(np.flip(screen_cap[40:50, 1500:1834]))

    # print("Boss HP: " + str(boss_hp))
    # print("Player HP: " + str(player_hp_bar))

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break