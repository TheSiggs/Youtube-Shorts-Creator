import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class Instagram:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def upload(self, file):
        try:
            self.driver.switch_to.new_window('tab')
            self.driver.get('https://www.instagram.com/redditssaid/')
            sleep(3)
            self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Create').click()
            sleep(2)
            inputs = self.driver.find_elements(By.XPATH, '//input[@type="file"]')
            chooseFile = inputs[-1]
            chooseFile.send_keys(file)
            sleep(1)
            buttons = self.driver.find_elements(By.XPATH, '//button')
            next((x for x in buttons if x.text == 'Next'), None).click()
            sleep(1)
            buttons = self.driver.find_elements(By.XPATH, '//button')
            next((x for x in buttons if x.text == 'Next'), None).click()
            sleep(1)
            buttons = self.driver.find_elements(By.XPATH, '//button')
            next((x for x in buttons if x.text == 'Share'), None).click()
            sleep(20)
            try:
                try_again = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Try Again")]')))
                try_again.click()
                sleep(5)
            except:
                print('It worked')
        except Exception as e:
            self.logger.log(f'Failed uploading {file} to Instagram')
            self.logger.log(e)