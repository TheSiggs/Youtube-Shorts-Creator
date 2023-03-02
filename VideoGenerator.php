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
        $titleText = $this->translateText($posts[0]->data->title, $this->subreddit->language);
        $videoTitle = sprintf('%s.mp4', $this->adjustText($titleText));
        // Loop through the post and create scenes for each post
        foreach ($posts as $post) {
            // Set up scene
            $scene = new Scene;
            $scene->background_color = 'transparent';

            $title = $post->data->title;
            $body = $post->data->selftext;

            // Voice Component
            $voiceText = '';
            if ($this->subreddit->showTitle) {
                $voiceText .= $title;
            }
            if ($this->subreddit->showBody) {
                $voiceText .= $body;
            }

            $voiceText = $this->cutWords($voiceText);

            // Text Component
            if ($this->subreddit->showTitle && $this->subreddit->showBody) {
                $headlineText = $title;
                $bodyText = $body;
            } else {
                $headlineText = '';
                $bodyText = $this->subreddit->showTitle ? $title : $body;
            }

            $bodyText = $this->cutWords($bodyText, 200);

            // Adds text to speech for the scene
            $scene->addElement([
                'type' => 'voice',
                'text' => $voiceText,
                'start' => 1,
                'voice' => $this->subreddit->voice
            ]);

            $scene->addElement([
                'type' => 'component',
                'component' => 'basic/000',
                'settings' => [
                    'card' => [
                        'background-color' => 'white',
                        'border' => '10px',
                        'transform' => 'translate(0px, 100px)'
                    ],
                    'headline' => [
                        'text' => $headlineText,
                        'color' => 'white',
                    ],
                    'body' => [
                        'text' => [
                            $bodyText,
                        ],
                        "color" => "black",
                    ],
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
     * @param string $text
     * @param int $limit
     * @return string
     */
    private function cutText(string $text, int $limit = 200): string {
        if (strlen($text) < $limit) {
            return $text;
        }

        $newText = explode(' ', $text);
        $textCount = 0;
        $returnText = [];
        foreach ($newText as $textItem) {
            $textCount += strlen($textItem);
            if ($textCount < $limit) {
                $returnText[] = $textItem;
            } else {
                return implode(' ', $returnText);
            }
        }
        return $text;
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