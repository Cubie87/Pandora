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
        # delete all text after the spacebar

    # Check for attack/illegal characters in link.
    if not re.search("^[a-zA-Z0-9_-]{11}$", link): # regex expression for a valid youtube video id.
        return True
    
    return False

    