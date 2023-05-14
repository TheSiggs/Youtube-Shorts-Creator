import os
import subprocess
import sys
from Entity.Logger import Logger
from dotenv import load_dotenv
from Entity.Platforms.Facebook import Facebook
from Entity.Platforms.Instagram import Instagram
from Entity.Platforms.TikTok import TikTok
from Entity.Platforms.Youtube import Youtube
from Entity.VideoUploader import VideoUploader

if __name__ == '__main__':
    load_dotenv()
    subreddit = sys.argv[1]
    logger = Logger(os.getenv('ENV'))

    out = subprocess.call(f"docker-compose run --rm --build ubuntu python3 make_video.py  \"{subreddit}\"", shell=True)

    if os.getenv('ENV') == 'dev':
        quit()

    # Get most recent file in videos
    list_of_files = [f for f in os.listdir('videos') if os.path.isfile(os.path.join('videos', f))]
    newVideo = f'{os.getcwd()}/videos/{list_of_files[0]}'

    print(newVideo)
    if newVideo:
        uploader = VideoUploader(logger, os.getenv('CHROME_USER_DIR'))
        uploader_driver = uploader.get_driver()

        youtube = Youtube(uploader_driver, logger)
        youtube.upload(newVideo)

        instagram = Instagram(uploader_driver, logger)
        instagram.upload(newVideo)

        tiktok = TikTok(uploader_driver, logger)
        tiktok.upload(newVideo)

        facebook = Facebook(uploader_driver, logger)
        facebook.upload(newVideo)
    else:
        logger.log('Failed to generate video... quitting')
        quit()
quit()

