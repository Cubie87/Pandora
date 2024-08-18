# some tools used to scrape twitter to keep up 
# to date with metro route changes and
# outages.
# notably this transport provider has an API/RSS 
# feed but does not update it as much as twitter
# uses third party twitter api.

import feedparser
import discord
from datetime import datetime

# grab tweets using scraper
def retrieveUserTweets(apiURL):
    # set browser agent
    feedparser.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    # grab RSS feed
    return feedparser.parse(apiURL)


async def metroTweets(ctx, apiURL):
    # get current time in unix epoch int
    rightNow = int(datetime.now().timestamp())
    # retrieve tweets
    userTweets = retrieveUserTweets(apiURL)
    # find useful tweets
    for tweet in userTweets['entries']:
        # get post timestamp as a unix epoch
        unixpost = int(datetime.strptime(str(tweet['published']), '%a, %d %b %Y %H:%M:%S %Z').timestamp())
        # break if not sent in the past 48 hours
        if unixpost < rightNow - 172800:
            break
        # otherwise retrieve text
        tweetText = tweet['title_detail']['value']
        # and send text in reply to the discord query.
        await ctx.send(embed = discord.Embed(title = "<t:" + str(unixpost) + ":F>", description = tweetText, color = 0xFFFFFF))
