import random
import shutil
import time
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import datetime
from pydub import AudioSegment
import subprocess
import requests
import json
import unicodedata
from google.cloud import texttospeech


class VideoMaker:
    def __init__(self, subreddit_name, logger):
        self.subreddit = subreddit_name
        self.transcripts = []
        self.audio_durations = []
        self.logger = logger

    def audio_from_text(self, text, output, trim=True):
        client = texttospeech.TextToSpeechClient()
        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)
        # Build the voice request, select the language code ("en-US") and the ssml voice gender
        voice = texttospeech.VoiceSelectionParams(
            language_code='en-US', ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        # The response's audio_content is binary
        with open(output, 'wb') as out:
            out.write(response.audio_content)
        if trim:
            # Load the audio file
            audio_clip = AudioFileClip(output)
            # Get the duration of the audio clip
            duration = audio_clip.duration
            # Trim the last 0.5 seconds of the audio clip
            trimmed_audio_clip = audio_clip.subclip(0, duration - 0.4)
            # Save the trimmed audio clip to a new file
            trimmed_audio_clip.write_audiofile(output)

    def generate_subtitle_file(self, durations, transcripts, subtitle_file_path):
        # Calculate the start and end times for each subtitle
        start_times = [datetime.timedelta(seconds=sum(durations[:i])) for i in range(len(durations))]
        end_times = [start_times[i] + datetime.timedelta(seconds=durations[i]) for i in range(len(durations))]

        # Generate the subtitle text
        subtitle_text = ''
        for i in range(len(transcripts)):
            # Format start and end time
            start_time = start_times[i]
            total_seconds = start_time.total_seconds()
            start_time = datetime.datetime.utcfromtimestamp(total_seconds).strftime('%-H:%M:%S,%f')

            end_time = end_times[i]
            total_seconds = end_time.total_seconds()
            end_time = datetime.datetime.utcfromtimestamp(total_seconds).strftime('%-H:%M:%S,%f')

            subtitle_text += '{}\n{} --> {}\n{}\n\n'.format(i + 1, start_time, end_time, transcripts[i])

        # Write the subtitle text to a file
        with open(subtitle_file_path, 'w') as f:
            f.write(subtitle_text)

    def setup_scenes(self, location):
        # Clean output folder
        if os.path.exists('videos'):
            # Delete the directory and its contents
            shutil.rmtree('videos')
        os.mkdir('videos')

        # Check if the directory exists
        if os.path.exists(location):
            # Delete the directory and its contents
            shutil.rmtree(location)

        os.makedirs(location, exist_ok=True)
        with open(f'{location}/scenes.txt', 'x') as _:
            pass

    def make_scene(self, text, sceneNo):
        location = f'temp_videos/scenes/scene_{sceneNo}'
        os.mkdir(location)
        currentDir = os.getcwd()
        with open(f'{location}/text.txt', 'x') as f:
            f.write(text)
        self.audio_from_text(text, f'{location}/speech.mp3')

        with open('temp_videos/scenes/scenes.txt', 'a') as file:
            file.write(f'file \'{currentDir}/{location}/speech.mp3\'\n')

        audio_file = AudioSegment.from_mp3(f'{location}/speech.mp3')
        duration = audio_file.duration_seconds
        self.audio_durations.append(duration)

    def generate_full_audio(self, text):
        location = f'temp_videos'
        self.audio_from_text(text, f'{location}/final_audio.mp3', False)

    def concat_scenes(self):
        subprocess.call('ffmpeg -f concat -safe 0 -i temp_videos/scenes/scenes.txt -c copy temp_videos/audio.mp3',
                        shell=True)

    def fetch_background_video(self, url):
        response = requests.get(url)
        with open("temp_videos/video.mp4", "wb") as f:
            f.write(response.content)

    def pick_random_video_object(self):
        # Open the JSON file in read mode
        with open('videos.json', 'r') as f:
            # Load the JSON data from the file
            data = json.load(f)
        return random.choice(data)

    def get_subreddit_from_subreddits_file(self, subreddit_name):
        # Open the JSON file in read mode
        with open('subreddits.json', 'r') as f:
            # Load the JSON data from the file
            data = json.load(f)
        for subreddit in data:
            if subreddit['name'] == subreddit_name:
                return subreddit

    def get_content(self, subreddit):
        for i in range(100):
            response = requests.get(subreddit['link'])
            if response.status_code == 200:
                posts = response.json()['data']['children'][:subreddit['posts']]
                content = []
                showTitle = subreddit['showTitle']
                showBody = subreddit['showBody']
                postsNo = subreddit['posts']
                title = unicodedata.normalize('NFC', posts[0]['data']['title']).encode('ascii', 'ignore').decode(
                    'ascii')
                if postsNo > 1:
                    for post in posts:
                        if showTitle:
                            text = unicodedata.normalize('NFC', post['data']['title']).encode('ascii', 'ignore').decode(
                                'ascii')
                            # words = text.split(' ')  # split the string into a list of words
                            # for i in range(0, len(words), 3):
                            #     content.append(" ".join(words[i:i]))
                            content.append(text)
                        if showBody:
                            bodyText = post['data']['selftext']
                            bodyText = unicodedata.normalize('NFC', bodyText).encode('ascii', 'ignore').decode('ascii')
                            words = bodyText.split('. ')  # split the string into a list of words
                            for chunk in words:
                                content.append(chunk + '. ')
                else:
                    post = posts[0]
                    if showTitle:
                        text = unicodedata.normalize('NFC', post['data']['title']).encode('ascii', 'ignore').decode(
                            'ascii')
                        content.append(text)
                    if showBody:
                        bodyText = post['data']['selftext']
                        bodyText = unicodedata.normalize('NFC', bodyText).encode('ascii', 'ignore').decode('ascii')
                        bodyText = bodyText.replace('\n', ' ', -1)
                        words = bodyText.split('. ')  # split the string into a list of words
                        for chunk in words:
                            content.append(chunk + '. ')
                return content, title
            elif response.status_code == 429:
                print(f"Too many requests. Retrying in {2} seconds...")
                time.sleep(2)
            else:
                print("Failed to make request after 5 attempts.")

    def cleanup(self):
        shutil.rmtree('temp_videos')

    def generate_video(self):
        try:
            subreddit = self.get_subreddit_from_subreddits_file(self.subreddit)
            video_object = self.pick_random_video_object()
            width = video_object['width']
            height = video_object['height']

            self.setup_scenes('temp_videos/scenes')

            # build audio and subtitles
            # Get text blocks to build audio from
            content, title = self.get_content(subreddit)
            for no, scene in enumerate(content):
                text = scene
                self.transcripts.append(text)
                self.make_scene(text, no)

            # self.concat_scenes()
            transcripts = ' '.join(self.transcripts)
            with open('temp_videos/transcripts.txt', 'w') as f:
                f.write(transcripts)

            self.generate_full_audio(transcripts)

            self.generate_subtitle_file(self.audio_durations, self.transcripts, 'temp_videos/subtitles.srt')

            # Set up background video
            self.fetch_background_video(video_object['video_link'])
            backgroundClip = VideoFileClip('temp_videos/video.mp4', audio=False)
            backgroundClip = backgroundClip.fx(vfx.crop, x1=width, x2=width * 2, y1=0, y2=height).fx(vfx.resize,
                                                                                                     width=width,
                                                                                                     height=height)
            # add subtitles
            subtitles = SubtitlesClip("temp_videos/subtitles.srt",
                                      lambda txt: TextClip(txt, font='Helvetica-Bold', fontsize=30, color='white',
                                                           size=backgroundClip.size, method='caption',
                                                           stroke_color='black',
                                                           stroke_width=0.8))

            subreddit_title = TextClip(subreddit['subreddit'], font='Helvetica-Bold', fontsize=28, color='white',
                                       size=backgroundClip.size, method='caption', stroke_color='black',
                                       stroke_width=0.8, align='north')

            audio = AudioFileClip("temp_videos/final_audio.mp3")
            video_with_subtitles = CompositeVideoClip([backgroundClip, subtitles, subreddit_title]).set_audio(audio)
            if audio.duration < 50:
                video_with_subtitles = video_with_subtitles.subclip(0, audio.duration)
            else:
                video_with_subtitles = video_with_subtitles.subclip(0, 50)

            videoTitle = title
            video = f"videos/{videoTitle}.mp4"
            video_with_subtitles.write_videofile(video)
            return video
        except Exception as e:
            self.logger.log(f'Error generating video - {self.subreddit}:')
            self.logger.log(e)
            return False
