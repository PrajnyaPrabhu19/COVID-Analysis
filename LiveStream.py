import json
import sys

import TwitterConfig as config
from datetime import datetime
import tweepy
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

CONSUMER_KEY = config.twitter['conKey']
CONSUMER_SECRET = config.twitter['conSecret']
ACCESS_TOKEN = config.twitter['accessToken']
ACCESS_SECRET = config.twitter['accessSecret']

class StreamListener(tweepy.StreamListener):
    def on_data(self, data):
        try:
            with open('LiveStream13jan.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

if __name__ == "__main__":
    # complete authorization and initialize API endpoint
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # initialize stream
    streamListener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=streamListener,tweet_mode='extended')
    tags = ['coronavirus','covid19','Covid-19','CoronavirusCrisis','CoronavirusOutbreak']
    stream.filter(track=tags)