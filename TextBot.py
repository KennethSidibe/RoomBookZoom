from constant import *
import numpy as np
import pytesseract
from pytesseract import Output
import cv2
import math
import time

class TextBot():

    calendarImg = None
    calendarAnalysis = None
    roomNameImg = None
    roomNameAnalysis = None
    roomsName = None
    roomSlot = None
    timeSlot = None
    roomsAvailability = None
    dateCoordinate = None

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

    def isStringATimeSlot(self, string):

        timeSlots = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00',
                    '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00',
                    '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'
                    ]

        for timeSlot in timeSlots:

            if string == timeSlot:

                return True

        return False

    def analyze(self, filePath):

        # Loading the screencapture
        img = cv2.imread(filePath)

        # Analyse the screencapture to find the timeTable coordinate
        wholeImageAnalysis = pytesseract.image_to_data(img, output_type=Output.DICT)

        calendarImg =  self.cropCalendarImage(img)
        self.setCalendarImg(calendarImg)

        calendarAnalysis = pytesseract.image_to_data(self.calendarImg, output_type=Output.DICT)
        self.setCalendarAnalysis(calendarAnalysis)

        # this function generate timeslot and roomSlot
        self.prepareRoomAnalysis()

        # Get the rooms' availability
        roomsAvailability = self.getAllRoomsAvailability()
        self.setRoomsAvailability(roomsAvailability)

        # get the image with the availability Text for test checking
        availabilityImg = self.visualizeRoomsAvailability()

        self.showImg(availabilityImg)

        return roomsAvailability

    def findCropDateCoordinateByHeight(self, screencaptureImg):

        dateId = -1

        imgPortions = self.getAllImagePortion(screencaptureImg)

        for i in range(0, len(imgPortions)):

            imgPortion = imgPortions[i]

            dateId, left, top = self.analyzePortion(imgPortion)

            if dateId != -1:

                imgPortionHeight = imgPortion.shape[0]
                correctedTop = (i) * imgPortionHeight + top

                return left, correctedTop

        return 0, 0

    def findCropDateCoordinateByArea(self, screencaptureImg):

        dateId = -1

        imgPortions = self.portionImageByArea(screencaptureImg)

        dateId, left, top, height, width = self.analyzeAllImgPortions(imgPortions)

        if dateId != -1:

            return left, top, height, width

        # if we could not find the date id, we will narrow our search
        dateId, left, top, height, width = self.doNarrowSearch(screencaptureImg)

        if dateId != -1:
            return left, top, height, width

        return  0, 0, 0, 0

    def doNarrowSearch(self, screencaptureImg):

        dateId = -1
        widthCorrector = 0
        heightCorrector = 0

        for i in range(0, NARROW_SEARCH_MAX_ITERATION):

            dateId, left, top, widthCorrector, heightCorrector, height, width\
                = self.NarrowSearchOfCropDateCoordinate(screencaptureImg, widthCorrector, heightCorrector)

            if dateId != -1:

                return dateId, left, top, height, width

        return -1, 0, 0, 0, 0

    def showAllImgPortions(self, imgPortions):

        for row in imgPortions:

            for img in row:

                self.showImg(img)

    def NarrowSearchOfCropDateCoordinate(self, screenCaptureImg, widthCorrector=0, heightCorrector=0):

        portionWidthCorrector = PORTION_WIDTH_CORRECTOR
        portionHeightCorrector = PORTION_HEIGHT_CORRECTOR + heightCorrector

        dateId = -1

        imgPortions = self.portionImageByArea(screenCaptureImg, portionHeightCorrector, portionWidthCorrector)

        dateId, left, top, width, height = self.analyzeAllImgPortions(imgPortions)

        if dateId != -1:

            return dateId, left, top, 0, 0, height, width

        return -1, 0, 0, 2, 2, 0, 0

    def analyzeAllImgPortions(self, imgPortions):

        for row in range(0, len(imgPortions)):

            for col in range(0, len(imgPortions[row])):

                areaImg = imgPortions[row][col]

                dateId, left, top, height, width = self.analyzePortion(areaImg, (row, col))

                if dateId != -1:
                    return dateId, left, top, height, width

        return -1, 0, 0, 0, 0

    def findCropDateCoordinateByWidth(self, screencaptureImg):

        dateId = -1

        imgPortions = self.getAllImagePortion(screencaptureImg)

        for i in range(0, len(imgPortions)):

            imgPortion = imgPortions[i]

            dateId, left, top = self.analyzePortion(imgPortion)

            if dateId != -1:

                imgPortionHeight = imgPortion.shape[0]
                correctedTop = (i) * imgPortionHeight + top

                return left, correctedTop

        return 0, 0

    def getAllImagePortion(self, screenCaptureImg):

        portions = []
        currTop = 0
        currLeft = 0

        for i in range(0, PORTION_HEIGHT_DIVISOR):

            portionImg, currLeft = self.portionImageByWidth(screenCaptureImg, currLeft)

            portions.append(portionImg)

        return portions

    def portionImageByHeight(self, img, currTop=0, heightDivisor=0):

        if heightDivisor >= 0:
            divisor = heightDivisor

        else:
            divisor = PORTION_HEIGHT_DIVISOR

        portionHeight = int((img.shape[0]) / divisor)
        imgWidth = img.shape[1]

        imgTop = portionHeight
        imgHeight = currTop + portionHeight

        imgPortion = img[currTop:imgHeight, 0:imgWidth]

        return (imgPortion, imgHeight)

    def portionImageByWidth(self, img, currLeft=0, widthDivisor=0):

        if widthDivisor >= 0:
            divisor = widthDivisor

        else:
            divisor = PORTION_WIDTH_DIVISOR

        portionWidth = int((img.shape[1]) / divisor)
        imgHeight = img.shape[1]

        imgWidth = currLeft + portionWidth

        imgPortion = img[0:imgHeight, currLeft:imgWidth]

        return (imgPortion, imgWidth)

    def portionImageByArea(self, img, portionHeightCorrector=0, portionWidthCorrector=0):

        rowsImg = []
        areaImg = []

        rowDivision = PORTION_HEIGHT_DIVISOR + portionHeightCorrector
        colDivision = PORTION_WIDTH_DIVISOR - portionWidthCorrector

        for i in range(0, rowDivision):

            rowsImg = self.portionToRowsImg(img, rowDivision)

        if colDivision <= 0:
            colDivision = 2

        for rowImg in rowsImg:

            if colDivision > 1:
                columnsImg = self.portionToColumnsImg(rowImg, colDivision)

                areaImg.append(columnsImg)

        return areaImg

    def portionToColumnsImg(self, rowImg, portionWidthCorrector=0):

        currLeft = 0

        columnPortionsImg = []

        colDivision = portionWidthCorrector

        if colDivision <= 0:
            colDivision = 2


        for i in range(0, colDivision):

            areaImg, currLeft = self.portionImageByWidth(rowImg, currLeft, colDivision)

            columnPortionsImg.append(areaImg)

        return columnPortionsImg

    def portionToRowsImg(self, screencaptureImg, portionHeightCorrector=0):

        currTop = 0

        rowPortionsImg =  []

        rowDivision = portionHeightCorrector

        if rowDivision <=  0:
            rowDivision = 2


        for i in range(0, rowDivision):

            rowImg, currTop = self.portionImageByHeight(screencaptureImg, currTop, rowDivision)

            rowPortionsImg.append(rowImg)

        return rowPortionsImg

    def analyzePortion(self, imgPortion, areaImgMatricePosition=None):

        preprocess = self.preprocessDateImg(imgPortion)

        portionAnalysis = pytesseract.image_to_data(preprocess, output_type=Output.DICT)
        analyzedText = portionAnalysis['text']

        dateId = self.findIdOfDate(analyzedText)

        if dateId == None:
            return -1, None, None, None, None

        correctLeft = 0
        correctTop = 0

        # If we analyze a portion area (ie a portion grid)
        if areaImgMatricePosition != None:

            rowPosition = areaImgMatricePosition[0]
            columnPosition = areaImgMatricePosition[1]

            portionHeight = imgPortion.shape[0]
            portionWidth = imgPortion.shape[1]

            correctTop = portionHeight * (rowPosition)
            correctLeft = portionWidth * (columnPosition)

        left = portionAnalysis['left'][dateId] + correctLeft
        top = portionAnalysis['top'][dateId] + correctTop
        height = portionAnalysis['height'][dateId]
        width = portionAnalysis['width'][dateId]

        return dateId, left, top, height, width

    def getKChannel(self, img):
        # Conversion to CMYK (just the K channel):

        # Convert to float and divide by 255:
        imgFloat = img.astype(np.float) / 255.

        # Calculate channel K:
        kChannel = 1 - np.max(imgFloat, axis=2)

        # Convert back to uint 8:
        kChannel = (255 * kChannel).astype(np.uint8)

        return kChannel

    def preprocessDateImg(self, img):

        # Preprocess img to upgrade text analysis result for current img capture

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        invert = cv2.bitwise_not(gray)

        thresh = 90
        max = 255

        th, threshImg = cv2.threshold(invert, thresh, max, cv2.THRESH_BINARY_INV)

        return threshImg

    def preprocessTimeSlotImg(self, img):
        # Preprocess img to upgrade text analysis result for current img timeslot

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        invert = cv2.bitwise_not(gray)

        thresh = 165
        max = 255

        th, threshImg = cv2.threshold(invert, thresh, max, cv2.THRESH_BINARY_INV)

        return threshImg

    def prepareRoomAnalysis(self):
        # Generate all the required attributes for the functioning of getRoomAvailability Method

        if (type(self.calendarImg) == type(np.array([]))):

            if not ( self.calendarImg.size == 0 or self.dateCoordinate == None ):

                # Get timeslot for the timetable and their coordinates on the screencapture
                timeSlot = self.getTimeSlot()
                self.setTimeSlot(timeSlot)

                # Get roomsSlot for the timetable and their coordinates
                roomNameImg = self.cropRoomName(self.calendarImg)
                self.setRoomNameImg(roomNameImg)

                # Get the roomName Image Analysis
                roomNameAnalysis = pytesseract.image_to_data(roomNameImg, output_type=Output.DICT)
                self.setRoomNameAnalysis(roomNameAnalysis)

                # Get all the roomsName
                roomsName = self.generateRoomsName()
                self.setRoomsName(roomsName)

                # Get the roomSlotCoordinate data
                roomSlot = self.generateRoomSlot()
                self.setRoomSlot(roomSlot)

        else:
            print("Failed to prepare analysis, img is None")

    def getRoomAvailability(self, roomName):

        roomId = self.getRoomId(roomName)

        roomBoundingBox = self.roomSlot[roomId][1]

        roomImg = self.cropRoomSlotFromImg(self.calendarImg, roomBoundingBox)

        roomAvailability = []

        for i in range(0, len(self.timeSlot)):
            timeSlotName = self.timeSlot[i][0]

            status = self.getTimeSlotStatus(roomImg, timeSlotName)

            roomAvailability.append({'timeSlot':timeSlotName, 'status': status})

        return roomAvailability

    def generateRoomsName(self):

        roomName = []

        for i in range(0, len(self.roomNameAnalysis['text'])):

            text = self.roomNameAnalysis['text'][i]

            if self.isStringARoom(text):
                roomName.append(text)

        return roomName

    def visualizeRoomsAvailability(self):
        # To visualize the result of the execution

        availabilityImg = np.array([])

        for room in self.roomsName:

            availabilityImg = self.addAvailabilityTextToRoomSlotImg(room, availabilityImg)

        return availabilityImg

    def addAvailabilityTextToRoomSlotImg(self, roomName, roomImg=None):
        # Add availability text to provided roomName

        if roomImg.size == 0:
            availabilityTextImg = self.calendarImg.copy()

        else:
            availabilityTextImg = roomImg

        roomId = self.getRoomId(roomName)

        roomYCoordinate = self.getRoomYCoord(roomName, roomId)

        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        color = (255, 0, 0)
        thickness = 2
        pixelOffset = 10

        for i in range(0, len(self.timeSlot)):

            slot = self.timeSlot[i][0]
            availability = self.roomsAvailability[roomName][i]['status']

            left = self.timeSlot[i][1]['x']['left']

            org = (left, roomYCoordinate + pixelOffset)

            text = self.setTextToAdd(availability)

            availabilityTextImg = cv2.putText(availabilityTextImg, text, org, font,
                              fontScale, color,
                              thickness, cv2.LINE_AA)

        return availabilityTextImg

    def setTextToAdd(self, availabilityIndicator):
        # Returns the text to add respective to the indicator

        if availabilityIndicator == FULLY_BOOK_INDICATOR:
            return 'FULL'
        elif availabilityIndicator == FULLY_RESERVABLE_INDICATOR:
            return 'FREE'
        elif availabilityIndicator == FIRST_HALF_INDICATOR:
            return 'FFREE'
        elif availabilityIndicator == SECOND_HALF_INDICATOR:
            return 'SFREE'
        else:
            return 'UND'

    def getRoomYCoord(self, roomName, roomId=None):
        # Returns the room y coordinate

        if roomId == None:
            roomId = self.getRoomId(roomName)

        roomTop = self.roomSlot[roomId][1]['y']['top']

        return roomTop

    def getAllRoomsAvailability(self):

        roomsAvailability = {}

        for room in self.roomsName:

            availability = self.getRoomAvailability(room)

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

    def getRoomAvailabilityWithSlot(self, roomName, timeSlot, roomSlot):

        roomId = self.getRoomId(roomName)

        roomBoundingBox = self.roomSlot[roomId][1]

        roomImg = self.cropRoomSlotFromImg(self.calendarImg, roomBoundingBox)

        # copyRoomImg = roomImg.copy()

        # textRoomImg = self.addTimeSlotTextToImg(copyRoomImg, timeSlot)
        # self.showImg(textRoomImg)

        # slotWithText = self.addTimeSlotTextToImg(roomImg, timeSlot)

        roomAvailability = {}

        for i in range (0, len(self.timeSlot)):

            timeSlotName = self.timeSlot[i][0]

            status = self.getTimeSlotStatus(roomImg, timeSlotName, self.timeSlot)

            roomAvailability[timeSlotName] = status

        return roomAvailability

    def getTimeSlotStatus(self, timeSlotImg, timeSlotName):
        # Get the status from the requested TimeSlot Img

        id = self.getTimeSlotId(timeSlotName)
        timeSlotBoundingBox = self.timeSlot[id][1]

        timeSlotStatusImg = self.cropImgWithBoundingBox(timeSlotImg, timeSlotBoundingBox)

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

    def cropPortionsLeftAndRightTimeslot(self, timeSlotStatusImg):

        width = timeSlotStatusImg.shape[1]
        height = timeSlotStatusImg.shape[0]

        leftPortion = self.cropImgWithCoordinates(timeSlotStatusImg, 5, 5, 20, height-3)

        rightPortion = self.cropImgWithCoordinates(timeSlotStatusImg, width-20, 5, width, height-3)

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

    def getTimeSlotId(self, timeSlotName):
        # Get the id of the timeslot requested

        for i in range(0, len(self.timeSlot)):

            if self.timeSlot[i][0] == timeSlotName:
                return i

    def addTimeSlotTextToImg(self, img, timeSlot):

        pixelOffset = 10

        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        color = (255, 0, 0)
        thickness = 2

        for i in range(0, len(self.timeSlot)):

            text = timeSlot[i][0]

            orgX = timeSlot[i][1]['x']['left']
            orgY = timeSlot[i][1]['y']['top'] + pixelOffset

            org = (orgX, orgY)

            imgWithTimeSlot = cv2.putText(img, text, org, font,
                              fontScale, color,
                              thickness, cv2.LINE_AA)

        return imgWithTimeSlot

    def drawBoxAroundTimeSlot(self, img, timeSlot):

        for i in range(0, len(self.timeSlot)):

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

    def getRoomId(self, roomName):
        # get the room id from the roomSlot Array

        for i in range(0, len(self.roomSlot)) :

            if roomName == self.roomSlot[i][0]:

                return i

    def cropRoomName(self, img):

        pixelOffset = 10

        imgHeight = img.shape[0]
        left = self.dateCoordinate[0]
        top = self.dateCoordinate[1]
        width = self.dateCoordinate[2]
        height = self.dateCoordinate[3]

        cropImg = img[0:imgHeight, 0:left + width]

        return cropImg

    def generateRoomSlot(self):

        # Get the coordinates of all the rooms in the present screenCapture
        roomsSlot = []

        for i in range(0, len(self.roomNameAnalysis['text'])):

            if self.roomNameAnalysis['conf'][i] >= 30:

                text = self.roomNameAnalysis['text'][i]

                if self.isStringARoom(text):

                    boundingBox = self.getTextBoundingBox(self.roomNameAnalysis, i)
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

    def getTimeSlot(self):

        # Get the timeSlot from the current screencapture with their exact coordinates
        imgWidth = self.calendarImg.shape[1]

        pixelOffset = 15

        boxLeft = self.dateCoordinate[0]
        boxTop = self.dateCoordinate[1]
        boxHeight = self.dateCoordinate[2]

        timeSlot = []

        availableTimeImg = self.calendarImg[0:boxHeight+boxTop+pixelOffset, 0:imgWidth]

        processImg = self.preprocessTimeSlotImg(availableTimeImg)

        timeAnalyzed = pytesseract.image_to_data(processImg, output_type=Output.DICT)

        for i in range(0, len(timeAnalyzed['text'])):

            confidenceLevel = timeAnalyzed['conf'][i]
            text = timeAnalyzed['text'][i]

            if confidenceLevel >= 30 and self.isStringATimeSlot(text):

                time = text

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

    def cropCalendarImage(self, screencaptureImg):
        # Crop the calendar from the screencapture

        boxLeft, boxTop, boxHeight, boxWidth = self.findCropDateCoordinateByArea(screencaptureImg)

        self.dateCoordinate = (boxLeft, boxTop, boxHeight, boxWidth)

        imgWidth = screencaptureImg.shape[1]
        imgHeight = screencaptureImg.shape[0]

        pixelOffset = 15

        cropImg = screencaptureImg[boxTop - pixelOffset:imgHeight , boxLeft-pixelOffset:imgWidth]

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

    # SETTERS

    def setCalendarImg(self, calendarImg):
        self.calendarImg = calendarImg

    def setRoomNameImg(self, roomNameImg):
        self.roomNameImg = roomNameImg

    def setCalendarAnalysis(self, analysisDict):
        self.calendarAnalysis = analysisDict

    def setRoomNameAnalysis(self, roomNameAnalysis):
        self.roomNameAnalysis = roomNameAnalysis

    def setRoomsName(self, rooms):
        self.roomsName = rooms

    def setTimeSlot(self, timeSlot):
        self.timeSlot = timeSlot

    def setRoomSlot(self, roomSlot):
        self.roomSlot = roomSlot

    def setRoomsAvailability(self, roomsAvailability):
        self.roomsAvailability = roomsAvailability

    # GETTERS

    def getCalendarImg(self):
        return self.calendarImg

    def getRoomNameImg(self):
        return self.roomNameImg

    def getCalendarAnalysis(self):
        return self.calendarAnalysis

    def getRoomNameAnalysis(self):
        return self.roomNameAnalysis

    def getRoomsName(self):
        return self.roomsName

    def getRoomSlot(self):
        return self.roomSlot