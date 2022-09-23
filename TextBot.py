
import numpy as np
import pytesseract
import cv2


class TextBot():

    def analyze(self):

        filePath = 'testImage.jpeg'

        img = np.array(cv2.imread(filePath))

        text = pytesseract.image_to_string(img)

        print(text)

