from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from credentials import *
import undetected_chromedriver as uc
from time import sleep


class LoginBot():

    def login(self):

        # Options to maximisze windows
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")

        # Other options
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])


        browser = webdriver.Chrome('/Users/kanekisidibe/Developer/Python/RoomBookZoom/driver/chromedriver',
                                   chrome_options=options)
        browser.get(('https://accounts.google.com/ServiceLogin?'
                     'service=mail&continue=https://mail.google'
                     '.com/mail/#identifier'))


        buttonXPath = '//*[@id="identifierNext"]/div/button'

        usernameField = browser.find_element(By.ID, "identifierId")
        time.sleep(3)
        usernameField.send_keys(username)
        time.sleep(3)

        nextButton = browser.find_element(By.XPATH, buttonXPath)
        time.sleep(3)
        nextButton.click()

        input(":")