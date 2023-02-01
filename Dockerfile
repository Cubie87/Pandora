# import base
FROM ubuntu:jammy

# install os dependencies
RUN apt-get update
RUN apt-get install yt-dlp -y
RUN apt-get install python-is-python3 python3-pip -y

# install python dependencies
RUN pip install --upgrade pip
RUN pip install discord.py python-dotenv numpy
RUN pip install -U discord.py[voice]
#openai
RUN pip install openai


# make new user for network security
RUN useradd -ms /bin/bash pandora

# copy code over
ADD src /home/pandora


# default user pandora in home directory
USER pandora
WORKDIR /home/pandora
# run pandora
CMD python3 pandora.py
#CMD /bin/bash

