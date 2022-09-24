
import numpy as np
import pytesseract
from pytesseract import Output
import cv2

class TextBot():

    def analyze(self):

        testFilePath = 'testImage.jpeg'
        screenFilePath = 'screencapture/booking_schedule_full.png'

        img = cv2.imread(screenFilePath)

        results = pytesseract.image_to_data(img, output_type=Output.DICT)

        print(results['text'])

        # for i in range(0, len(results['text'])):
        #     # check confidence level
        #
        #     confidenceLevel = int(results['conf'][i])
        #
        #     if confidenceLevel >= 80:
        #
        #         # Get text
        #         text = results['text'][i]
        #
        #         # getting coordinates of the box
        #         x = results['left'][i]
        #         y = results['top'][i]
        #
        #         # get width and height of text box
        #         w = results['width'][i]
        #         h = results['height'][i]
        #
        #         # draw box around word
        #         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        #
        #         # add text top of the rectangle
        #         cv2.putText(img, text,
        #                     (x, y - 10),
        #                     cv2.FONT_HERSHEY_SIMPLEX,
        #                     0.5,
        #                     (0,0, 200),
        #                     2)
        #
        # cv2.imshow('text', img)
        #
        # cv2.setWindowProperty('text', cv2.WND_PROP_TOPMOST, 1)
        #
        # cv2.waitKey()

    def findIdOfDate(self, texts):

        # This id will be used to crop our the schedule screen capture image

        id = 0

        for i in range(0, len(texts)):

            if self.isWeekday(texts[i]):

                id = i
                break

        if not self.isWeekday(texts[id]):
            return None

        return id

    def drawBoxAroundText(self, id, analyzedResults, img):

        # getting coordinates of the box
        x = analyzedResults['left'][id]
        y = analyzedResults['top'][id]

        # get width and height of text box
        w = analyzedResults['width'][id]
        h = analyzedResults['height'][id]

        # draw box around word
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('test', img)

        cv2.setWindowProperty('test', cv2.WND_PROP_TOPMOST, 1)

        cv2.waitKey()

    def drawAroundBoundingBox(self, img, boundBox):

        top = boundBox['y']['top']
        left = boundBox['x']['left']
        width = boundBox['x']['width']
        height = boundBox['y']['height']

        cv2.rectangle(img, (left, top), (left + width, top + height), (255, 255, 0), 2)

        self.showImg(img)

    def getTimeSlot(self, img):

        results = pytesseract.image_to_data(img, output_type=Output.DICT)

        analyzedText = results['text']

        # Find the id of the text to crop the image
        wordIdToCrop = self.findIdOfDate(analyzedText)

        imgWidth = img.shape[1]

        pixelOffset = 15

        boxLeft = results['left'][wordIdToCrop]
        boxTop = results['top'][wordIdToCrop]
        boxHeight = results['height'][wordIdToCrop]

        timeSlot = []

        availableTimeImg = img[boxTop - pixelOffset:boxHeight + boxTop + pixelOffset, boxLeft - pixelOffset:imgWidth]

        processImg = self.preprocessImg(availableTimeImg)

        timeAnalyzed = pytesseract.image_to_data(processImg, output_type=Output.DICT)

        for i in range(0, len(timeAnalyzed['text'])):

            confidenceLevel = timeAnalyzed['conf'][i]

            if confidenceLevel >= 80:

                time = timeAnalyzed['text'][i]

                boundBox = self.getTextBoundingBox(timeAnalyzed, i)

                timeSlot.append((time, boundBox))

        print(timeSlot[0][1])

        self.drawAroundBoundingBox(processImg, timeSlot[0][1])

        return timeSlot

    def cropImage(self):

        filePath = 'screencapture/booking_schedule_full.png'

        img = cv2.imread(filePath)

        results = pytesseract.image_to_data(img, output_type=Output.DICT)

        analyzedText = results['text']

        timeSlot = self.getTimeSlot(img)

    def getTextBoundingBox(self, analyzedResults, id):

        boxLeft = analyzedResults['left'][id]
        boxTop = analyzedResults['top'][id]
        boxHeight = analyzedResults['height'][id]
        boxWidth = analyzedResults['width'][id]

        boundingBox = {'x':{'left':boxLeft, 'width':boxWidth},
                       'y':{'top':boxTop, 'height':boxHeight}
                       }

        return boundingBox

    def preprocessImg(self, img):

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        invert = cv2.bitwise_not(gray)

        thresh = 180
        max = 255

        th, threshImg = cv2.threshold(invert, thresh, max, cv2.THRESH_BINARY)

        return threshImg

    def showImg(self, img):

        cv2.imshow('window', img)

        cv2.setWindowProperty('window', cv2.WND_PROP_TOPMOST, 1)

        cv2.waitKey()

    def isWeekday(self, string):

        weekDayEng = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        weekDayFr = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']

        # we remove coma from the text

        string = string.replace(',', '')

        for i in range(0, len(weekDayEng)):

            day = (weekDayFr[i], weekDayEng[i])

            capitalize = (day[0].title(), day[1].title())
            allCaps = (day[0].upper(), day[1].upper())

            if string == day[0] or string == day[1] or string == capitalize[0] or string == capitalize[1] or string == allCaps[0] or string == allCaps[1]:

                return True

        return False