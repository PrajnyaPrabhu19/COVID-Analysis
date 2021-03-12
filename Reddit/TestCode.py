import praw
import pandas as pd
from praw.models import MoreComments

reddit = praw.Reddit(client_id='grAXAOXOnMJt9A', client_secret='A8I1AW0ysmsZrMSUmdqNCkc6jXZTNw', user_agent='ScrapeBot')
comments=[]
submission = reddit.submission(id='kwi2rz')
for comment in submission.comments.list():
    if isinstance(comment, MoreComments):
        continue
    print(comment.body)