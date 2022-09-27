from constant import *
import numpy as np
import pytesseract
from pytesseract import Output
import cv2
import math

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
        calendarImg = self.cropImage(img, results)

        calendarAnalysis = pytesseract.image_to_data(calendarImg, output_type=Output.DICT)

        roomsName = self.getRoomsName(calendarImg, calendarAnalysis)

        # roomsAvailability = self.getRoomAvailability("CRX-C520", calendarImg)

        # roomsAvailability = self.getAllRoomsAvailability(roomsName, calendarImg)

        # return roomsAvailability

    def getRoomAvailability(self, roomName, img):

        # Analyze the cropped img to get only the timeslots
        resultsCalendarImg = pytesseract.image_to_data(img, output_type=Output.DICT)

        # Get timeslot for the timetable and their coordinates on the screencapture
        timeslot = self.getTimeSlot(img, resultsCalendarImg)

        # Get roomsSlot for the timetable and their coordinates
        roomNameImg = self.cropRoomName(img, resultsCalendarImg)

        resultsRoomNameImg = pytesseract.image_to_data(roomNameImg, output_type=Output.DICT)

        roomsSLot = self.getRoomCoordinate(roomNameImg, resultsRoomNameImg)

        roomAvailability = self.getRoomAvailabilityWithSlot('CRX-C523', timeslot, roomsSLot, img)

        return roomAvailability

    def getRoomsName(self, img, analyzedResults):

        roomNameImg = self.cropRoomName(img, analyzedResults)

        roomName = []

        for i in range(0, len(analyzedResults['text'])):

            text = analyzedResults['text'][i]

            if self.isStringARoom(text):
                roomName.append(text)

        return roomName

    def getAllRoomsAvailability(self, roomsName, img):

        roomsAvailability = {}

        for room in roomsName:

            availability = self.getRoomAvailability(room, img)

            roomsAvailability[room] = availability


        return roomsAvailability

    def findIdOfDateWithYear(self, texts):
        id = 0

        for i in range(0, len(texts)):

            if self.isDate(texts[i]):
                id = i
                break

        if not self.isDate(texts[id]):
            return None

        return id

    def getRoomAvailabilityWithSlot(self, roomName, timeSlot, roomSlot, img):

        roomId = self.getRoomId(roomSlot, roomName)

        roomBoundingBox = roomSlot[roomId][1]

        roomImg = self.cropRoomSlotFromImg(img, roomBoundingBox)

        # copyRoomImg = roomImg.copy()

        # textRoomImg = self.addTimeSlotTextToImg(copyRoomImg, timeSlot)
        # self.showImg(textRoomImg)

        # slotWithText = self.addTimeSlotTextToImg(roomImg, timeSlot)

        timeSlotStatus = {}

        for i in range (0, len(timeSlot)):

            timeSlotName = timeSlot[i][0]

            status = self.getTimeSlotStatus(roomImg, timeSlotName, timeSlot)

            timeSlotStatus[timeSlotName] = status

        return timeSlotStatus

    def getTimeSlotStatus(self, img, timeSlotName, timeSlot):
        # Get the status of the requested timeslot

        id = self.getTimeSlotId(timeSlotName, timeSlot)
        timeSlotBoundingBox = timeSlot[id][1]

        timeSlotStatusImg = self.cropImgWithBoundingBox(img, timeSlotBoundingBox)

        if self.isTimeSlotFull(timeSlotStatusImg):
            return FULLY_BOOK_INDICATOR

        elif self.isTimeSlotFullyReservable(timeSlotStatusImg):
            return FULLY_RESERVABLE_INDICATOR

        elif self.isFirstHalfReservable(timeSlotStatusImg):
            return FIRST_HALF_INDICATOR

        elif self.isSecondHalfReservable(timeSlotStatusImg):
            return SECOND_HALF_INDICATOR

    def isTimeSlotFull(self, timeSlotImg):

        if self.arePixelsBlue(timeSlotImg):
            return True

        return False

    def isTimeSlotFullyReservable(self, timeSlotImg):

        if self.arePixelsWhite(timeSlotImg):
            return True

        return False

    def isFirstHalfReservable(self, timeSlotImg):

        leftPortion = self.cropPortionsLeftAndRightTimeslot(timeSlotImg)[0]

        if self.arePixelsWhite(leftPortion):
            return True

        return False

    def isSecondHalfReservable(self, timeSlotImg):

        rightPortion = self.cropPortionsLeftAndRightTimeslot(timeSlotImg)[1]

        if self.arePixelsWhite(rightPortion):
            return True

        return False

    def isDate(self, string):

        chars = list(string.split('/'))

        if  len(chars) == 3:
            return True

        return False

    def cropPortionsLeftAndRightTimeslot(self, img):

        width = img.shape[1]
        height = img.shape[0]

        leftPortion = self.cropImgWithCoordinates(img, 5, 5, 20, height-3)

        rightPortion = self.cropImgWithCoordinates(img, width-20, 5, width, height-3)

        return (leftPortion, rightPortion)

    def arePixelsBlue(self, img):

        hsvImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hue, sat, val = cv2.split(img)

        pixelNumber = len(hsvImg) * len(hsvImg[0])

        pixelCount = {'blue':0, 'green':0, 'red':0}

        if self.arePixelsWhite(img):
            return False

        for y in range(0, len(hsvImg)):

            for x in range(0, len(hsvImg[y])):

                pixel = hsvImg[y][x]
                h = pixel[0] * 2
                v = pixel[2]

                if 190 < h < 230:
                    pixelCount['blue'] += 1

                elif 80 < h < 100:
                    pixelCount['green'] += 1

                elif h < 10:
                    pixelCount['red'] += 1

        if pixelCount['red'] > 0 or pixelCount['green'] > 0:

            return False


        return True

    def arePixelsWhite(self, img):

        if np.mean(img) >= 250:

            return True

        else:

            return False

    def cropImgWithCoordinates(self, img, x, y, width, height):

        width = int(width)
        height = int(height)

        cropImg = img[y:y+height, x:x+width]

        return cropImg

    def getTimeSlotId(self, timeSlotName, timeSlot):
        # Get the id of the timeslot requested

        for i in range(0, len(timeSlot)):

            if timeSlot[i][0] == timeSlotName:
                return i

    def addTimeSlotTextToImg(self, img, timeSlot):

        pixelOffset = 10

        for i in range(0, len(timeSlot)):

            text = timeSlot[i][0]

            orgX = timeSlot[i][1]['x']['left']
            orgY = timeSlot[i][1]['y']['top'] + pixelOffset

            font = cv2.FONT_HERSHEY_SIMPLEX
            org = (orgX, orgY)
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2
            imgWithTimeSlot = cv2.putText(img, text, org, font,
                              fontScale, color,
                              thickness, cv2.LINE_AA)

        return imgWithTimeSlot

    def drawBoxAroundTimeSlot(self, img, timeSlot):

        for i in range(0, len(timeSlot)):

            left = timeSlot[i][1]['x']['left']
            top = timeSlot[i][1]['y']['top']
            width = timeSlot[i][1]['x']['width']
            height = timeSlot[i][1]['y']['height']

            imgWithBoundingBox = cv2.rectangle(img,
                                               (left, top),
                                               (left + width, top + height),
                                               (0, 0, 255),
                                               2)

        return imgWithBoundingBox

    def getRoomId(self, roomSlot, roomName):
        # get the room id from the roomSlot Array

        for i in range(0, len(roomSlot)) :

            if roomName in roomSlot[i]:
                return i

    def cropRoomName(self, img, analyzedResults):

        id = self.findIdOfDateWithYear(analyzedResults['text'])

        pixelOffset = 10

        boundingBox = self.getTextBoundingBox(analyzedResults, id)

        imgHeight = img.shape[0]
        left = boundingBox['x']['left']
        top = boundingBox['y']['top']
        width = boundingBox['x']['width']
        height = boundingBox['y']['height']

        cropImg = img[0:imgHeight, 0:left + width + pixelOffset]

        return cropImg

    def getRoomCoordinate(self, img, analyzedResults):
        # Get the coordinates of all the rooms in the present screenCapture

        roomsSlot = []

        self.cropRoomName(img, analyzedResults)

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
                self.addWidthOffsetToBoundingBox(boundBox)

                timeSlot.append((time, boundBox))

        return timeSlot

    def addWidthOffsetToBoundingBox(self, boundBox):

        boundBox['x']['width'] += boundBoxPixelOffset

    def cropRoomSlotFromImg(self, img, boundingBox):
        # Crop room slot from img with the provided bounding box

        imgWidth = img.shape[1]
        top = boundingBox['y']['top']
        height = boundingBox['y']['height']
        pixelOffset = 20

        cropImg = img[top-pixelOffset:top+height+pixelOffset, 0:imgWidth]

        return cropImg

    def cropImgWithBoundingBox(self, img, boundingBox):

        # Crop room slot from img with the provided bounding box
        top = boundingBox['y']['top']
        height = boundingBox['y']['height']
        left = boundingBox['x']['left']
        width = boundingBox['x']['width']

        cropImg = img[top:top + height, left: left + width]

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