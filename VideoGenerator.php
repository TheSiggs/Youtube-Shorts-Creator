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
        if (!$this->subreddit->showTitle && !$this->subreddit->showBody) {
            throw new Exception('Requires either showTitle or showBody to be true to continue');
        }

        if ($this->subreddit->posts < 1) {
            throw new Exception('Need to have one or more posts to generate video');
        }

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
        $filteredPosts = array_filter($resp->data->children, fn($post) => $post->data->stickied === false);
        $posts = array_slice($filteredPosts, 0, $this->subreddit->posts);

        if (count($posts) > 1) {
            // Loop through the post and create scenes for each post
            foreach ($posts as $post) {
                if ($this->subreddit->showTitle) {
                    $title = $post->data->title;
                    $this->generateScene($title);
                }
                if ($this->subreddit->showBody) {
                    $body = $post->data->selftext;
                    $this->generateScene($body);
                }
            }
        } else {
            $body = $posts[0]->data->selftext;
            $body = $this->cutWords($body, 170);
            $body = explode('.', $body);
            if ($this->subreddit->showTitle) {
                $title = $posts[0]->data->title;
                $this->generateScene($title);
            }
            foreach ($body as $bodyParts) {
                $this->generateScene($bodyParts, 0);
            }
        }
        // Call the API and start rendering the movie
        $this->movie->render();

        // Wait for the render to finish
        $newVideo = $this->movie->waitToFinish();

        $titleText = $this->translateText($posts[0]->data->title, $this->subreddit->language);
        $videoTitle = sprintf('%s.mp4', $this->adjustText($titleText));
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
     * This creates multiple scenes using predefined text
     * @param $text
     * @param int $delay
     * @return void
     * @throws Exception
     */
    private function generateScene($text, int $delay = 1): void {
        // Set up scene
        $scene = new Scene;
        $scene->background_color = 'transparent';

        // Adds text to speech for the scene
        $scene->addElement([
            'type' => 'voice',
            'text' => $text,
            'start' => $delay,
            'voice' => $this->subreddit->voice
        ]);

        $scene->addElement([
            'type' => 'text',
            'style' => "001",
            'text' => $text,
            'settings' => [
                'text-shadow' => '2px 2px rgba(0, 0, 0, 0.5)',
                'color' => '#FFFFFF',
            ],
        ]);

        // Add the scene to the movie
        $this->movie->addScene($scene);
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
     * @param string $text
     * @param int $limit
     * @return string
     */
    private function cutWords(string $text, int $limit = 200): string {
        $textArr = explode(' ', $text);
        if (count($textArr) > $limit) {
            return implode(' ', array_slice($textArr, 0, $limit));
        }
        return $text;
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