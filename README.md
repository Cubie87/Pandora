# Pandora
A custom discord bot :D

 - Originally written to roll dice.
 - Eventually expanded to be able to cache and play youtube audio (using yt-dlp)
 - Added chatGPT interface (chat-davinci-003 model)


## Setup
To run Pandora, some files need to be created in the project's root directory.

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

Install `yt-dlp` and `screen`
```
$ sudo apt install yt-dlp
$ sudo apt install screen
```

Then run `run.sh`
```
$ chmod +x run.sh
$ ./run.sh
```

## Usage

Generate a discord bot invite URL on the applications page and invite to a server. Use `help` (with prefix) to see commands in Discord.

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



