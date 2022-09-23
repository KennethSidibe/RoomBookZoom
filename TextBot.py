
import numpy as np
import pytesseract
from pytesseract import Output
import cv2

class TextBot():

    def analyze(self):

        filePath = 'testImage.jpeg'

        img = cv2.imread(filePath)

        results = pytesseract.image_to_data(img, output_type=Output.DICT)

        print(results)

        for i in range(0, len(results['text'])):
            # check confidence level

            confidenceLevel = int(results['conf'][i])

            if confidenceLevel >= 80:

                # Get text
                text = results['text'][i]

                # getting coordinates of the box
                x = results['left'][i]
                y = results['top'][i]

                # get width and height of text box
                w = results['width'][i]
                h = results['height'][i]

                # draw box around word
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # add text top of the rectangle
                cv2.putText(img, text,
                            (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0,0, 200),
                            2)

        cv2.imshow('text', img)

        cv2.setWindowProperty('text', cv2.WND_PROP_TOPMOST, 1)

        cv2.waitKey()

