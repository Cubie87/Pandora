# a custom toolkit to grab CTFtime entries from the website 
# and post the event details into the discord server.

# note that this abides by their API guidelines, which is re-stated below.

#API for simple data export. Data is in JSON format.
#This API is provided for data analysis and mobile applications only.
#You can not use this API to run CTFtime clones — most of the CTFtime data
#is moderated by humans, please, respect their time.

# More information can be found at https://ctftime.org/api/


import json
import urllib.request
import feedparser
import re # regex
import discord
from datetime import datetime


# build the reply card from json format.
def buildReplyJson(eventJson):
    # convert the timestamps provided into Unix epoch for discord formatting.
    unixStart = datetime.strptime(str(eventJson['start']), '%Y-%m-%dT%H:%M:%S%z').timestamp()
    unixEnd = datetime.strptime(str(eventJson['finish']), '%Y-%m-%dT%H:%M:%S%z').timestamp()

    # note the disccord formatting used for the timestamps.
    # the split function it to remove all trailing decimals
    reply = "Organised by: **" + str(eventJson['organizers'][0]['name']) + "**\nOfficial URL: " + str(eventJson['url']) + "\nStart Time: <t:" + str(unixStart).split('.')[0] + ":F>\nEnd Time: <t:" + str(unixEnd).split('.')[0] + ":F>\nDuration: " + str(eventJson['duration']['days']) + " Days, " + str(eventJson['duration']['hours']) + " Hours" + "\nCTF Time URL: " + str(eventJson['ctftime_url']) + "\nFormat: " + str(eventJson['format']) + "\nWeight: " + str(eventJson['weight'])
    return reply


# build the reply card from RSS format.
def buildReplyRSS(rssFeed):
    # convert the timestamps provided into Unix epoch for discord formatting.
    unixStart = datetime.strptime(str(rssFeed['start_date']) + "+0000", '%Y%m%dT%H%M%S%z').timestamp() #20230114T000000
    unixEnd = datetime.strptime(str(rssFeed['finish_date']) + "+0000", '%Y%m%dT%H%M%S%z').timestamp()
    # convert organisers to json (cause otherwise it's just a string and sucks to format)
    organisers = json.loads(rssFeed['organizers'])
    
    # the split function it to remove all trailing decimals
    # note the disccord formatting used for the timestamps.
    # note that duration doesn't exist in the rss feed
    reply = "Organised by: **" + str(organisers[0]['name']) + "**\nOfficial URL: " + str(rssFeed['href']) + "\nStart Time: <t:" + str(unixStart).split('.')[0] + ":F>\nEnd Time: <t:" + str(unixEnd).split('.')[0] + ":F>\nCTF Time URL: " + str(rssFeed['link']) + "\nFormat: " + str(rssFeed['format_text']) + "\nWeight: " + str(rssFeed['weight'])
    return rssFeed['title'], reply


# check if it's a 4 digit numerical code
def isCtfCodeValid(code):
    if not re.search("\\d{1,4}", code):
        return False
    return True


# grab the event, convert from text to json, and return with the key details.
def grabCtfDetails(code):
    # define browser agent
    headers = {'User-Agent':"Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
    # format URL
    url = "https://ctftime.org/api/v1/events/" + str(code) + "/"
    # build request
    req = urllib.request.Request(url, headers=headers)
    # try request
    try:
        resp = urllib.request.urlopen(req)
    except: # if error, return error condition
        return False, False
    # cast to json
    eventJson = json.loads(resp.read())
    # built reply
    reply = buildReplyJson(eventJson)
    # send reply
    return str(eventJson['title']), reply


# grab all current ongoing CTFs
def currentCTFs():
    # grab RSS feed
    return feedparser.parse("https://ctftime.org/event/list/running/rss/")


# grab all upcoming CTFs
def upcomingCTFs():
    # grab RSS feed
    return feedparser.parse("https://ctftime.org/event/list/upcoming/rss/")





async def getCtfTime(ctx, code):
    if not isCtfCodeValid(code):
        await ctx.send(embed = discord.Embed(title = "Error!", description = "Please input a valid CTFTime ID.\nEg: `=ctftime 1000`", color = 0x880000))
        return

    # grab the event details
    title, reply = grabCtfDetails(code)
    # errors if the event ID doesn't correspond with an actual ctftime event
    if not title:
        await ctx.send(embed = discord.Embed(title = "Error!", description = "Please input a valid CTFTime ID.\nEg: `=ctftime 1000`", color = 0x880000))
        return
    await ctx.send(embed = discord.Embed(title = title, description = reply, color = 0xFFFFFF))


async def getCtfNow(ctx):
    # grab from RSS feed
    rssFeed = currentCTFs()
    for entry in rssFeed['entries']:
        title, reply = buildReplyRSS(entry)
        await ctx.send(embed = discord.Embed(title = title, description = reply, color = 0xFFFFFF))


async def getCtfSoon(ctx):
    # grab from RSS feed
    num = 6 # default number to retrieve
    # retrieve and print
    rssFeed = upcomingCTFs()
    # prevent retrieving too many
    if num > len(rssFeed['entries']):
        num = len(rssFeed['entries'])
    # send all the ones retrieved
    for entry in rssFeed['entries'][slice(0,num)]:
        title, reply = buildReplyRSS(entry)
        await ctx.send(embed = discord.Embed(title = title, description = reply, color = 0xFFFFFF))