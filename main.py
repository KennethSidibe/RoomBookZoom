
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
    filepath3 = 'screencapture/booking_half_empty.png'
    filepath4 = 'screencapture/booking_schedule_full.png'
    filepath5 = 'screencapture/testBooking.png'
    filepath6 = 'screencapture/testBooking2.png'
    filepath7 = 'screencapture/booking_FTX525-MRT412.png'
    filepath8 = 'screencapture/booking_MRT412-RGN1020.png'
    testProcessFilePath = 'screencapture/testProcess.png'

    bot = LoginBot()

    bookBot = BookBot()

    textBot = TextBot()

    # bookBot.login()

    screenFilePath = 'SCREEN_IMG.png'

    # start = time.time()
    availability = textBot.analyze(mobileFilepath)
    # elapsedTime = time.time() - start

    # print(availability)

    # print('elapsed time : ', elapsedTime)