<?php
require 'vendor/autoload.php';

require_once realpath(__DIR__ . '/vendor/autoload.php');
require_once realpath(__DIR__ . '/VideoGenerator.php');
$dotenv = Dotenv\Dotenv::createImmutable(__DIR__);
$dotenv->load();

// Reads the videos from a json file and creates the videos. This will be replaced with variables in the future
$subreddits = array_filter(json_decode(file_get_contents("subreddits.json")), fn ($video) => $video->include === true);
foreach ($subreddits as $subreddit) {
    $VideoGenerator = new VideoGenerator($subreddit);
    $VideoGenerator->generateVideo();
}
