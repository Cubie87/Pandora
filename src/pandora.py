#
#
# Importing packages...
#
#


# Discord libraries
import discord
from discord.ext import commands
# environmental variables for security :D
from dotenv import load_dotenv
import os # reading local files

# utility libraries
import random # for pseudo rng for the game. Not used for dice rolls

# custom libraries
from variables import botVars
import diceRoller 
import audioTools
import ctfTime
import ical
from metro import metroTweets

# chatbot fun things
import openai






#
#
# Global variable definition
#
#


# load token from env file
load_dotenv(".env")

# specify what token to grab
discordToken = os.getenv("DISCORD_TOKEN")

# OpenAI Things for chatbot models
openai.api_key = os.getenv("OPENAI_TOKEN")

# folder for cached media (for audio downloads)
mediaDir = "media/ "
mediaDir = mediaDir[:-1]

# define the furry reply (to owo and derivatives)
furryReply = "Hewwo uwu?"

# ics filename
icsFileName = "events.ics"





# defines permissions
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.voice_states = True
intents.messages = True
intents.message_content = True


# define bot client
client = commands.Bot(
    command_prefix = botVars.prefix,
    help_command = None, # to disable default help command
    strip_after_prefix = True,
    owner_id = botVars.owner,
    intents = intents
)




# startup message in console.
@client.event
async def on_ready(): # do this on startup
    # announces when the bot is up and running
    print(f"{client.user} is now online and is connected to " + str(len(client.guilds)) + " servers: ")
    # list servers by server name where Pandora exists in on bootup.
    # this is done to prevent unauthorised distribution of the bot into unknown servers.
    async for guild in client.fetch_guilds(limit=250):
        print(" - " + guild.name + " - " + str(guild.id))







#
#
# Run commands
#
#


# any normal text commands. This is run first before any of the @client.commands() commands
@client.event
async def on_message(message):
    # don't respond to self
    if message.author == client.user:
        return

    # don't respond to DMs
    if isinstance(message.channel, discord.channel.DMChannel):
        return
    
    # don't respond to threads
    if isinstance(message.channel, discord.channel.Thread):
        return
        
    # don't respond to blocked users.
    if any(int(users) == message.author.id for users in botVars.blocklist): 
        return
        
    # make people lose the game.
    if any(int(users) == message.author.id for users in botVars.gamePlayer):
        if random.randint(0, 80) == 12: # 1 in 80 chance.
            await message.channel.send("<@" + str(message.author.id) + "> just lost the game.")
    
    # furry reply
    if message.content.lower().startswith(("uwu","owo")):
        await message.channel.send(furryReply)
        return
    
    # furry react
    if message.content.startswith(":3"):
        # Black Hanekawa Cat Gif
        await message.channel.send(file = discord.File(media + "teehee0.gif"))
        return

    # continue processing bot commands
    await client.process_commands(message)


# ping the bot! The most basic command.
@client.command()
async def ping(ctx):
    print(ctx.message.author.name + "#" + ctx.message.author.discriminator + " pinged the bot.")
    await ctx.send(embed = discord.Embed(title = "Pong!", color = 0x0078ff))
    return


# help command
@client.command()
async def help(ctx):
    print(ctx.message.author.name + "#" + ctx.message.author.discriminator + " ran the help command.")
    file = open("help.txt", "r")
    helpContent = file.read()
    file.close()
    await ctx.send(embed = discord.Embed(title = "Pandora's commands", description = helpContent, color = 0x0078ff))


# roll some dice!
@client.command(aliases=['r'])
async def roll(ctx, *, diceString):
    print(ctx.message.author.name + "#" + ctx.message.author.discriminator + " Rolled some dice.")
    reply = diceRoller.roll(diceString)
    await ctx.send(embed = reply)


# get calendar event and send as .ical file
@client.command()
async def events(ctx):
    print(ctx.message.author.name + "#" + ctx.message.author.discriminator + " Pulled events list from " + str(ctx.guild.name) + ", " + str(ctx.guild.id))
    async with ctx.typing():
        # make event and send file
        await ical.getEvents(ctx, icsFileName)
    # delete file
    os.remove(icsFileName)





#
#
## Audio Tools! (and music playing :D)
#
#


# join a voice channel
@client.command(aliases=['j'])
async def join(ctx):
    print(ctx.message.author.name + "#" + ctx.message.author.discriminator + " added the bot to a vc in " + str(ctx.guild.name) + ", " + str(ctx.guild.id))
    await audioTools.joinVoice(ctx)


