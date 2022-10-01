import pyotp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from credentials import *
import undetected_chromedriver.v2 as uc
from time import sleep
from pyotp import TOTP
from constant import *


class BookBot():

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
        usernameFieldXPath = '//*[@id="i0116"]'
        usernameNextButtonXPath = '//*[@id="idSIButton9"]'

        usernameField = driver.find_element(By.XPATH, usernameFieldXPath)
        usernameNextButton = driver.find_element(By.XPATH, usernameNextButtonXPath)

        usernameField.send_keys(uoUsername)
        usernameNextButton.click()

        sleep(3)

        # entering pwd

        pwdFieldXPath = '//*[@id="i0118"]'
        pwdSignInButtonXPath = '//*[@id="idSIButton9"]'

        pwdField = driver.find_element(By.XPATH, pwdFieldXPath)
        pwdSignInButton = driver.find_element(By.XPATH, pwdSignInButtonXPath)

        pwdField.send_keys(uoPwd)
        pwdSignInButton.click()

        sleep(4)

        # Pick 2FA methods

        pick2FAMethodButtonXPath = '//*[@id="signInAnotherWay"]'

        pick2FAMethodButton = driver.find_element(By.XPATH, pick2FAMethodButtonXPath)

        pick2FAMethodButton.click()

        sleep(3)

        # Select 2FA Methods

        selectCode2FAButtonXPath = '//*[@id="idDiv_SAOTCS_Proofs"]/div[2]/div'

        selectCode2FAButton = driver.find_element(By.XPATH, selectCode2FAButtonXPath)

        selectCode2FAButton.click()

        sleep(3)

        # Entering OTP code

        otpFieldXPath = '//*[@id="idTxtBx_SAOTCC_OTC"]'
        verifyButtonXPath = '//*[@id="idSubmit_SAOTCC_Continue"]'

        otpField = driver.find_element(By.XPATH, otpFieldXPath)
        verifyButton = driver.find_element(By.XPATH, verifyButtonXPath)

        otpField.send_keys(self.getOTP())

        verifyButton.click()

        sleep(3)

        # confirming stayed login

        reduceLoginBoxXPath = '//*[@id="KmsiCheckboxField"]'
        noButtonXPath = '//*[@id="idBtn_Back"]'
        yesButtonXPath = '//*[@id="idSIButton9"]'

        reduceLoginBox = driver.find_element(By.XPATH, reduceLoginBoxXPath)
        noButton = driver.find_element(By.XPATH, noButtonXPath)
        yesButton = driver.find_element(By.XPATH, yesButtonXPath)

        reduceLoginBox.click()
        yesButton.click()

        sleep(5)

        # access the booking schedule page
        bookRoomButtonXPath = '//*[@id="navReservation"]/a'

        bookRoomButton = driver.find_element(By.XPATH, bookRoomButtonXPath)

        bookRoomButton.click()

        # Take screenshot of the page
        for i in range(1, 8):

            fileName = 'SCREEN_' + str(i) + '_IMG.png'

            imgFilePath = 'screencapture/' + fileName

            driver.save_screenshot(imgFilePath)

            driver = self.goToNextPage(driver)

        # input is just to wait and see results
        driver.quit()

    def getOTP(self):

        totp = pyotp.parse_uri(uoAuthSecretURI)

        return totp.now()

    def goToNextPage(self, driver):

        # Go to next page
        nextPageButtonXPath = '//*[@id="page-schedule"]/div[2]/div[2]/a[3]'
        nextPageButton = driver.find_element(By.XPATH, nextPageButtonXPath)

        nextPageButton.click()

        sleep(3)

        return driver

    def testRetrieveTable(self):

        print('hi')