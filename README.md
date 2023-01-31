# Pandora
A custom discord bot :D

 - Originally written to roll dice.
 - Eventually expanded to be able to cache and play youtube audio (using yt-dlp)
 - Added chatGPT interface (chat-davinci-003 model)


## Usage
Use `help` (with prefix) to see commands in Discord.

 - `help`: shows this command
 - `ping`: ping the bot
 - `roll` (or `r`): roll some dice
 - `join`: join the voice channel you're currently in
 - `leave` (or `dc`): leave the connected voice channel in the server
 - `play` (or `p`): play some music (control with `pause`/`resume`/`stop`)
 - `chat`: chat with the bot (OpenAI's chat-davinci-003 model)

The bot owner is also able to use the following commands:
 - `list`: list all the guilds that the bot is part of
 - `bail`: leave a guild
 - `sleep`: shut down the bot


All audio played is cached in `./media/` as mp3 files and can be deleted occasionally.


## Setup
To run your own instance of Pandora, you will need some extra files in the project's `src/` directory.

### Files

`.env` with
```
DISCORD_TOKEN=[Discord token here]
OPENAI_TOKEN=[OpenAI token here]
```

`variables.py` with
```py
class botVars:
    prefix = [prefix]
    owner = [numerical Discord ID]
```

Then, install dependencies.

### Program Dependencies

Install `yt-dlp` and `screen`
```
$ sudo apt install yt-dlp
$ sudo apt install screen
```

### Python Dependencies

If you don't have python3 and pip already, install them
```
$ sudo apt install python-is-python3 python3-pip
```

Install python dependencies
```
$ pip install discord.py
$ pip install python-dotenv
$ pip install -U discord.py[voice]
```

Then run `run.sh`
```
$ chmod +x run.sh
$ ./run.sh
```

Generate a discord bot invite URL on the applications page and invite to a server. 
