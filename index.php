<?php

require 'vendor/autoload.php';
require_once 'curl_wrapper.php';
use JSON2Video\Movie;
use JSON2Video\Scene;

// Create a new movie
$movie = new Movie;

// Set your API key
// Get your free API key at https://json2video.com
$movie->setAPIKey('FQ435dp2me3m4jdXqzyf87dEIryFxd963DCWwkIB');

// Set movie quality: low, medium, high
$movie->quality = 'high';
$movie->draft = false;
$movie->resolution = 'full-hd';
//$movie->width = 607;
//$movie->height = 1080;

$movie->addElement([
    'type' => 'video',
    'src' => 'https://drive.google.com/file/d/106GlzUvpHB-iZQhCUMKFQlxEkW7kmAQW/view?usp=sharing',
    'x' => -657,
]);


// Add text to screen in scenes
$resp = runCurl('https://www.reddit.com/r/Showerthoughts/.json');
$posts = array_slice($resp->data->children, 0, 9, true);
foreach ($posts as $post) {
    $text = $post->data->title;
    // Create a new scene
    $scene = new Scene;
    // Set the scene background color
    $scene->addElement([
        'type' => 'voice',
        'text' => $text,
        'start' => 1
    ]);

    $scene->addElement([
        'type' => 'text',
        'style' => '001',
        'text' => $text,
        'settings' => [
            'color' => '#FFFFFF',
            'font-size' => '60px',
            'font-family' => 'Roboto Condensed',
            'shadow' => 2,
            'text-align' => 'left',
            'vertical-align' => 'top'
        ],
    ]);

    // Add the scene to the movie
    $movie->addScene($scene);
}



// Call the API and start rendering the movie
$result = $movie->render();
var_dump($result);

//$result = $movie->getStatus('cLiLZ7fKeMvjb4b8');
//var_dump($result);

// Wait for the render to finish
$movie->waitToFinish();
var_dump($movie);
