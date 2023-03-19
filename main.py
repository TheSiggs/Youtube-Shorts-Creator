import glob
import os
import subprocess
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from dotenv import load_dotenv
import sys

load_dotenv()

def log(error):
    if os.getenv('ENV') == 'dev':
        print(error)
    else:
        headers = {"Authorization": "Bearer xoxb-2102419125553-4890952961859-MnsB3ow5KnQx8iBdmi1oDKvz"}
        data = {
            "channel": "C04S0BQCSS2",
            "text": error
        }
        requests.post('https://slack.com/api/chat.postMessage', headers=headers, data=data)


def printQuota():
    req = requests.get('https://api.json2video.com/v2/movies', headers={
        "x-api-key": "GUqCH3WziX8Z0qx4xxjIFRaxoCkC8Kl7EyVYOTGi"
    })
    resp = req.json()
    quota = resp['remaining_quota']
    log('Quota Remaining - Movies: {}, Drafts: {}'.format(quota['movies'], quota['drafts']))


def get_latest_youtube_vid():
    url = 'https://www.googleapis.com/youtube/v3/search?key=AIzaSyBAmzATERyHVgNkkEc4CDUqCD8ppn0fXLE&channelId=UCkrrIuQTIUcvVobIl_0ofTg&part=snippet,id&order=date&maxResults=1'
    links = requests.get(url)
    links_dict = links.json()
    youtube_links = ['https://www.youtube.com/shorts/{}'.format(item['id']['videoId']) for item in links_dict['items']]
    return youtube_links[0]


def post_to_twitter():
    driver.switch_to.new_window('tab')
    driver.get('https://studio.youtube.com/channel/UCkrrIuQTIUcvVobIl_0ofTg')
    sleep(10)
    latest_video = get_latest_youtube_vid()
    tweet = 'New {} Video! {}'.format(sys.argv[1], latest_video)
    driver.find_element(By.XPATH, '//div[@id="placeholder-cavgb"]').send_keys(tweet)
    sleep(2)
    driver.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]').click()



def upload_youtube(file):
    try:
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
    except Exception as e:
        log(e)


def upload_ig(file):
    try:
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
        sleep(20)
        try:
            try_again = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Try Again")]')))
            try_again.click()
            sleep(5)
        except:
            print('It worked')
    except Exception as e:
        log(e)


def upload_tiktok(file):
    try:
        driver.switch_to.new_window('tab')
        driver.get('https://www.tiktok.com/upload/')
        sleep(5)
        iframe = driver.find_element(By.XPATH, '//iframe')
        driver.switch_to.frame(iframe)
        chooseFile = driver.find_element(By.XPATH, '//input[@type="file"]')
        chooseFile.send_keys(file)
        post_button = WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "btn-post")]/button')))
        sleep(5)
        post_button.click()
        sleep(30)
    except Exception as e:
        log(e)


def upload_facebook(file):
    try:
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
        post_button = WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//div[contains(@aria-label, "Publish") and contains(@tabindex, "0")]')))
        post_button.click()
        sleep(50)
    except Exception as e:
        log(e)


log('Started Youtube Shorts Creator')
log('Creating new "{}" video...'.format(sys.argv[1]))

# Remove files
for file in glob.glob(os.getcwd() + '\\videos\\*'):
    os.remove(file)

# Run PHP Script
out = 1
retry = 2 if os.getenv('ENV') == 'dev' else 0
while out != 0:
    if retry < 3:
        out = subprocess.call("docker-compose run --rm --build php81-service php index.php \"{}\"".format(sys.argv[1]),
                              shell=True)
        retry += 1
    else:
        log("Could not generate video")
        quit()

if os.getenv('ENV') == 'dev':
    quit('In development mode')

if out == 0:
    try:
        # Get most recent file in videos
        list_of_files = glob.glob(os.getcwd() + '\\videos\\*')
        latest_file = list_of_files[0]

        if latest_file:
            options = uc.ChromeOptions()
            options.add_argument("--ignore-certificate-error")
            options.add_argument("--ignore-ssl-errors")
            options.add_argument("--user-data-dir=" + os.getenv('CHROME_USER_DIR'))
            options.add_argument("--headless")
            options.add_argument("--mute-audio")
            driver = uc.Chrome(options=options)

            log('Started Youtube Upload')
            upload_youtube(latest_file)
            log('Finished Youtube Upload')

            log('Started Instagram Upload')
            upload_ig(latest_file)
            log('Finished Instagram Upload')

            log('Started Tiktok Upload')
            upload_tiktok(latest_file)
            log('Finished Tiktok Upload')

            log('Started Facebook Upload')
            upload_facebook(latest_file)
            log('Finished Facebook Upload')

            # log('Started Posting to Twitter')
            # post_to_twitter()
            # log('Finished Posting to Twitter')

            log('Finished Youtube Shorts Creator')
            printQuota()
        else:
            log('No videos found')
    except Exception as e:
        log(e)
        quit()
else:
    log('PHP script failed')
quit()
