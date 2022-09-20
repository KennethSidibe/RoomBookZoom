from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from credentials import *
from selenium_stealth import stealth
import time



class LoginBot():

    def login(self):

        # Options to maximisze windows
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")

        # Other options
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        browser = webdriver.Chrome('/Users/kanekisidibe/Developer/Python/RoomBookZoom/driver/chromedriver')
        browser.get(('https://accounts.google.com/ServiceLogin?'
                     'service=mail&continue=https://mail.google'
                     '.com/mail/#identifier'))

        # Selenium stealth statement
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        buttonXPath = '//*[@id="identifierNext"]/div/button'

        usernameField = browser.find_element(By.ID, "identifierId")
        usernameField.send_keys(username)
        nextButton = browser.find_element(By.XPATH, buttonXPath)
        nextButton.click()

        input(":")