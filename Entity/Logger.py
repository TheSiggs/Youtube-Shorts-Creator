import requests


class Logger:
    def __init__(self, is_dev):
        self.is_dev = is_dev
        self.headers = {"Authorization": "Bearer xoxb-2102419125553-4890952961859-MnsB3ow5KnQx8iBdmi1oDKvz"}
        self.channel = "C04S0BQCSS2"

    def log(self, error):
        if self.is_dev:
            print(error)
        else:
            data = {
                "channel": self.channel,
                "text": error
            }
            requests.post('https://slack.com/api/chat.postMessage', headers=self.headers, data=data)
