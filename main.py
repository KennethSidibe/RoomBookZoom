
from BookBot import *
from LoginBot import *
from TextBot import *
import cv2
import time

if __name__ == '__main__':

    mobileFilepath = 'screencapture/mobileBookingScreenshot.jpg'
    smallCopyFilePath = 'screencapture/smallBookingSchedule.png'
    filepath = 'screencapture/booking_hard_test.png'
    filepath2 = 'screencapture/booking_full_2.png'
    filepathEmpty = 'screencapture/booking_half_empty.png'
    filepath3 = 'screencapture/booking_half_empty.png'
    filepath4 = 'screencapture/booking_schedule_full.png'
    filepath5 = 'screencapture/testBooking.png'
    filepath6 = 'screencapture/testBooking2.png'
    filepath7 = 'screencapture/booking_FTX525-MRT412.png'
    filepath8 = 'screencapture/booking_MRT412-RGN1020.png'
    testProcessFilePath = 'screencapture/testProcess.png'
    screenFilePath = 'SCREEN_IMG.png'

    bot = LoginBot()

    bookBot = BookBot()

    textBot = TextBot()

    # bookBot.testRetrieveTable()

    availability = textBot.analyze(filepathEmpty)

    twoHoursConsecutive = bookBot.find2HoursSlot(availability['CRX-C520'])
    hourSlot = bookBot.find1HourSlot(availability['CRX-C520'])

    print(twoHoursConsecutive)
    print(hourSlot)

    # start = time.time()

    # for i in range(1, 8):
    #
    #     fileName = 'SCREEN_' + str(i) + '_IMG.png'
    #
    #     screenFilePath = 'screencapture/' + fileName
    #
    #     availability = textBot.analyze(screenFilePath)
    #


    # elapsedTime = time.time() - start

    # print(availability)

    # print('elapsed time : ', elapsedTime)