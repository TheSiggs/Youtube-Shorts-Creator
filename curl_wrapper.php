<?php
/**
 * cURL request
 *
 * General cURL request function for GET and POST
 * @param string $url URL to be requested
 */
function runCurl($url){
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