import pyotp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from credentials import *
import undetected_chromedriver.v2 as uc
from time import sleep
from pyotp import TOTP
from constant import *


class BookBot():

    rooms = ['CRX-C520', 'CRX-C521', 'CRX-C522', 'CRX-C523', 'CRX-C524', 'CRX-C525',
             'CRX-C526', 'CRX-C527', 'CRX-C528','CRX-C529', 'CRX-C541', 'CRX-C542',
             'CRX-C543', 'CRX-C544', 'CRX-C545',

             'FTX-514', 'FTX-515', 'FTX-525A', 'FTX-525B', 'FTX-525C', 'FTX-525D',
             'FTX-525F', 'FTX-525G', 'FTX-525H', 'FTX-525J',

             'MRT-404', 'MRT-405', 'MRT-406', 'MRT-407', 'MRT-408', 'MRT-409',
             'MRT-410', 'MRT-411', 'MRT-412', 'MRT-415', 'MRT-417', 'MRT-418',

             'RGN-1020J', 'RGN-1020K', 'RGN-1020L', 'RGN-1020M', 'RGN-1020N', 'RGN-1020P'
             ]


    def enteringUsername(self, driver):
        usernameFieldXPath = '//*[@id="i0116"]'
        usernameNextButtonXPath = '//*[@id="idSIButton9"]'

        usernameField = driver.find_element(By.XPATH, usernameFieldXPath)
        usernameNextButton = driver.find_element(By.XPATH, usernameNextButtonXPath)

        usernameField.send_keys(uoUsername)
        usernameNextButton.click()

        return driver

    def enteringPwd(self, driver):

        pwdFieldXPath = '//*[@id="i0118"]'
        pwdSignInButtonXPath = '//*[@id="idSIButton9"]'

        pwdField = driver.find_element(By.XPATH, pwdFieldXPath)
        pwdSignInButton = driver.find_element(By.XPATH, pwdSignInButtonXPath)

        pwdField.send_keys(uoPwd)
        pwdSignInButton.click()

        return driver

    def pick2FAMethod(self, driver):

        pick2FAMethodButtonXPath = '//*[@id="signInAnotherWay"]'

        pick2FAMethodButton = driver.find_element(By.XPATH, pick2FAMethodButtonXPath)

        pick2FAMethodButton.click()

        return driver

    def select2FAMethod(self, driver):

        selectCode2FAButtonXPath = '//*[@id="idDiv_SAOTCS_Proofs"]/div[2]/div'

        selectCode2FAButton = driver.find_element(By.XPATH, selectCode2FAButtonXPath)

        selectCode2FAButton.click()

        return driver

    def enterOTPCode(self, driver):

        otpFieldXPath = '//*[@id="idTxtBx_SAOTCC_OTC"]'
        verifyButtonXPath = '//*[@id="idSubmit_SAOTCC_Continue"]'

        otpField = driver.find_element(By.XPATH, otpFieldXPath)
        verifyButton = driver.find_element(By.XPATH, verifyButtonXPath)

        otpField.send_keys(self.getOTP())

        verifyButton.click()

        return driver

    def confirmStayedLogIn(self, driver):

        reduceLoginBoxXPath = '//*[@id="KmsiCheckboxField"]'
        noButtonXPath = '//*[@id="idBtn_Back"]'
        yesButtonXPath = '//*[@id="idSIButton9"]'

        reduceLoginBox = driver.find_element(By.XPATH, reduceLoginBoxXPath)
        noButton = driver.find_element(By.XPATH, noButtonXPath)
        yesButton = driver.find_element(By.XPATH, yesButtonXPath)

        reduceLoginBox.click()
        yesButton.click()

        return driver

    def accessBookSchedule(self, driver):

        bookRoomButtonXPath = '//*[@id="navReservation"]/a'

        bookRoomButton = driver.find_element(By.XPATH, bookRoomButtonXPath)

        bookRoomButton.click()

        return driver

    def takeScreenshotOfNDays(self, numberOfPages, driver):

        for i in range(1, numberOfPages+1):

            fileName = 'SCREEN_' + str(i) + '_IMG.png'

            imgFilePath = 'screencapture/' + fileName

            driver.save_screenshot(imgFilePath)

            driver = self.goToNextPage(driver)

    def getOTP(self):

        totp = pyotp.parse_uri(uoAuthSecretURI)

        return totp.now()

    def waitForElementToAppear(self, elementXPath):

        wait.until(EC.presence_of_element_located((By.XPATH, elementXPath)))

    def goToNextPage(self, driver):

        # Go to next page
        nextPageButtonXPath = '//*[@id="page-schedule"]/div[2]/div[2]/a[3]'
        nextPageButton = driver.find_element(By.XPATH, nextPageButtonXPath)

        nextPageButton.click()

        sleep(3)

        return driver

    def getElementsText(self, driver, xPath):

        texts = []

        elements = driver.find_elements(By.XPATH, xPath)

        for element in elements:

            texts.append(element.text)

        if len(texts) == 1:
            return texts[0], driver

        return texts, driver

    def testRetrieveTable(self):

        # Options
        options = uc.ChromeOptions()
        options.user_data_dir = "c:\\temp\\profile"
        options.add_argument('--user-data-dir=c:\\temp\\profile2')
        options.add_argument('--incognito')
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"

        # creating the driver
        driver = uc.Chrome(options=options, desired_capabilities=capa)
        wait = WebDriverWait(driver, 20)

        tableDemoUrl = 'file:///Users/kanekisidibe/Developer/Python/RoomBookZoom/HtmlBookSchedulePage.html'

        # Opening the url
        driver.get(tableDemoUrl)

        reservationTableXPath = '//table[@class="reservations"]'
        timeSlotXPath = '//*[@class="reslabel"]'
        roomsXPath = '//td[@class="resourcename"]'
        reservationDateXPath = '//*[@class="resdate"]'

        wait.until(EC.presence_of_element_located((By.XPATH, reservationTableXPath)))

        # driver.execute_script("window.stop();")

        reservationDate, driver = self.getElementsText(driver, reservationDateXPath)
        timeSlot, driver = self.getElementsText(driver, timeSlotXPath)
        rooms, driver = self.getElementsText(driver, roomsXPath)

        print(reservationDate)
        print(timeSlot)
        print(rooms)

        driver.quit()

    def find2HoursSlot(self, roomAvailability):

        twoHoursSlot = []

        for i  in range(0, len(roomAvailability)-1):

            slot = roomAvailability[i]['timeSlot']
            slotNext = roomAvailability[i+1]['timeSlot']
            status = roomAvailability[i]['status']
            statusNext = roomAvailability[i+1]['status']

            if status == FULLY_RESERVABLE_INDICATOR and statusNext == FULLY_RESERVABLE_INDICATOR:

                firstSlot = {'timeSlot':slot, 'id':i}
                secondSlot = {'timeSlot':slotNext, 'id':i+1}

                twoHoursSlot.append( { 'firstSlot':firstSlot, 'secondSlot':secondSlot } )

        return  twoHoursSlot

    def find1HourSlot(self, roomAvailability):

        hourSlot = []

        for i in range(0, len(roomAvailability)):

            slot = roomAvailability[i]['timeSlot']
            status = roomAvailability[i]['status']

            if status == FULLY_RESERVABLE_INDICATOR:
                slot = {'timeSlot': slot, 'id': i}

                hourSlot.append( slot )

        return hourSlot

    def login(self):

        # Options
        options = uc.ChromeOptions()

        options.user_data_dir = "c:\\temp\\profile"

        options.add_argument('--user-data-dir=c:\\temp\\profile2')
        options.add_argument('--incognito')

        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')

        # creating the driver
        driver = uc.Chrome(options=options)

        # Opening the url
        driver.get((uoBookRoomUrl))

    #   entering username
        driver = self.enteringUsername(driver)

        sleep(3)

        # entering pwd
        driver = self.enteringPwd(driver)

        sleep(4)

        # Pick 2FA methods
        driver = self.pick2FAMethod(driver)

        sleep(3)

        # Select 2FA Methods

        self.select2FAMethod(driver)

        sleep(3)

        # Entering OTP code
        driver = self.enterOTPCode(driver)

        sleep(3)

        # confirming stayed login
        driver = self.confirmStayedLogIn(driver)


        sleep(5)

        # access the booking schedule page
        driver = self.accessBookSchedule(driver)

        # Take screenshot of the page
        driver = self.takeScreenshotOfNDays(8, driver)

        # input is just to wait and see results
        driver.quit()

