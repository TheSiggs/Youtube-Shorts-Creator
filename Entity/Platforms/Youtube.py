import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class Youtube:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def upload(self, file):
        try:
            self.driver.switch_to.new_window('tab')
            self.driver.get('https://studio.youtube.com/channel/UCkrrIuQTIUcvVobIl_0ofTg')
            sleep(10)
            self.driver.find_element(By.XPATH, '//*[@id="create-icon"]').click()
            sleep(0.5)
            self.driver.find_element(By.XPATH, '//*[@id="text-item-0"]').click()
            sleep(1)
            chooseFileYT = self.driver.find_element(By.XPATH, '//*[@name="Filedata"]')
            chooseFileYT.send_keys(file)
            sleep(10)
            self.driver.find_element(By.XPATH, '//*[@id="next-button"]').click()
            sleep(1)
            self.driver.find_element(By.XPATH, '//*[@id="next-button"]').click()
            sleep(1)
            self.driver.find_element(By.XPATH, '//*[@id="next-button"]').click()
            sleep(1)
            self.driver.find_element(By.XPATH, '//*[@name="PUBLIC"]').click()
            sleep(0.1)
            self.driver.find_element(By.XPATH, '//*[@id="done-button"]').click()
            sleep(0.5)
        except Exception as e:
            self.logger.log(f'Failed uploading {file} to Youtube')
            self.logger.log(e)