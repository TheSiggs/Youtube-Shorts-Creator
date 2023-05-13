import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class Twitter:
    def __init__(self, driver, logger, video_title):
        self.driver = driver
        self.logger = logger
        self.video_title = video_title

    def get_latest_youtube_vid(self):
        url = 'https://www.googleapis.com/youtube/v3/search?key=AIzaSyBAmzATERyHVgNkkEc4CDUqCD8ppn0fXLE&channelId=UCkrrIuQTIUcvVobIl_0ofTg&part=snippet,id&order=date&maxResults=1'
        links = requests.get(url)
        links_dict = links.json()
        youtube_links = ['https://www.youtube.com/shorts/{}'.format(item['id']['videoId']) for item in
                         links_dict['items']]
        return youtube_links[0]

    def post_to_twitter(self):
        self.driver.switch_to.new_window('tab')
        self.driver.get('https://studio.youtube.com/channel/UCkrrIuQTIUcvVobIl_0ofTg')
        sleep(10)
        latest_video = self.get_latest_youtube_vid()
        tweet = 'New {} Video! {}'.format(self.video_title, latest_video)
        self.driver.find_element(By.XPATH, '//div[@id="placeholder-cavgb"]').send_keys(tweet)
        sleep(2)
        self.driver.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]').click()