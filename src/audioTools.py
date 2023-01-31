# some audio tools that I wrote up to help
# with repeated commands that are required to 
# participate in voice channels,


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