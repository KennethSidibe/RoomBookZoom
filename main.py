
from BookBot import *
from LoginBot import *
from TextBot import *
import cv2
import time

if __name__ == '__main__':

    def analyzeNImages(numberOfPages, textBot):

        for i in range(1, numberOfPages):

            imageFilePath = 'screencapture/SCREEN_' + str(i) + '_IMG.PNG'

            textBot.analyze(imageFilePath)


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
    screenFilePath = 'screencapture/SCREEN_1_IMG.png'

    bookBot = BookBot()

    textBot = TextBot()

    start = time.time()
    # bookBot.login()

    availability = textBot.analyze(filepathEmpty)

    print(availability)

    elapsedTime = time.time() - start

    print('elapsed time : ', elapsedTime)







