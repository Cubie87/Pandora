# import base
FROM ubuntu:jammy

# install os dependencies
RUN apt-get update
RUN apt-get install yt-dlp -y
RUN apt-get install python-is-python3 python3-pip -y

# install python dependencies
RUN pip install discord.py
RUN pip install python-dotenv
RUN pip install -U discord.py[voice]

CMD python
