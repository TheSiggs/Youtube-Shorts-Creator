import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class TikTok:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def upload(self, file):
        try:
            self.driver.switch_to.new_window('tab')
            self.driver.get('https://www.tiktok.com/upload/')
            sleep(5)
            iframe = self.driver.find_element(By.XPATH, '//iframe')
            self.driver.switch_to.frame(iframe)
            chooseFile = self.driver.find_element(By.XPATH, '//input[@type="file"]')
            chooseFile.send_keys(file)
            post_button = WebDriverWait(self.driver, 120).until(
                EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "btn-post")]/button')))
            sleep(5)
            post_button.click()
            sleep(30)
        except Exception as e:
            self.logger.log(f'Failed uploading {file} to TikTok')
            self.logger.log(e)