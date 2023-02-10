# a toolkit to grab CTFtime entries from the website 
# and post the event details into the discord server.

# note that this abides by their API guidelines, which is re-stated below.
# More information can be found at https://ctftime.org/api/

#API for simple data export. Data is in JSON format.
#This API is provided for data analysis and mobile applications only.
#You can not use this API to run CTFtime clones — most of the CTFtime data is moderated by humans, please, respect their time.



import json
import urllib.request
import re # regex
from datetime import datetime

# check if it's a 4 digit numerical code
def isCtfCodeValid(code):
    if not re.search("\d{1,4}", code):
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
    reply = "\nStart Time: " + str(eventJson['start']) + "\nEnd Time: " + str(eventJson['finish']) + "\nDuration: " + str(eventJson['duration']) + "\nCTF Time URL: " + str(eventJson['ctftime_url']) + "\nFormat: " + str(eventJson['format'])
    # send reply
    return str(eventJson['organizers'][0]['name']), reply