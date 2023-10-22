import numpy as np
import cv2
from mss import mss
from PIL import Image

import pytesseract

bounding_box = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}

sct = mss()

while True:
    sct_img = sct.grab(bounding_box)
    cv2_image = np.array(sct_img)
    cropped_image = cv2_image[995:1020, 850:1070]

    # cropped_image = cv2.GaussianBlur(cropped_image, (1, 1), 0)
    cropped_image = cv2.resize(cropped_image, None, fx = 2, fy = 2)
    cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    cropped_image = cv2.threshold(cropped_image, 150, 255, cv2.THRESH_BINARY)[1]

    ocr_result = pytesseract.image_to_string(cropped_image, lang='eng', \
           config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789/')
    print(ocr_result)

    cv2.imshow('screen', cropped_image)

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break