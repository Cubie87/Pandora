# import base
FROM ubuntu:jammy

# install os dependencies
RUN apt-get update --fix-missing
RUN apt-get install python-is-python3 python3-pip ffmpeg -y
# I would add gnu screen to be able to reattach to Pandora's output
# but docker really does not like it. Blows the build time to >2hr
# and crashes the build. If you have a solution please let me know.

# install python dependencies
RUN pip install --upgrade pip
RUN pip install discord.py python-dotenv numpy yt-dlp feedparser
RUN pip install -U discord.py[voice]
#openai
RUN pip install openai


# make new user for network security
RUN useradd -ms /bin/bash pandora

# copy code over
COPY src /home/pandora


# default user pandora in home directory
USER pandora
WORKDIR /home/pandora
# run pandora
CMD python3 pandora.py
#CMD /bin/bash

