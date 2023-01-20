# Pandora
A custom discord bot :D

 - Originally written to roll dice.
 - Eventually expanded to be able to cache and play youtube audio (using yt-dlp)
 - Added chatGPT interface (chat-davinci-003 model)


## Usage
To run Pandora, you will have to make your own files.

`.env` with
```
DISCORD_TOKEN=[Discord token here]

OPENAI_TOKEN=[OpenAI token here]
```


`variables.py` with
```
class botVars:
    prefix = [prefix]
    owner = [numerical Discord ID]
```

Then run `run.sh`

Generate a discord bot invite URL on the applications page and invite to a server. Use `help` (with prefix) to see commands.
The bot owner is also able to use the following commands:
`list`: list all the guilds that the bot is part of
`bail`: leave a guild
`sleep`: shut down the bot


All audio is cached in `./media/` and can be deleted occasionally.



