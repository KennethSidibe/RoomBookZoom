from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class LoginBot():

    def login(self):

        browser = webdriver.Chrome('/Users/kanekisidibe/Developer/Python/RoomBookZoom/driver/chromedriver')
        browser.get(('https://accounts.google.com/ServiceLogin?'
                     'service=mail&continue=https://mail.google'
                     '.com/mail/#identifier'))
        buttonXPath = '//*[@id="identifierNext"]/div/button'

        usernameField = browser.find_element(By.ID, "identifierId")
        usernameField.send_keys(self.username)
        nextButton = browser.find_element(By.XPATH, buttonXPath)
        nextButton.click()

        input(":")