<?php

require 'vendor/autoload.php';
require_once 'curl_wrapper.php';
use JSON2Video\Movie;
use JSON2Video\Scene;

// Create a new movie
$movie = new Movie;

// Set your API key
// Get your free API key at https://json2video.com
$movie->setAPIKey('04QLiatYSb37jpsOwDZs56RjEPqE2Pfy3wcxWwab');

// Set movie quality: low, medium, high
$movie->quality = 'high';
$movie->draft = true;
$movie->width = 607;
$movie->height = 1080;

// Adds a video element directly to the movie
$movie->addElement([
    'type' => 'video',
    'src' => 'https://drive.google.com/file/d/106GlzUvpHB-iZQhCUMKFQlxEkW7kmAQW/view?usp=sharing',
    'x' => -657,
]);

// Fetch posts from the reddit api
$resp = runCurl('https://www.reddit.com/r/Showerthoughts/.json');
$posts = array_slice($resp->data->children, 0, 7, true);
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

    // Add a block with the post text on the screen
    $scene->addElement([
        'type' => 'component',
        'component' => 'basic/000',
        'settings' => [
            'card' => [
                'background' => 'white',
                'border-radius' => '10px'
            ],
            'headline' => [],
            'body' => [
                'text' => $text,
                'color' => 'black'
            ]
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