# some audio tools that I wrote up to help
# with repeated commands that are required to 
# participate in voice channels,

import re # regex

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