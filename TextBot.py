
import numpy as np
import pytesseract
from pytesseract import Output
import cv2

class TextBot():

    def analyze(self, filePath):

        img = cv2.imread(filePath)

        results = pytesseract.image_to_data(img, output_type=Output.DICT)

        cropImg = self.cropImage(img, results)

        resultsCropImg = pytesseract.image_to_data(cropImg, output_type=Output.DICT)

        timeslot = self.getTimeSlot(cropImg, resultsCropImg)


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

        cv2.rectangle(img, (left, top), (left + width, top + height), (0, 0, 255), 2)

        self.showImg(img)

    def getTimeSlot(self, img, analyzedResults):

        imgWidth = img.shape[1]

        analyzedText = analyzedResults['text']

        wordIdToCrop = self.findIdOfDate(analyzedText)

        pixelOffset = 15

        boxLeft = analyzedResults['left'][wordIdToCrop]
        boxTop = analyzedResults['top'][wordIdToCrop]
        boxHeight = analyzedResults['height'][wordIdToCrop]

        timeSlot = []

        availableTimeImg = img[0:boxHeight+boxTop+pixelOffset, 0:imgWidth]

        processImg = self.preprocessImg(availableTimeImg)

        timeAnalyzed = pytesseract.image_to_data(processImg, output_type=Output.DICT)

        for i in range(0, len(timeAnalyzed['text'])):

            confidenceLevel = timeAnalyzed['conf'][i]

            if confidenceLevel >= 60:

                time = timeAnalyzed['text'][i]

                boundBox = self.getTextBoundingBox(timeAnalyzed, i)

                timeSlot.append((time, boundBox))

        return timeSlot

    def cropImage(self, img, analyzedResults):

        analyzedText = analyzedResults['text']

        # Find the id of the text to crop the image
        wordIdToCrop = self.findIdOfDate(analyzedText)

        imgWidth = img.shape[1]
        imgHeight = img.shape[0]

        pixelOffset = 15

        boxLeft = analyzedResults['left'][wordIdToCrop]
        boxTop = analyzedResults['top'][wordIdToCrop]
        boxHeight = analyzedResults['height'][wordIdToCrop]

        cropImg = img[boxTop - pixelOffset:imgHeight , boxLeft-pixelOffset:imgWidth]

        return cropImg

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

        thresh = 165
        max = 255

        th, threshImg = cv2.threshold(invert, thresh, max, cv2.THRESH_BINARY_INV)

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