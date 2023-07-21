import feedparser

def retrieveEvents(metroAPIurl):
    return feedparser.parse("https://www.adelaidemetro.com.au/announcements/rss")