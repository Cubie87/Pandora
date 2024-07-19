# import base image
FROM python:latest

# install python dependencies
RUN pip install --upgrade pip
RUN pip install discord.py python-dotenv numpy yt-dlp feedparser
#openai
RUN pip install openai

# make new user for network security
RUN useradd -ms /bin/bash pandora

# copy code over
COPY src /home/pandora

# default user pandora in home directory
USER pandora
WORKDIR /home/pandora
# run pandora on container start
CMD python3 pandora.py

