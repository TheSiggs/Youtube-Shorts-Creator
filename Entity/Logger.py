import requests
import os

class Logger:
    def __init__(self, is_dev):
        self.is_dev = is_dev
        self.headers = {"Authorization": "Bearer " + os.getenv('SLACK_TOKEN')}
        self.channel = os.getenv('SLACK_CHANNEL')

    def log(self, error):
        if self.is_dev:
            print(error)
        else:
            data = {
                "channel": self.channel,
                "text": error
            }
            requests.post('https://slack.com/api/chat.postMessage', headers=self.headers, data=data)
