#
#
# importing packages...
#
#


# Discord libraries
import discord
from discord.ext import commands
# environmental variables for security :D
from dotenv import load_dotenv
import os # reading .env file

# custom libraries
from variables import botVars
import diceRoller 
import audioTools






#
#
# Global variable definition
#
#



# chatbot fun things
import openai

# load token from env file
load_dotenv(".env")

# specify what token to grab
discordToken = os.getenv("DISCORD_TOKEN")

# OpenAI Things for chatbot models
openai.api_key = os.getenv("OPENAI_TOKEN")



# folder for cached media (for audio downloads)
media = "media/ "
media = media[:-1]

# define the furry reply (to owo and derivatives)
furryReply = "Hewwo uwu"




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




# ping the bot! The most basic command.
@client.command()
async def ping(ctx):
    print(ctx.message.author.name + "#" + ctx.message.author.discriminator + " pinged the bot.")
    await ctx.send(embed = discord.Embed(title = "Pong!", color = 0x0078ff))

# help command
@client.command()
async def help(ctx):
    file = open("help.txt", "r")
    await ctx.send(embed = discord.Embed(title = "Pandora's commands", description = file.read(), color = 0x0078ff))
    file.close()

# roll some dice!
@client.command(aliases=['r'])
async def roll(ctx, *, diceString):
    print(ctx.message.author.name + "#" + ctx.message.author.discriminator + " Rolled some dice.")
    reply = diceRoller.roll(diceString)
    await ctx.send(embed = reply)




#
## Audio Tools! (and music playing :D)
#



# join a voice channel
@client.command(aliases=['j'])
async def join(ctx):
    # runs a pre-join check to see if the message is valid
    channel = audioTools.preJoinCheck(ctx)
    # if the user is not in a channel, then channel = 0, and there will be an error message
    if channel == 0:
        await ctx.send(embed = discord.Embed(title = "Error!", description = "Please join a voice channel first!", color = 0x880000))
        return
    # otherwise, channel is the voice channel that the user is currently connected to.
    await channel.connect()
    await ctx.message.add_reaction("👍")
    print("Joining a voice channel!")


# disconnect from voice in relevant server
@client.command(aliases=['leave', 'exit', 'quit'])
async def dc(ctx):
    try:
        await ctx.voice_client.disconnect()
    except: # if we're not voice connected, let them know!
        await ctx.send(embed = discord.Embed(title = "Error!", description = "I'm not in a voice channel here!", color = 0x880000))
    else:
        print("Leaving a voice channel!")
        await ctx.message.add_reaction("👍")


# bot autodisconnects if there's no one in the voice channel
@client.event
async def on_voice_state_update(member, before, after):
    voice_state = member.guild.voice_client
    if voice_state is None:
        # Exiting if the bot it's not connected to a voice channel
        return 

    if len(voice_state.channel.members) == 1:
        await voice_state.disconnect()


# play some audio
@client.command(aliases=['p'])
async def play(ctx, *, link):
    # ctx.voice_client
    print("Gonna try to play some music")
    print(client.voice_clients)

    
    if audioTools.checkInvalidLink(link):
        await ctx.send(embed = discord.Embed(title = "Error!", description = "Please input a valid YouTube ID.\nEg: `=play dQw4w9WgXcQ`", color = 0x880000))
        return
    
    # get the right voice connection
    voiceChannel = audioTools.getVoiceChannel(ctx, client)

    # if the bot isn't connected to a voice channel, then voiceChannel = -1
    if voiceChannel == -1:
        await ctx.send(embed = discord.Embed(title = "Error!", description = "Please connect the bot to a voice channel. `=join`", color = 0x880000))
        return

    # if the file does exist, play!
    if os.path.isfile(media + link + ".mp3"):
        try:
            voiceChannel.play(discord.FFmpegPCMAudio(media + link + ".mp3"))
        except:
            ctx.send(embed = discord.Embed(title = "Error!", description = "Please join a voice channel to play music.", color = 0x880000))
        return
    
    await ctx.message.add_reaction("👍")
    # the file doesn't exist! Need to download it.
    os.system("yt-dlp -x --audio-format mp3 --audio-quality 0  -o '" + media + link + ".%(ext)s' " + "'https://www.youtube.com/watch?v=" + link + "'")

    voiceChannel.play(discord.FFmpegPCMAudio(media + link + ".mp3"))
    await ctx.message.add_reaction("➡")


# audio controls


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
    print("Pausing")
    
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
    print("Resuming Playback")
    
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
    print("Stopping Playback")




# download and send some audio
@client.command()
async def grab(ctx, *, link):
    # check for attack    
    if audioTools.checkInvalidLink(link):
        await ctx.send(embed = discord.Embed(title = "Error!", description = "Please input a valid YouTube ID.\nEg: `=play dQw4w9WgXcQ`", color = 0x880000))
        return
    
    await ctx.message.add_reaction("👍")
    # if the file does exist, send!
    if os.path.isfile(media + link + ".mp3"):
        try:
            await ctx.send(file=discord.File(media + link + ".mp3"))
        except:
            await ctx.send(embed = discord.Embed(title = "Error!", description = "File is too large.", color = 0x880000))
        else:
            await ctx.message.add_reaction("➡")
        return

    # the file doesn't exist! Need to download it.
    os.system("yt-dlp -x --audio-format mp3 --audio-quality 0  -o '" + media + link + ".%(ext)s' " + "'https://www.youtube.com/watch?v=" + link + "'")

    try:
        await ctx.send(file=discord.File(media + link + ".mp3"))
    except:
        await ctx.send(embed = discord.Embed(title = "Error!", description = "File is too large.", color = 0x880000))
    else:
        await ctx.message.add_reaction("➡")



# any normal text commands. This is run first before any of the @client.commands() commands
@client.event
async def on_message(message):
    # don't respond to the bot
    if message.author == client.user:
        return
    
    # don't respond to DMs
    if isinstance(message.channel, discord.channel.DMChannel):
        return
    
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









# chatbot functionality written by chatGPT
@client.command() # hide it from help command returns.
async def chat(ctx, *, prompt):
    # acknowledge prompt has been seen.
    await ctx.message.add_reaction("👍")
    #print(prompt) # verify the prompt has preamble removed.
    response = "I'm sorry, I am unable to access OpenAI's API at the moment. Please try again later."

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
    )
    response_text = response["choices"][0]["text"]
    
    file = open("logs/gptlog.log", 'a')
    file.write("Q: " + prompt + "\n")
    file.write("A: " + response_text + "\n\n\n\n\n")
    file.close()

    # Send the generated response back to the channel
    await ctx.send(response_text)
    # acknowledge response has been sent.
    await ctx.message.add_reaction("✅")











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


# Get the bot to leave this guild
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
