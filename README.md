# Pandora
A custom discord bot :D

 - Originally written to roll dice.
 - Expanded to be able to cache and play YouTube audio (using yt-dlp)
 - Can grab video's audio for on the go listening (eg, on the bus), allowing for phone to be locked
    - This bypasses YouTube's paid feature where you can turn your screen off and still listen
 - Has a ChatGPT interface (text-davinci-003)


## Usage
Use `help` (with prefix) to see commands in Discord.

 - `help`: shows this command
 - `ping`: ping the bot
 - `roll` (or `r`): roll some dice
 - `join`: join the voice channel you're currently in
 - `leave` (or `dc`): leave the connected voice channel in the server
 - `play` (or `p`): play some music (control with `pause`/`resume`/`stop`)
 - `grab`: grab a youtube video, extract the audio, and reply with the audio file as a `.mp3`
 - `chat`: chat with the bot (OpenAI's text-davinci-003)
 

The bot owner is also able to use the following commands:
 - `list`: list all the guilds that the bot is part of
 - `bail`: leave a guild
 - `sleep`: shut down the bot

Bail allows the bot to be removed from a server without the owner being part of said server.


All audio played is cached in `./media/` as mp3 files and can be deleted occasionally.


## Setup
To run your own instance of Pandora, you will need some extra files in the project's `src/` directory.

### Files

`src/.env` with
```
DISCORD_TOKEN=[Discord token here]
```

`src/variables.py` with
```py
class botVars:
    prefix = [prefix]
    owner = [numerical Discord ID]
    blocklist = [list of numerical Discord ID] # can be empty list
```
The prefix should be a single character used as the prefix for bot commands.

Remove the rsp command, along with the metro command

Then, install dependences 

### Program Dependencies

Install `screen`
```bash
sudo apt install screen
```

#### Python Dependencies

If you don't have python3 and pip already, install them
```bash
sudo apt install python-is-python3 python3-pip ffmpeg
```

Install python dependencies
```bash
pip install discord.py python-dotenv numpy yt-dlp openai feedparser
pip install -U discord.py[voice]
```

Then run `run.sh`
```bash
chmod +x run.sh
./run.sh
```

Remember that Pandora will run in a detached screen. To re-attach, `$ screen -r pandora`. To detach, `Ctrl+A, Ctrl+D`.


Alternatively, run `docker build -t pandora .` to build the docker image, and `docker run pandora` to run pandora. Please note that the docker image is not thoroughly tested and may contain bugs.

Generate a discord bot invite URL on the applications page and invite to a server. 
