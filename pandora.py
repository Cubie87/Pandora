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

# other libraries
import re # regex

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
bot = commands.Bot(
    command_prefix = botVars.prefix,
    help_command = None, # to disable default help command
    strip_after_prefix = True,
    owner_id = botVars.owner,
    intents = intents
    )




# startup message in console.
@bot.event
async def on_ready(): # do this on startup
    # announces when the bot is up and running
    print(f"{bot.user} is now online and is connected to " + str(len(bot.guilds)) + " servers: ")
    # list servers by server name where Pandora exists in on bootup.
    # this is done to prevent unauthorised distribution of the bot into unknown servers.
    async for guild in bot.fetch_guilds(limit=250):
        print(" - " + guild.name + " - " + str(guild.id) + "\n")




# ping the bot! The most basic command.
@bot.command()
async def ping(ctx):
    print(ctx.message.author.name + "#" + ctx.message.author.discriminator + " pinged the bot.")
    await ctx.send(embed = discord.Embed(title = "Pong!", color = 0x0078ff))

# help command
@bot.command()
async def help(ctx):
    await ctx.send(embed = discord.Embed(title = "Pandora's commands", description = "This is the help command!", color = 0x0078ff))

# roll some dice!
@bot.command(aliases=['r'])
async def roll(ctx, *, diceString):
    print(ctx.message.author.name + "#" + ctx.message.author.discriminator + " Rolled some dice.")
    reply = diceRoller.roll(diceString)
    await ctx.send(embed = reply)




#
## Audio Tools! (and music playing :D)
#



# join a voice channel
@bot.command()
async def join(ctx):
    # runs a pre-join check to see if the message is valid
    channel = audioTools.preJoinCheck(ctx)
    # if the user is not in a channel, then channel = 0, and there will be an error message
    if channel == 0:
        await ctx.send(embed = discord.Embed(title = "Error!", description = "Please join a voice channel first!", color = 0x880000))
        return
    # otherwise, channel is the voice channel that the user is currently connected to.
    await channel.connect()
    await ctx.send(embed = discord.Embed(title = "Joining...", color = 0x888888))
    print("Joining a voice channel!")


# disconnect from voice in relevant server
@bot.command(aliases=['leave', 'exit', 'quit'])
async def dc(ctx):
    await ctx.voice_client.disconnect()
    ctx.voice_client.cleanup()
    print("Leaving a voice channel!")
    await ctx.send(embed = discord.Embed(title = "Leaving...", color = 0x888888))
    #print("No channel to disconnect!")
    #await ctx.send(embed = discord.Embed(title = "Error!", description = "I'm not in a voice channel here!", color = 0x880000))



# play some audio
@bot.command(aliases=['play'])
async def p(ctx, *, link):
    # ctx.voice_client
    print("Gonna try to play some music")
    print(bot.voice_clients)
    # finds the second spacebar in message
    a = link.find(" ")
    if a != -1:
        link = link[:a]
        # delete all text after the spacebar

    # Check for attack/illegal characters in link.
    if re.search("[^a-zA-Z1-9_-]", link) != None or len(link) != 11:
        await ctx.send(embed = discord.Embed(title = "Error!", description = "Please input a valid YouTube ID.\nEg: `=play dQw4w9WgXcQ`", color = 0x880000))
        return
    
    # get the right voice connection
    voiceChannel = audioTools.getVoiceChannel(ctx, bot)

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
    
    # the file doesn't exist! Need to download it.
    os.system("yt-dlp -x --audio-format mp3 --audio-quality 0  -o '" + media + link + ".%(ext)s' " + "https://www.youtube.com/watch?v=" + link)

    voiceChannel.play(discord.FFmpegPCMAudio(media + link + ".mp3"))


# audio controls


@bot.command()
async def pause(ctx):
    # get voice channel
    voiceChannel = audioTools.getVoiceChannel(ctx, bot)
    # if the bot isn't connected to a voice channel, then voiceChannel = -1
    if voiceChannel == -1:
        await ctx.send(embed = discord.Embed(title = "Error!", description = "Not in a voice channel", color = 0x880000))
        return
    voiceChannel.pause()
    await ctx.message.add_reaction("👍")
    print("Pausing")
    
@bot.command()
async def resume(ctx):
    # get voice channel
    voiceChannel = audioTools.getVoiceChannel(ctx, bot)
    # if the bot isn't connected to a voice channel, then voiceChannel = -1
    if voiceChannel == -1:
        await ctx.send(embed = discord.Embed(title = "Error!", description = "Not in a voice channel", color = 0x880000))
        return
    voiceChannel.resume()
    await ctx.message.add_reaction("👍")
    print("Resuming Playback")
    
@bot.command()
async def stop(ctx):
    # get voice channel
    voiceChannel = audioTools.getVoiceChannel(ctx, bot)
    # if the bot isn't connected to a voice channel, then voiceChannel = -1
    if voiceChannel == -1:
        await ctx.send(embed = discord.Embed(title = "Error!", description = "Not in a voice channel", color = 0x880000))
        return
    voiceChannel.stop()
    await ctx.message.add_reaction("👍")
    print("Stopping Playback")







#"""
# furry reactions
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # the furry reacts
    if message.content.lower().startswith(("uwu","owo")):
        await message.channel.send(furryReply)
    elif message.content.startswith(":3"):
        # Black Hanekawa Cat Gif
        await message.channel.send(file = discord.File(media + "teehee0.gif"))

    await bot.process_commands(message)









# chatbot functionality written by chatGPT
@bot.command() # hide it from help command returns.
async def chat(ctx, *, prompt):
    #print(prompt) # verify the prompt has preamble removed.

    response = "I'm sorry, I am unable to access OpenAI's API at the moment. Please try again later."

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
    )
    response_text = response["choices"][0]["text"]
    
    file = open("gptlog.log", 'a')
    file.write("Q: " + prompt + "\n")
    file.write("A: " + response_text + "\n\n\n\n\n")
    file.close()

    # Send the generated response back to the channel
    await ctx.send(response_text)











#
#
# Everything below is administration commands for the bot, for the owner.
#
#




# list all the guilds that the bot is part of
@bot.command(hidden = True) # hide it from help command returns.
@commands.is_owner()
async def list(ctx):
    reply = "This bot is connected to " + str(len(bot.guilds)) + " servers: \n"
    # list servers by server name where the bot exists in.
    async for guild in bot.fetch_guilds(limit=250):
        #print(guild.name)
        reply = reply + " - " + guild.name + " - " + str(guild.id) + "\n"
    await ctx.send(reply)


# Get the bot to leave this guild
@bot.command(hidden = True)
@commands.is_owner()
async def bail(ctx, *, ID):
    guild = bot.get_guild(int(ID))
    try: 
        print("Bailing from " + guild.name)
        await guild.leave()
        await ctx.send("Successfully left " + guild.name)
    except:
        print("Guild does not exist! ID: " + guild.name)
        await ctx.send("I'm not part of this guild! Check the ID please.")

        
# shut down the bot
@bot.command(hidden = True)
@commands.is_owner()
async def sleep(ctx):
    print("Going to sleep....")
    # disconnect from all voice channels.
    for connections in bot.voice_clients:
        await connections.disconnect()
        connections.cleanup()
    # send ack
    await ctx.send(embed = discord.Embed(title = "Going to sleep...", color = 0x222222))
    # change status to offline
    await bot.change_presence(status=discord.Status.offline)
    # close off the bot
    await bot.close()


bot.run(discordToken)
