import glob
import os
import subprocess
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


def upload_youtube(file):
    driver.switch_to.new_window('tab')
    driver.get('https://studio.youtube.com/channel/UCkrrIuQTIUcvVobIl_0ofTg')
    sleep(10)
    driver.find_element(By.XPATH, '//*[@id="create-icon"]').click()
    sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="text-item-0"]').click()
    sleep(1)
    chooseFileYT = driver.find_element(By.XPATH, '//*[@name="Filedata"]')
    chooseFileYT.send_keys(file)
    sleep(10)
    driver.find_element(By.XPATH, '//*[@id="next-button"]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//*[@id="next-button"]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//*[@id="next-button"]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//*[@name="PUBLIC"]').click()
    sleep(0.1)
    driver.find_element(By.XPATH, '//*[@id="done-button"]').click()
    sleep(0.5)


def upload_ig(file):
    driver.switch_to.new_window('tab')
    driver.get('https://www.instagram.com/redditssaid/')
    sleep(3)
    driver.find_element(By.PARTIAL_LINK_TEXT, 'Create').click()
    sleep(2)
    inputs = driver.find_elements(By.XPATH, '//input[@type="file"]')
    chooseFile = inputs[-1]
    chooseFile.send_keys(file)
    sleep(1)
    buttons = driver.find_elements(By.XPATH, '//button')
    next((x for x in buttons if x.text == 'Next'), None).click()
    sleep(1)
    buttons = driver.find_elements(By.XPATH, '//button')
    next((x for x in buttons if x.text == 'Next'), None).click()
    sleep(1)
    buttons = driver.find_elements(By.XPATH, '//button')
    next((x for x in buttons if x.text == 'Share'), None).click()


def upload_tiktok(file):
    driver.switch_to.new_window('tab')
    driver.get('https://www.tiktok.com/upload/')
    sleep(5)
    iframe = driver.find_element(By.XPATH, '//iframe')
    driver.switch_to.frame(iframe)
    chooseFile = driver.find_element(By.XPATH, '//input[@type="file"]')
    chooseFile.send_keys(file)
    post_button = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "btn-post")]/button')))
    sleep(5)
    post_button.click()
    sleep(30)


def upload_facebook(file):
    driver.switch_to.new_window('tab')
    driver.get('https://www.facebook.com/reels/create')
    sleep(10)
    driver.find_element(By.XPATH, '//div[contains(@aria-label, "Reels creation form")]').click()
    sleep(1)
    chooseFile = driver.find_element(By.XPATH, '//div[contains(@aria-label, "Reels")]//input[@type="file"]')
    chooseFile.send_keys(file)
    sleep(5)
    driver.find_element(By.XPATH, '//div[contains(@aria-label, "Next")]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//div[contains(@aria-label, "Next") and contains(@tabindex, "0")]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//div[contains(@aria-label, "Publish") and contains(@tabindex, "0")]').click()
    sleep(50)


# e.g. Chrome path in Mac =/Users/x/Library/xx/Chrome/Default/
user_data_dir = 'C:\\Users\\samsi\\AppData\\Local\\Google\\Chrome\\User Data\\Default'

# Remove files
for file in glob.glob(os.getcwd()+'\\videos\\*'):
    os.remove(file)

# Run PHP Script
out = subprocess.call("docker-compose run --rm php81-service php index.php", shell=True)
# out = 1
if out == 0:
    try:
        options = uc.ChromeOptions()
        options.add_argument("--ignore-certificate-error")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--user-data-dir=" + user_data_dir)
        options.add_argument("--headless")
        driver = uc.Chrome(options=options)

        # Get most recent file in videos
        list_of_files = glob.glob(os.getcwd()+'\\videos\\*')
        latest_file = max(list_of_files, key=os.path.getctime)

        upload_youtube(latest_file)
        upload_ig(latest_file)
        upload_tiktok(latest_file)
        upload_facebook(latest_file)
    except Exception as e:
        print(e)
else:
    print("PHP script failed :(")
