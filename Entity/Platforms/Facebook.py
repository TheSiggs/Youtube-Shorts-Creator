import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class Facebook:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def upload(self, file):
        try:
            self.driver.switch_to.new_window('tab')
            self.driver.get('https://www.facebook.com/reels/create')
            sleep(10)
            self.driver.find_element(By.XPATH, '//div[contains(@aria-label, "Reels creation form")]').click()
            sleep(1)
            chooseFile = self.driver.find_element(By.XPATH, '//div[contains(@aria-label, "Reels")]//input[@type="file"]')
            chooseFile.send_keys(file)
            sleep(5)
            self.driver.find_element(By.XPATH, '//div[contains(@aria-label, "Next")]').click()
            sleep(5)
            self.driver.find_elements(By.XPATH, '//div[contains(@aria-label, "Next")]')[1].click()
            sleep(1)
            post_button = WebDriverWait(self.driver, 120).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//div[contains(@aria-label, "Publish") and contains(@tabindex, "0")]')))
            post_button.click()
            sleep(50)
        except Exception as e:
            self.logger.log(f'Failed uploading {file} to Facebook')
            self.logger.log(e)