import praw
import pandas as pd
from praw.models import MoreComments


reddit = praw.Reddit(client_id='CLIENT_ID', client_secret='CLIENT_SECRET', user_agent='AGENT_NAME')

posts = []
subreddit = reddit.subreddit('COVID19')
for post in subreddit.hot(limit=5):
    posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
#print(posts)
posts.to_csv('COVID19.csv', index=False)

#covid19positive
#Coronavirus
#CoronavirusUS
#CoronavirusRecession
#COVID19
