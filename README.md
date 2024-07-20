# Pandora
A custom discord bot :D

 - Originally written to roll dice
 - Export discord events to calendar function
 - Expanded to be able to cache and play YouTube audio (using yt-dlp)
 - Can grab video's audio for on the go listening (eg, on the bus), allowing for phone to be locked
    - This bypasses YouTube's paid feature where you can turn your screen off and still listen
    - Note no song queueing (yet. Maybe future feature???)
 - Has a ChatGPT interface (gpt-3.5-turbo)


## Usage
Use `help` (with prefix) to see commands in Discord.

 - `help`: shows this command
 - `ping`: ping the bot
 - `events`: send upcoming server events as `.ics` file
 - `roll` (or `r`): roll some dice
 - `join`: join the voice channel you're currently in
 - `leave` (or `dc`): leave the connected voice channel in the server
 - `play` (or `p`): play some music (control with `pause`/`resume`/`stop`)
 - `grab`: grab a youtube video, extract the audio, and reply with the audio file as a `.mp3`
 - `chat`: chat with the bot (OpenAI's gpt-3.5-turbo)
 

The bot owner is also able to use the following commands:
 - `list`: list all the guilds that the bot is part of
 - `bail`: leave a guild
 - `sleep`: shut down the bot

Bail allows the bot to be removed from a server without the owner being part of said server.

All audio played is cached in `./media/` as mp3 files and can be deleted occasionally.

Other misc commands not covered here are "easter eggs" and can be found by looking in the source code (not too difficult)


## Setup
To run your own instance of Pandora:

```sh
git clone https://github.com/Cubie87/Pandora
cd Pandora
```

you will need some extra files in the project's `src/` directory.

### Files
#### Environment Variables (API Keys)
```sh
vim src/.env
```
and add the following into the .env file:
```
DISCORD_TOKEN=[Discord token here]
OPENAI_TOKEN=[OpenAI token here]
```
#### Bot Variables
```sh
vim src/variables.py
```
with the following file content:
```py
class botVars:
    prefix = [prefix]
    owner = [numerical Discord ID]
    blocklist = [list of numerical Discord ID] # can be empty list
    gamePlayer = [list of numerical Discord ID] # can be empty list
```

`gamePlayer` are for users that play "the game" (you just lost the game)

The prefix should be a single character used as the prefix for bot commands.

Remove the `rsp` command (or figure it out and customise it!)

### Docker Compose

To run Pandora, ensure that you have docker and docker compose installed on your machine. Simply run `docker compose up -d` to start Pandora.

### First Server

Generate a discord bot management invite URL on the applications page of the developer portal and invite to a server. 