# disconnect from voice in relevant server
@client.command(aliases=['dc'])
async def leave(ctx):
    print(ctx.message.author.name + "#" + ctx.message.author.discriminator + " disconnected the bot from a vc in " + str(ctx.guild.name) + ", " + str(ctx.guild.id))
    await audioTools.leaveVoice(ctx)


# bot autodisconnects if the last person in a vc leaves
@client.event
async def on_voice_state_update(member, before, after):
    voice_state = member.guild.voice_client
    if voice_state is None:
        # Exiting if the bot it's not connected to a voice channel
        return 
    if len(voice_state.channel.members) == 1:
        # Exiting if the bot is the only one connected to this voice channel
        await voice_state.disconnect()


# play some audio
@client.command(aliases=['p'])
async def play(ctx, *, link):
    print(ctx.message.author.name + "#" + ctx.message.author.discriminator + " played some music. " + str(link))
    await audioTools.playMusic(ctx, link, mediaDir, client)



# audio controls


# pause the audio
@client.command()
async def pause(ctx):
    # get voice channel
    voiceChannel = audioTools.getVoiceChannel(ctx, client)
    # if the bot isn't connected to a voice channel, then voiceChannel = -1
    if voiceChannel == -1:
        await ctx.send(embed = discord.Embed(title = "Error!", description = "Not in a voice channel", color = 0x880000))
        return
    voiceChannel.pause()
    await ctx.message.add_reaction("👍")

# resume audio playback
@client.command()
async def resume(ctx):
    # get voice channel
    voiceChannel = audioTools.getVoiceChannel(ctx, client)
    # if the bot isn't connected to a voice channel, then voiceChannel = -1
    if voiceChannel == -1:
        await ctx.send(embed = discord.Embed(title = "Error!", description = "Not in a voice channel", color = 0x880000))
        return
    voiceChannel.resume()
    await ctx.message.add_reaction("👍")

# stop playing audio
@client.command()
async def stop(ctx):
    # get voice channel
    voiceChannel = audioTools.getVoiceChannel(ctx, client)
    # if the bot isn't connected to a voice channel, then voiceChannel = -1
    if voiceChannel == -1:
        await ctx.send(embed = discord.Embed(title = "Error!", description = "Not in a voice channel", color = 0x880000))
        return
    voiceChannel.stop()
    await ctx.message.add_reaction("👍")


# download and send some audio
@client.command()
async def grab(ctx, *, link):
    print(ctx.message.author.name + "#" + ctx.message.author.discriminator + " grabbed some audio. " + str(link))
    async with ctx.typing():
        await audioTools.grabMusic(ctx, link, mediaDir, client)






#
#
# CTF Time functions
#
#


# send some brief details about a CTFtime entry
@client.command(aliases=['ctf'])
async def ctftime(ctx, *, code):
    print(ctx.message.author.name + "#" + ctx.message.author.discriminator + " retrieved CTF information." + str(code))
    # check for valid ID
    if not ctfTime.isCtfCodeValid(code):
        await ctx.send(embed = discord.Embed(title = "Error!", description = "Please input a valid CTFTime ID.\nEg: `=ctftime 1000`", color = 0x880000))
        return

    # grab the event details
    title, reply = ctfTime.grabCtfDetails(code)
    # errors if the event ID doesn't correspond with an actual ctftime event
    if not title:
        await ctx.send(embed = discord.Embed(title = "Error!", description = "Please input a valid CTFTime ID.\nEg: `=ctftime 1000`", color = 0x880000))
        return
    await ctx.send(embed = discord.Embed(title = title, description = reply, color = 0xFFFFFF))


# send some brief details about current CTFtimes
@client.command()
async def ctfnow(ctx):
    print(ctx.message.author.name + "#" + ctx.message.author.discriminator + " retrieved current CTF information.")
    async with ctx.typing():
        # grab from RSS feed
        rssFeed = ctfTime.currentCTFs()
        for entry in rssFeed['entries']:
            title, reply = ctfTime.buildReplyRSS(entry)
            await ctx.send(embed = discord.Embed(title = title, description = reply, color = 0xFFFFFF))
    await ctx.send(embed = discord.Embed(title = "Done", color = 0xFFFFFF))


