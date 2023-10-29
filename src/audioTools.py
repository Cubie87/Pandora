# some audio tools that I wrote up to help
# with repeated commands that are required to 
# participate in voice channels,

import re # regex
import discord
import os # audio cached file management
import yt_dlp # audio file downloading



# yt-dlp options
ytdlOps = {
    'format': 'mp3/bestaudio/best',
    'outtmpl': 'media/%(id)s.%(ext)s',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }]
}



def preJoinCheck(ctx):
    if str(ctx.message.author.voice) == "None":
        # if the user is not in a voice channel?
        return 0
    # otherwise, return the voice channel
    return ctx.message.author.voice.channel


def getVoiceChannel(ctx, bot):
    if bot.voice_clients == []:
        return -1
    # get the right voice connection
    voiceChannel = bot.voice_clients[0]
    #print(bot.voice_clients)
    for connections in bot.voice_clients:
        if connections.guild == ctx.guild:
            voiceChannel = connections
            return voiceChannel
    return -1


def checkInvalidLink(link):
    # finds the second spacebar in message
    a = link.find(" ")
    if a != -1:
        link = link[:a]
        # delete all text after the second spacebar
    # Check for attack/illegal characters in link.
    if not re.search("^[a-zA-Z0-9_-]{11}$", link): # regex expression for a valid youtube video id.
        return True
    return False








async def joinVoice(ctx):
    # runs a pre-join check to see if the message is valid
    channel = preJoinCheck(ctx)
    # if the user is not in a channel, then channel = 0, and there will be an error message
    if channel == 0:
        await ctx.send(embed = discord.Embed(title = "Error!", description = "Please join a voice channel first!", color = 0x880000))
        return
    # otherwise, channel is the voice channel that the user is currently connected to.
    await channel.connect()
    await ctx.message.add_reaction("👍")
    return


async def leaveVoice(ctx):
    try: # try disconnect
        await ctx.voice_client.disconnect()
    except: # if we're not voice connected, let them know!
        await ctx.send(embed = discord.Embed(title = "Error!", description = "I'm not in a voice channel here!", color = 0x880000))
    else: #
        await ctx.message.add_reaction("👍")
    return


async def playMusic(ctx, link, mediaDir, client):
    # get the right voice connection
    voiceChannel = getVoiceChannel(ctx, client)
    print("Gonna try to play some music")
    print(client.voice_clients)

    # check for invalid input to prevent data injection
    if checkInvalidLink(link):
        await ctx.send(embed = discord.Embed(title = "Error!", description = "Please input a valid YouTube ID.\nEg: `=play dQw4w9WgXcQ`", color = 0x880000))
        return
    
    # if the bot isn't connected to a voice channel, then voiceChannel = -1
    if voiceChannel == -1:
        await ctx.send(embed = discord.Embed(title = "Error!", description = "Please connect the bot to a voice channel. `=join`", color = 0x880000))
        return

    # if the file does exist, play!
    if os.path.isfile(mediaDir + link + ".mp3"):
        try:
            voiceChannel.play(discord.FFmpegPCMAudio(mediaDir + link + ".mp3"))
        except:
            await ctx.send(embed = discord.Embed(title = "Error!", description = "Please join a voice channel to play music.", color = 0x880000))
        return
    
    # show typing while we download the file so the user knows something is happenning.
    async with ctx.typing():
        # the file doesn't exist! Need to download it.
        with yt_dlp.YoutubeDL(ytdlOps) as ydl:
            error_code = ydl.download([link])

    # play the audio
    voiceChannel.play(discord.FFmpegPCMAudio(mediaDir + link + ".mp3"))
    await ctx.message.add_reaction("➡")

# there's opportunity to merge a lot of the below with playMusic().
async def grabMusic(ctx, link, mediaDir, client):
    # check for invalid links    
    if checkInvalidLink(link):
        await ctx.send(embed = discord.Embed(title = "Error!", description = "Please input a valid YouTube ID.\nEg: `=play dQw4w9WgXcQ`", color = 0x880000))
        return
    
    # if the file does exist, send!
    if os.path.isfile(mediaDir + link + ".mp3"):
        try:
            await ctx.send(file=discord.File(mediaDir + link + ".mp3"))
        except:
            await ctx.send(embed = discord.Embed(title = "Error!", description = "File is too large.", color = 0x880000))
        return

    # the file doesn't exist! Need to download it.
    async with ctx.typing():
        with yt_dlp.YoutubeDL(ytdlOps) as ydl:
            error_code = ydl.download([link])

    # try send the file. If there's an error, it's probably too big
    try:
        await ctx.send(file=discord.File(mediaDir + link + ".mp3"))
    except:
        await ctx.send(embed = discord.Embed(title = "Error!", description = "File is too large.", color = 0x880000))
