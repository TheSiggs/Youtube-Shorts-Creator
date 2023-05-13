FROM ubuntu:jammy

WORKDIR /var/local

ENV TZ=Australia/Sydney

RUN apt-get update && apt-get install -y ffmpeg curl wget software-properties-common tzdata festival espeak imagemagick && \
    add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get update

RUN apt-get install -y python3.8 python3-pip

COPY requirements.txt /var/local/requirements.txt

RUN pip3 install -r requirements.txt

COPY policy.xml /etc/ImageMagick-6/policy.xml

COPY google-tts-credentials.json /var/local/google-tts-credentials.json
ENV GOOGLE_APPLICATION_CREDENTIALS /var/local/google-tts-credentials.json

