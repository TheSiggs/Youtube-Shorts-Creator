<?php

require 'vendor/autoload.php';
require_once 'curl_wrapper.php';
use JSON2Video\Movie;
use JSON2Video\Scene;

// Create a new movie
$movie = new Movie;

// Set your API key
// Get your free API key at https://json2video.com
$movie->setAPIKey('GUqCH3WziX8Z0qx4xxjIFRaxoCkC8Kl7EyVYOTGi');

// Set movie quality: low, medium, high
$movie->quality = 'high';
$movie->draft = true;

// Create a new scene
$scene = new Scene;

// Set the scene background color
$scene->background_color = '#4392F1';

// Add a text element printing "Hello world" in a fancy way (basic/006)
// The element is 10 seconds long and starts 2 seconds from the scene start
// Element's vertical position is 50 pixels from the top

// Add text to screen in scenes

$resp = runCurl('https://www.reddit.com/r/Showerthoughts/.json');
$posts = array_slice($resp->data->children, 0, 5, true);
foreach ($posts as $post) {
    $text = $post->data->title;
    $scene->addElement([
        'type' => 'voice',
        'text' => $text,
        'voice' => 'en-GB-LibbyNeural',
        'start' => 1.5
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
