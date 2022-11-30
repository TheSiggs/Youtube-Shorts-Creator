<?php

require_once realpath(__DIR__ . '/vendor/autoload.php');

$dotenv = Dotenv\Dotenv::createImmutable(__DIR__);
$dotenv->load();


require_once 'curl_wrapper.php';
use JSON2Video\Movie;
use JSON2Video\Scene;

/**
 * MOVIE CREATION
 */
/*
// Create a new movie
$movie = new Movie;

// Set your API key
// Get your free API key at https://json2video.com
$movie->setAPIKey($_ENV['JSON2VIDEO_API_KEY']);

// Get a random video from the videos files
$videos = json_decode(file_get_contents("videos.json"));
$choice = array_rand($videos);
$chosenVideo = ($videos[$choice]);

// Set movie quality: low, medium, high
$movie->quality = 'high';
$movie->draft = $_ENV['ENV'] === 'dev';
$movie->width = $chosenVideo->width;
$movie->height = $chosenVideo->height;

// Adds a video element directly to the movie
$movie->addElement([
    'type' => 'video',
    'src' => $chosenVideo->video_link,
    'x' => $chosenVideo->x,
    'z-index' => -1,
]);

// Fetch posts from the reddit api
$resp = runCurl($_ENV['SUBREDDIT']);
$posts = array_slice($resp->data->children, 0, 5, true);
// Loop through the post and create scenes for each post
foreach ($posts as $post) {
    $text = $post->data->title; // Text to be used for each scene
    $scene = new Scene;
    // Adds text to speech for the scene
    $scene->addElement([
        'type' => 'voice',
        'text' => $text,
        'start' => 1
    ]);
    $scene->background_color = 'transparent';

    // Add a block with the post text on the screen
//    $scene->addElement([
//        'type' => 'component',
//        'component' => 'basic/000',
//        "background-color" => "transparent",
//        'settings' => [
//            'card' => [
//                'background' => 'white',
//                'border-radius' => '10px'
//            ],
//            'headline' => [],
//            'body' => [
//                'text' => $text,
//                'color' => 'black'
//            ]
//        ]
//    ]);
    $scene->addElement([
        'type' => 'text',
        'text' => $text,
        'settings' => [
            'font-size' => '5vh',
            'text-shadow' => '2px 2px rgba(0,0,0, 1)',
        ]
    ]);
    // Add the scene to the movie
    $movie->addScene($scene);
}

// Call the API and start rendering the movie
$result = $movie->render();

// Wait for the render to finish
$video = $movie->waitToFinish();

// Download video
$url = $video['movie']['url'];
$file_name = basename($url);
if (file_put_contents($file_name, file_get_contents($url))) {
    echo "File downloaded successfully" . PHP_EOL;
} else {
    echo "File downloading failed." . PHP_EOL;
}
*/
/**
 * VIDEO UPLOAD
 */

$client = new Google_Client();
$client->setApplicationName('API code samples');
$client->setScopes([
    'https://www.googleapis.com/auth/youtube.upload',
]);
$client->setAuthConfig('secret.json');
$client->setAccessType('online');

// Request authorization from the user.
// TODO: FIGURE OUT HOW TO AUTOMATE THIS
$authUrl = $client->createAuthUrl();
printf("Open this link in your browser:\n%s\n", $authUrl);
print('Enter verification code: ');
$authCode = trim(fgets(STDIN));

// Exchange authorization code for an access token.
$accessToken = $client->fetchAccessTokenWithAuthCode($authCode);
$client->setAccessToken($accessToken);

// Define service object for making API requests.
$service = new Google_Service_YouTube($client);

// Define the $video object, which will be uploaded as the request body.
$video = new Google_Service_YouTube_Video();

// Add 'snippet' object to the $video object.
$videoSnippet = new Google_Service_YouTube_VideoSnippet();
$videoSnippet->setCategoryId('22');
//$videoSnippet->setDescription('Description of uploaded video.');
// TODO: SET THIS DYNAMICALLY
$videoSnippet->setTitle('Shower Thoughts 3');
$videoSnippet->setTags(explode(',', $_ENV['TAGS']));
$video->setSnippet($videoSnippet);

// Add 'status' object to the $video object.
$videoStatus = new Google_Service_YouTube_VideoStatus();
$videoStatus->setPrivacyStatus('public');
$video->setStatus($videoStatus);

$response = $service->videos->insert(
    'snippet,status',
    $video,
    array(
        // TODO: SET THIS DYNAMICALLY
        'data' => file_get_contents("2022-11-30-27751.mp4"),
        'mimeType' => 'application/octet-stream',
        'uploadType' => 'multipart'
    )
);
print_r($response);
