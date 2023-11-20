from datetime import datetime
import discord
import os

# ics header
icsHeader = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:https://github.com/Cubie87/Pandora\n"

# cast time from discord to zulu
# zulu time is what's used by ics files
def castDiscordTimeToZulu(timeObject):
    timeString = str(timeObject)
    time = datetime.strptime(timeString, "%Y-%m-%d %H:%M:%S%z")
    return time.strftime('%Y%m%dT%H%M%SZ')


# make a VEvent based on discord event data
def makeVevent(event, icsFile):
    icsFile.write("BEGIN:VEVENT\n")
    icsFile.write("UID:" + str(datetime.now().timestamp()) + "\n")
    icsFile.write("DTSTAMP:" + datetime.now().strftime('%Y%m%dT%H%M%SZ') + "\n")
    icsFile.write("DTSTART:" + castDiscordTimeToZulu(event.start_time) + "\n")
    icsFile.write("DTEND:" + castDiscordTimeToZulu(event.end_time) + "\n")
    icsFile.write("SUMMARY:" + event.name + "\n")
    icsFile.write("LOCATION:" + event.location + "\n")
    descString = clean_text = event.description.replace("\n", "\\n")
    icsFile.write("DESCRIPTION:" + descString + "\n")
    icsFile.write("END:VEVENT\n")


# get all events, format them to ics format and send as file.
async def getEvents(ctx, icsFileName):
    # grab all events in server
    eventList = await ctx.guild.fetch_scheduled_events()
    # case if no events are present
    if len(eventList) == 0:
        await ctx.send(embed = discord.Embed(title = "No events found", color = 0x888888))
        return
    # opens an ics file for writing
    icsFile = open(icsFileName, "w")
    # writes header
    icsFile.write(icsHeader)
    # enumerates all events and writes properties to ics file
    for event in eventList:
        makeVevent(event, icsFile)
    # write footer and close file
    icsFile.write("END:VCALENDAR\n")
    icsFile.close()
    # load file and send
    file = discord.File(icsFileName)
    await ctx.send(file=file)
    # delete file
    os.remove(icsFileName)


