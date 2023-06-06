import requests
import re

def retrieveTwitter(twitterAPIurl, twitterUser, twitterAPIkey, twitterAPIhost):
    querystring = {"username":twitterUser}
    headers = {
        "X-RapidAPI-Key": twitterAPIkey,
        "X-RapidAPI-Host": twitterAPIhost
    }
    response = requests.get(twitterAPIurl, headers=headers, params=querystring)

    information = response.json()

    return information['data']['user_result']['result']['timeline_response']['timeline']['instructions'][1]['entries']
