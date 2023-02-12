<?php

use JSON2Video\Movie;
use JSON2Video\Scene;
use Google\Cloud\Translate\V2\TranslateClient;


class VideoGenerator {
    private Movie $movie;
    private mixed $chosenVideo;
    private mixed $subreddit;

    public function __construct($subreddit) {
        $this->movie = new Movie;
        $this->movie->setAPIKey($_ENV['JSON2VIDEO_API_KEY']);

        // Get a random video from the videos files
        $videos = json_decode(file_get_contents("videos.json"));
        $choice = array_rand($videos);
        $this->chosenVideo = ($videos[$choice]);

        // Set up options required to make the video
        $this->movie->quality = 'high';
        $this->movie->draft = $_ENV['ENV'] === 'dev';
        $this->movie->width = $this->chosenVideo->width;
        $this->movie->height = $this->chosenVideo->height;

        $this->subreddit = $subreddit;
    }

    /**
     * @return void
     * @throws Exception
     */
    public function generateVideo(): void {
        // Create a new movie
        echo "Generating video from " . $this->subreddit->name . PHP_EOL;

        // Adds a video element directly to the movie
        $this->movie->addElement([
            'type' => 'video',
            'src' => $this->chosenVideo->video_link,
            'x' => $this->chosenVideo->x,
            'z-index' => -1,
            'muted' => true
        ]);

        // Fetch posts from the reddit api
        $resp = $this->runCurl($this->subreddit->link);
        $posts = array_slice($resp->data->children, 0, $this->subreddit->posts, true);
        $titleText = $this->translateText($posts[0]->data->title, $this->subreddit->language);
        $videoTitle = sprintf('%s.mp4', $this->adjustText($titleText));

        // Loop through the post and create scenes for each post
        foreach ($posts as $post) {
            // Text formatting
            $initialText = $post->data->title;
            $translatedText = $this->translateText($initialText, $this->subreddit->language);
            $filteredText = $this->getFilteredText($translatedText);

            // Set up scene
            $scene = new Scene;
            $scene->background_color = 'transparent';

            // Adds text to speech for the scene
            $scene->addElement([
                'type' => 'voice',
                'text' => $translatedText,
                'start' => 1,
                'voice' => $this->subreddit->voice
            ]);

            $scene->addElement([
                'type' => 'text',
                'text' => $filteredText,
                'settings' => [
                    'font-size' => '3vh',
                    'text-shadow' => '2px 2px rgba(0, 0, 0, 1)',
                ]
            ]);
            // Add the scene to the movie
            $this->movie->addScene($scene);
        }
        // Call the API and start rendering the movie
        $this->movie->render();

        // Wait for the render to finish
        $newVideo = $this->movie->waitToFinish();

        $this->downloadVideo($videoTitle, $newVideo);
    }

    /**
     * @param $videoTitle
     * @param $newVideo
     * @return void Downloads a new video
     */
    private function downloadVideo($videoTitle, $newVideo): void {
        // Download video
        if (file_put_contents('./videos/'.$videoTitle, file_get_contents($newVideo['movie']['url']))) {
            echo "File downloaded successfully" . PHP_EOL;
        } else {
            echo "File downloading failed." . PHP_EOL;
        }
    }

    /**
     * cURL request
     *
     * General cURL request function for GET and POST
     * @param string $url URL to be requested
     */
    private function runCurl($url){
        $ch = curl_init($url);

        $options = array(
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_CONNECTTIMEOUT => 5,
            CURLOPT_TIMEOUT => 10
        );

        if (!empty($_SERVER['HTTP_USER_AGENT'])){
            $options[CURLOPT_USERAGENT] = $_SERVER['HTTP_USER_AGENT'];
        }

        curl_setopt_array($ch, $options);
        $apiResponse = curl_exec($ch);
        $response = json_decode($apiResponse);

        //check if non-valid JSON is returned
        if ($error = json_last_error()){
            $response = $apiResponse;
        }
        curl_close($ch);

        return $response;
    }

    /**
     * Returns a profanity filtered string
     * @param string $text
     * @return mixed
     */
    public function getFilteredText(string $text): mixed {
        $api = "https://www.purgomalum.com/service/json?";
        $query = http_build_query(['text' => $text]);
        return $this->runCurl($api.$query)->result;
    }

    /**
     * @param string $content Text to be translated
     * @param string $targetLanguage Language to translate in to (For list. See: https://cloud.google.com/translate/docs/languages)
     * @return mixed
     */
    public function translateText(string $content, string $targetLanguage): mixed {
        if ($targetLanguage !== 'en') {
            // Authenticate using the service account key file
            $translate = new TranslateClient([
                'key' => $_ENV['TRANSLATE_API_KEY']
            ]);
            // Translate the text
            $translation = $translate->translate($content, [
                'target' => $targetLanguage
            ]);
            if (is_null($translation)) {
                echo "Failed to translate text" . PHP_EOL;
                die();
            }
            // Print the translation
            return $translation['text'];
        }
        return $content;
    }

    /**
     * @param string $content
     * @return string
     */
    public function adjustText(string $content): string {
        $newTitle = substr($content, 0, 90);
        $newTitle .= ' #shorts';
        return $newTitle;
    }
}