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

        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')

        # creating the driver
        driver = uc.Chrome(options=options)

        # Opening the url
        driver.get(('https://accounts.google.com/ServiceLogin?'
                     'service=mail&continue=https://mail.google'
                     '.com/mail/#identifier'))

        buttonXPath = '//*[@id="identifierNext"]/div/button'

        usernameField = driver.find_element(By.ID, "identifierId")
        usernameField.send_keys(username)

        nextButton = driver.find_element(By.XPATH, buttonXPath)

        nextButton.click()



        input(":")

    def getOTP(self):

        totp = pyotp.parse_uri(authSecretURI)

        while 1:

            sleep(1)
            print(totp.now())
