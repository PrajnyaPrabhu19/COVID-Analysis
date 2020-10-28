import csv
import os
import tweepy as tw
import pandas as pd
from datetime import datetime,timedelta

consumer_key= 'tRlXdz2ZfEWOqJM59oAnONh9k'
consumer_secret= 'bVzVBtAWOcxzsBiZF34fxgtCzaTRzySOVujZkNhTt0R9GW3GW2'
access_token= '4751759016-SMsAKHL4VXgFc4qd7C5ZpZubUoJbGYnDHyA5WLf'
access_token_secret= 'GAu5rsdmQO8DKR5WGHb6vEyzBU3kOj7WM3uzaLbvpwgBJ'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

search_words = "#coronavirus"
new_search = search_words + " -filter:retweets"


date_since = "2020-10-01"

#tweets = tw.Cursor(api.search,
 #             q=new_search,
  #            lang="en",
   #           include_entities=True,
    #          since=date_since).items(1)

#users_locs = [[tweet.user.screen_name, tweet.user.location, tweet.text] for tweet in tweets]
#print(users_locs)

#tweet_text = pd.DataFrame(data=users_locs,
 #                   columns=['user', "location", "text"])
#print(tweet_text)


csvFile = open('output4oct.csv', 'a')
csvWriter = csv.writer(csvFile)

for status in tw.Cursor(api.search,
                       q=new_search,
                       since='2020-10-04', until='2020-10-05',
                       count=10,
                       result_type='recent',
                       include_entities=True,
                       monitor_rate_limit=True,
                       wait_on_rate_limit=True,
                       lang="en").items():

    eastern_time = status.created_at - timedelta(5)
    edt_time = eastern_time.strftime('%Y-%m-%d %H:%M')
    #print(status.created_at)

    csvWriter.writerow([status.created_at, status.user.screen_name.encode('utf8'), status.text.encode('utf-8')])

csvFile.close()