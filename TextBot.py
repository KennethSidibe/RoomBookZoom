
import numpy as np
import pytesseract
from pytesseract import Output
import cv2

class TextBot():


    def isStringARoom(self, string):
        # check if provided string is a reservable room by the system
        # Like FTX-514

        if len(string) > 10 or len(string) < 7:
            return False

        rooms = {
                'CRX' : ['CRX-C520', 'CRX-C521', 'CRX-C522', 'CRX-C523', 'CRX-C524',
                         'CRX-C525', 'CRX-C526', 'CRX-C527', 'CRX-C528','CRX-C529',
                         'CRX-C541', 'CRX-C542', 'CRX-C543', 'CRX-C544', 'CRX-C545'],

                 'FTX' : ['FTX-514', 'FTX-515', 'FTX-525A', 'FTX-525B',
                  'FTX-525C', 'FTX-525D', 'FTX-525G', 'FTX-525H', 'FTX-525J'],

                 'MRT' : ['MRT-404', 'MRT-405', 'MRT-406', 'MRT-407', 'MRT-408', 'MRT-409',
                          'MRT-410', 'MRT-411', 'MRT-412','MRT-415', 'MRT-417', 'MRT-418'],

                 'RGN' : ['RGN-1020J', 'RGN-1020K', 'RGN-1020L',
                          'RGN-1020M', 'RGN-1020N', 'RGN-1020P']
                 }

        chars = []
        Buildings = rooms.keys()

        for i in range(0, 3):
            chars.append(string[i])

        charFromString = ''.join(chars)

        if not (charFromString in rooms):
            return False

        roomsForBuilding = rooms[charFromString]

        if string in roomsForBuilding:
            return True

        else:
            return False

    def analyze(self, filePath):

        # Loading the screencapture
        img = cv2.imread(filePath)

        # Analyse the screencapture to find the timeTable coordinate
        results = pytesseract.image_to_data(img, output_type=Output.DICT)

        # crop the img to get only the calendar
        cropImg = self.cropImage(img, results)

        # Analyze the cropped img to get only the timeslots
        resultsCropImg = pytesseract.image_to_data(cropImg, output_type=Output.DICT)

        # Get timeslot for the timetable and their coordinates on the screencapture
        timeslot = self.getTimeSlot(cropImg, resultsCropImg)

        # Get roomSlot for the timetable and their coordinates
        roomsSLot = self.getRoomCoordinate(cropImg, resultsCropImg)

        # Get one singulard roomSlot from whole screencapture
        roomImg = self.cropRoomSlotFromImg(cropImg, roomsSLot[17][1])

        self.showImg(roomImg)

    def getRoomCoordinate(self, img, analyzedResults):
        # Get the coordinates of all the rooms in the present screenCapture

        roomsSlot = []

        for i in range(0, len(analyzedResults['text'])):

            if analyzedResults['conf'][i] >= 60:

                text = analyzedResults['text'][i]

                if self.isStringARoom(text):

                    boundingBox = self.getTextBoundingBox(analyzedResults, i)
                    slot = [text, boundingBox]

                    roomsSlot.append(slot)

        return  roomsSlot

    def findIdOfDate(self, texts):
        # Find the id of the date in the analyzedResults dict

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
        # Draw a box around the text in the current image with the id provided

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
        # Draw a box with the provided bounding box

        top = boundBox['y']['top']
        left = boundBox['x']['left']
        width = boundBox['x']['width']
        height = boundBox['y']['height']

        cv2.rectangle(img, (left, top), (left + width, top + height), (0, 0, 255), 2)

        self.showImg(img)

    def getTimeSlot(self, img, analyzedResults):
        # Get the timeSlot from the current screencapture with their exact coordinates

        imgWidth = img.shape[1]

        analyzedText = analyzedResults['text']

        wordIdToCrop = self.findIdOfDate(analyzedText)

        pixelOffset = 15

        boxLeft = analyzedResults['left'][wordIdToCrop]
        boxTop = analyzedResults['top'][wordIdToCrop]
        boxHeight = analyzedResults['height'][wordIdToCrop]

        timeSlot = []

        availableTimeImg = img[0:boxHeight+boxTop+pixelOffset, 0:imgWidth]

        processImg = self.preprocessTimeSlotImg(availableTimeImg)

        timeAnalyzed = pytesseract.image_to_data(processImg, output_type=Output.DICT)

        for i in range(0, len(timeAnalyzed['text'])):

            confidenceLevel = timeAnalyzed['conf'][i]

            if confidenceLevel >= 60:

                time = timeAnalyzed['text'][i]

                boundBox = self.getTextBoundingBox(timeAnalyzed, i)

                timeSlot.append((time, boundBox))

        return timeSlot

    def cropRoomSlotFromImg(self, img, boundingBox):
        # Crop room slot from img with the provided bounding box

        imgWidth = img.shape[1]
        top = boundingBox['y']['top']
        height = boundingBox['y']['height']
        pixelOffset = 20

        cropImg = img[top-pixelOffset:top+height+pixelOffset, 0:imgWidth]

        return cropImg

    def cropImage(self, img, analyzedResults):
        # Crop the calendar from the screencapture

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
        # Get bounding box of text with the provided id

        boxLeft = analyzedResults['left'][id]
        boxTop = analyzedResults['top'][id]
        boxHeight = analyzedResults['height'][id]
        boxWidth = analyzedResults['width'][id]

        boundingBox = {'x':{'left':boxLeft, 'width':boxWidth},
                       'y':{'top':boxTop, 'height':boxHeight}
                       }

        return boundingBox

    def preprocessTimeSlotImg(self, img):
        # Preprocess img to upgrade text analysis result for current img timeslot

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        invert = cv2.bitwise_not(gray)

        thresh = 165
        max = 255

        th, threshImg = cv2.threshold(invert, thresh, max, cv2.THRESH_BINARY_INV)

        return threshImg

    def showImg(self, img):
        # Show image with wait statement

        cv2.imshow('window', img)

        cv2.setWindowProperty('window', cv2.WND_PROP_TOPMOST, 1)

        cv2.waitKey()

    def isWeekday(self, string):

        # check if string is a weekday works with english and french

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