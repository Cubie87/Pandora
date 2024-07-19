# import base image
FROM python:latest

# install python dependencies
RUN pip install --upgrade pip
RUN pip install discord.py PyNaCl python-dotenv numpy yt-dlp feedparser
# PyNaCl required for discord voice
# ffmpeg for yt-dlp
RUN apt-get update && apt-get install ffmpeg -y
#openai
RUN pip install openai

# make new user for network security
RUN useradd -ms /bin/bash pandora

# default user pandora in home directory
USER pandora
WORKDIR /home/pandora

# copy code over
COPY --chown=pandora src /home/pandora

# run pandora on container start
CMD python3 pandora.py

