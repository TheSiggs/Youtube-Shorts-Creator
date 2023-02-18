import subprocess
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from time import sleep


def upload_youtube():
    driver.switch_to.new_window('tab')
    driver.get('https://studio.youtube.com/channel/UCkrrIuQTIUcvVobIl_0ofTg')
    sleep(10)
    driver.find_element(By.XPATH, '//*[@id="create-icon"]').click()
    sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="text-item-0"]').click()
    sleep(1)
    chooseFileYT = driver.find_element(By.XPATH, '//*[@name="Filedata"]')
    chooseFileYT.send_keys(
        "S:\\Projects\\SeleniumTest\\We shortened Television to 'TV', but Telephone to 'phone'. #shorts.mp4")
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


def upload_ig():
    driver.switch_to.new_window('tab')
    driver.get('https://www.instagram.com/redditssaid/')
    sleep(3)
    driver.find_element(By.PARTIAL_LINK_TEXT, 'Create').click()
    sleep(2)
    inputs = driver.find_elements(By.XPATH, '//input[@type="file"]')
    chooseFile = inputs[-1]
    chooseFile.send_keys(
        "S:\\Projects\\SeleniumTest\\We shortened Television to 'TV', but Telephone to 'phone'. #shorts.mp4")
    sleep(1)
    buttons = driver.find_elements(By.XPATH, '//button')
    next((x for x in buttons if x.text == 'Next'), None).click()
    sleep(1)
    buttons = driver.find_elements(By.XPATH, '//button')
    next((x for x in buttons if x.text == 'Next'), None).click()
    sleep(1)
    buttons = driver.find_elements(By.XPATH, '//button')
    next((x for x in buttons if x.text == 'Share'), None).click()


def upload_tiktok():
    driver.switch_to.new_window('tab')
    driver.get('https://www.tiktok.com/upload/')
    sleep(5)
    iframe = driver.find_element(By.XPATH, '//iframe')
    driver.switch_to.frame(iframe)
    chooseFile = driver.find_element(By.XPATH, '//input[@type="file"]')
    chooseFile.send_keys("S:\\Projects\\SeleniumTest\\We shortened Television to 'TV', but Telephone to 'phone'. #shorts.mp4")
    sleep(20)
    driver.find_element(By.XPATH, "//button/div/div[text()='Post']").click()



# Run PHP Script
out = subprocess.call("docker-compose run php81-service php index.php", shell=True)
if out == 0:
    options = uc.ChromeOptions()
    options.add_argument("--ignore-certificate-error")
    options.add_argument("--ignore-ssl-errors")
    # e.g. Chrome path in Mac =/Users/x/Library/xx/Chrome/Default/
    options.add_argument("--user-data-dir=C:\\Users\\samsi\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
    driver = uc.Chrome(options=options)
    upload_youtube()
    upload_ig()
    upload_tiktok()
else:
    print("PHP script failed :(")