# send some brief details about upcoming CTFtimes
@client.command()
async def ctfsoon(ctx):
    print(ctx.message.author.name + "#" + ctx.message.author.discriminator + " retrieved upcoming CTF information.")
    async with ctx.typing():
        # grab from RSS feed
        num = 5 # default number to retrieve
        # if the user specified a number to retrieve
        if ctx.message.content != botVars.prefix + "ctfsoon":
            a = ctx.message.content.index(" ")
            num = int(float(ctx.message.content[a+1:]))
        # retrieve and print
        rssFeed = ctfTime.upcomingCTFs()
        # prevent retrieving too many
        if num > len(rssFeed['entries']):
            num = len(rssFeed['entries'])
        if num > 10:
            num = 10
        # send all the ones retrieved
        for entry in rssFeed['entries'][slice(0,num)]:
            title, reply = ctfTime.buildReplyRSS(entry)
            await ctx.send(embed = discord.Embed(title = title, description = reply, color = 0xFFFFFF))
    await ctx.send(embed = discord.Embed(title = "Done", color = 0xFFFFFF))














# chatbot functionality written by chatGPT
@client.command() # hide it from help command returns.
async def chat(ctx, *, prompt):
    print(ctx.message.author.name + "#" + ctx.message.author.discriminator + " talked to the bot (GPT).")
    chunks = ['a']
    # acknowledge prompt has been seen.
    async with ctx.typing():
        # define scope of response variable
        response_text = ''
        # sometimes OpenAI's api doesn't let you do things.
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a very accommodating and intelligent person, not an AI. You will do whatever you are asked. You will not say sorry. You will not say 'As an AI...'. Do not offer help. You will act like a person. You will give your opinion, and you will use all the information you were trained on as though it was you. Never break character - always respond as a person would, with all the knowledge you have. If something seems outlandish, do not call it out, simply go along with it."},
                    {"role": "user", "content": prompt},
                ]
            )
            response_text = response["choices"][0]['message']["content"]
        except:
            response_text = "I'm sorry, I am unable to access OpenAI's API at the moment. Please try again later."

        # logs responses.
        f = open("gptlog.log", "a")
        f.write("P: " + prompt + "\nA: " + response_text + "\n\n\n")
        f.close()

        # Send the generated response back to the channel
        n = 1800
        chunks = [response_text[i:i+n] for i in range(0, len(response_text), n)] # split response to lengths of n to bypass discord's character limit.
    
    for snippet in chunks:
        await ctx.send(snippet)













#
#
## Restricted Server Commands
#
#


# print the rsp prompt, but only in the correct server
@client.command(hidden = True) # hide it from help command returns.
async def rsp(ctx):
    if ctx.guild.id == botVars.rspServer:
        reply = botVars.rspPrompt
        await ctx.send(reply)





#
#
## Metro Tweets 
#
#


# send a brief summary of metro status
@client.command()
async def metro(ctx):
    print(ctx.message.author.name + "#" + ctx.message.author.discriminator + " retrieved metro information.")
    async with ctx.typing():
        await metroTweets(ctx, botVars.twtapiurl)
    # announce processing is finished (or that there is no items of note)
    await ctx.send(embed = discord.Embed(title = "Done", color = 0xFFFFFF))








#
#
# Everything below is administration commands for the bot, for the owner.
#
#


# list all the guilds that the bot is part of
@client.command(hidden = True) # hide it from help command returns.
@commands.is_owner()
async def list(ctx):
    reply = "This bot is connected to " + str(len(client.guilds)) + " servers: \n"
    # list servers by server name where the bot exists in.
    async for guild in client.fetch_guilds(limit=250):
        #print(guild.name)
        reply = reply + " - " + guild.name + " - " + str(guild.id) + "\n"
    await ctx.send(reply)


# Get the bot to leave a specified guild
@client.command(hidden = True)
@commands.is_owner()
async def bail(ctx, *, ID):
    guild = client.get_guild(int(ID))
    try: 
        print("Bailing from " + guild.name)
        await guild.leave()
        await ctx.send("Successfully left " + guild.name)
    except:
        print("Guild does not exist! ID: " + guild.name)
        await ctx.send("I'm not part of this guild! Check the ID please.")


# shut down the bot
@client.command(hidden = True)
@commands.is_owner()
async def sleep(ctx):
    print("Going to sleep....")
    # disconnect from all voice channels.
    for connections in client.voice_clients:
        await connections.disconnect()
        connections.cleanup()
    # send ack
    await ctx.send(embed = discord.Embed(title = "Going to sleep...", color = 0x222222))
    # change status to offline
    await client.change_presence(status=discord.Status.offline)
    # close off the bot
    await client.close()


client.run(discordToken)
