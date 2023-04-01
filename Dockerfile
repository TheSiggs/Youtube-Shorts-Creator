FROM php:8.1-cli

WORKDIR /var/www/project

RUN apt-get update && apt-get -y install ffmpeg

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

COPY . .