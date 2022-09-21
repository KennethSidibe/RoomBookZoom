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



class LoginBot():

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
        driver.get(('https://accounts.google.com/ServiceLogin?'
                     'service=mail&continue=https://mail.google'
                     '.com/mail/#identifier'))

        sleep(3)

        # entering username and clicking nexgt
        usernameNextButtonXPPath = '//*[@id="identifierNext"]/div/button'
        pwdNextButtonXPath = '//*[@id="passwordNext"]/div/button'
        pwdFieldXPath = '//*[@id="password"]/div[1]/div/div[1]/input'


        usernameField = driver.find_element(By.ID, "identifierId")
        usernameField.send_keys(username)

        nextButton = driver.find_element(By.XPATH, usernameNextButtonXPPath)
        nextButton.click()

        sleep(3)

        # entering password and clicking
        passwordField = driver.find_element(By.XPATH, pwdFieldXPath)
        pwdNextButton = driver.find_element(By.XPATH, pwdNextButtonXPath)

        passwordField.send_keys(pwd)
        pwdNextButton.click()

        sleep(3)

        # Choosing 2FA methods
        another2FAMethodButtonXPath = '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div/button'

        another2FAButton = driver.find_element(By.XPATH, another2FAMethodButtonXPath)
        another2FAButton.click()

        sleep(3)

        # Choose Google auth code meth
        authMethodButtonXPath = '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/ul/li[3]'
        authGoogle2FAButton = driver.find_element(By.XPATH, authMethodButtonXPath)

        authGoogle2FAButton.click()

        sleep(3)

        # Enter auth code into form
        otpFieldXPath = '//*[@id="totpPin"]'
        otpNextButtonXPath = '//*[@id="totpNext"]/div/button'

        otpField = driver.find_element(By.XPATH, otpFieldXPath)
        otpNextButton = driver.find_element(By.XPATH, otpNextButtonXPath)

        # generating one time code
        otp = self.getOTP()
        otpField.send_keys(otp)

        otpNextButton.click()

        sleep(3)

        input(":")

    def getOTP(self):

        totp = pyotp.parse_uri(authSecretURI)

        return totp.now()