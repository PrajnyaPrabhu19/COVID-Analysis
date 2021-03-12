import praw
import pandas as pd
from praw.models import MoreComments

reddit = praw.Reddit(client_id='grAXAOXOnMJt9A', client_secret='A8I1AW0ysmsZrMSUmdqNCkc6jXZTNw', user_agent='ScrapeBot')
#read ids form csv
posts = pd.read_csv('/Users/prajnyaprabhu/PycharmProjects/MSProject/Reddit/COVID19.csv')
id_list = posts['id'].to_list()
comments=[]
for id in id_list:
    submission = reddit.submission(id=id)

    for comment in submission.comments.list():
        if isinstance(comment, MoreComments):
            continue
        #print(comment.body)
        comments.append([comment.body,id])

comments = pd.DataFrame(comments, columns=['comments','id'])
comments.to_csv('COVID19Comments.csv', index=False)
