#!/bin/bash

url=$(php index.php | grep "Movie URL" | sed 's/Movie URL: //')
wget $url;