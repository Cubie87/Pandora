from datetime import datetime



def castDiscordTimeToZulu(timeObject):
    timeString = str(timeObject)
    time = datetime.strptime(timeString, "%Y-%m-%d %H:%M:%S%z")
    return time.strftime('%Y%m%dT%H:%M:%SZ')



def makeVevent(event, icalFile):
    icalFile.write("BEGIN:VEVENT\n")
    icalFile.write("DTSTART:" + castDiscordTimeToZulu(event.start_time) + "\n")
    icalFile.write("DTEND:" + castDiscordTimeToZulu(event.end_time) + "\n")
    icalFile.write("SUMMARY:" + event.name + "\n")
    icalFile.write("LOCATION:" + event.location + "\n")
    icalFile.write("DESCRIPTION:" + event.description + "\n")
    icalFile.write("END:VEVENT\n")



