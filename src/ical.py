from datetime import datetime



def castDiscordTimeToZulu(timeObject):
    timeString = str(timeObject)
    time = datetime.strptime(timeString, "%Y-%m-%d %H:%M:%S%z")
    print(time)
    return time.strftime('%Y%m%dT%H%M%SZ')



def makeVevent(event, icsFile):
    icsFile.write("BEGIN:VEVENT\n")
    icsFile.write("UID:" + str(datetime.now().timestamp()) + "\n")
    icsFile.write("DTSTAMP:" + datetime.now().strftime('%Y%m%dT%H%M%SZ') + "\n")
    icsFile.write("DTSTART:" + castDiscordTimeToZulu(event.start_time) + "\n")
    icsFile.write("DTEND:" + castDiscordTimeToZulu(event.end_time) + "\n")
    icsFile.write("SUMMARY:" + event.name + "\n")
    icsFile.write("LOCATION:" + event.location + "\n")
    icsFile.write("DESCRIPTION:" + event.description + "\n")
    icsFile.write("END:VEVENT\n")




