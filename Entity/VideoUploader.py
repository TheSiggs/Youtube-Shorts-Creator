import undetected_chromedriver as uc


class VideoUploader:
    def __init__(self, logger, chrome_user_dir):
        self.logger = logger
        self.options = uc.ChromeOptions()
        self.options.add_argument("--ignore-certificate-error")
        self.options.add_argument("--ignore-ssl-errors")
        self.options.add_argument("--user-data-dir=" + chrome_user_dir)
        # self.options.add_argument("--headless")
        self.options.add_argument("--mute-audio")
        self.driver = uc.Chrome(options=self.options)

    def get_driver(self):
        return self.driver
