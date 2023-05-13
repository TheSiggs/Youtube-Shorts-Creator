import os
import sys

from dotenv import load_dotenv

from Entity.Logger import Logger
from Entity.VideoMaker import VideoMaker

if __name__ == '__main__':
    load_dotenv()
    subreddit = sys.argv[1]
    logger = Logger(os.getenv('ENV'))
    videoMaker = VideoMaker(subreddit, logger)
    video = videoMaker.generate_video()
    print(video)
