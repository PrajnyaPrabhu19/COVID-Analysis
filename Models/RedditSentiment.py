import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import spacy
import re

import nltk
#nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import gensim
from gensim.utils import simple_preprocess
from collections import Counter
from wordcloud import WordCloud

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

csv_file_list = ["/Users/prajnyaprabhu/PycharmProjects/MSProject/Reddit/CoronavirusComments.csv", "/Users/prajnyaprabhu/PycharmProjects/MSProject/Reddit/CoronavirusRecessionComments.csv","/Users/prajnyaprabhu/PycharmProjects/MSProject/Reddit/CoronavirusUSComments.csv","/Users/prajnyaprabhu/PycharmProjects/MSProject/Reddit/COVID19Comments.csv","/Users/prajnyaprabhu/PycharmProjects/MSProject/Reddit/RedditComments.csv"]

list_of_dataframes = []
for filename in csv_file_list:
    list_of_dataframes.append(pd.read_csv(filename))

df = pd.concat(list_of_dataframes)

def tokenize(comment):
    for word in comment:
        yield(gensim.utils.simple_preprocess(str(word), deacc=True))  # deacc=True Removes punctuations

df['tidy_tokens'] = list(tokenize(df['comments']))



stop_words = stopwords.words('english')
def remove_stopwords(tidy_tokens):
    return [[word for word in simple_preprocess(str(comment)) if word not in stop_words] for comment in tidy_tokens]

df['tokens_no_stop'] = remove_stopwords(df['tidy_tokens'])

#print(df.head())

df = df.drop(['tidy_tokens'], axis=1)

def remove_links(tweet):
    tweet_no_link = re.sub(r"http\S+", "", tweet)
    return tweet_no_link

df['tweet_text_p'] = np.vectorize(remove_links)(df['comments'])

vader_analyzer = SentimentIntensityAnalyzer()

negative = []
neutral = []
positive = []
compound = []

def sentiment_scores(df, negative, neutral, positive, compound):
    for i in df['tweet_text_p']:
        sentiment_dict = vader_analyzer.polarity_scores(i)
        negative.append(sentiment_dict['neg'])
        neutral.append(sentiment_dict['neu'])
        positive.append(sentiment_dict['pos'])
        compound.append(sentiment_dict['compound'])

# Function calling
sentiment_scores(df, negative, neutral, positive, compound)

# Prepare columns to add the scores later
df["negative"] = negative
df["neutral"] = neutral
df["positive"] = positive
df["compound"] = compound

# Fill the overall sentiment with encoding:
# (-1)Negative, (0)Neutral, (1)Positive
sentiment = []
for i in df['compound']:
    if i >= 0.05:
        sentiment.append(1)

    elif i <= - 0.05:
        sentiment.append(-1)

    else:
        sentiment.append(0)
df['sentiment'] = sentiment

neg_tweets = df.sentiment.value_counts()[-1]
neu_tweets = df.sentiment.value_counts()[0]
pos_tweets = df.sentiment.value_counts()[1]

# Draw Plot
fig, ax = plt.subplots(figsize=(10, 6), subplot_kw=dict(aspect="equal"), dpi= 80)

data = [df.sentiment.value_counts()[-1], df.sentiment.value_counts()[0], df.sentiment.value_counts()[1]]
categories = ['Negative', 'Neutral', 'Positive']
explode = [0.05,0.05,0.05]

def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}% ({:d} )".format(pct, absolute)

wedges, texts, autotexts = ax.pie(data,
                                  autopct=lambda pct: func(pct, data),
                                  textprops=dict(color="w"),
                                  colors=['#e55039', '#3c6382', '#78e08f'],
                                  startangle=140,
                                  explode=explode)

# Decoration
ax.legend(wedges, categories, title="Sentiment", loc="center left", bbox_to_anchor=(1, 0.2, 0.5, 1))
plt.setp(autotexts, size=10, weight=700)
ax.set_title("Number of Comments by Sentiment", fontsize=12, fontweight="bold")
plt.show()

labels = ['Negative', 'Neutral', 'Positive']
freq = [df.sentiment.value_counts()[-1], df.sentiment.value_counts()[0], df.sentiment.value_counts()[1]]
index = np.arange(len(freq))

plt.figure(figsize=(8,6))
plt.bar(index, freq, alpha=0.8, color= 'black')
plt.xlabel('Sentiment', fontsize=13)
plt.ylabel('Number of Comments', fontsize=13)
plt.xticks(index, labels, fontsize=11, fontweight="bold")
plt.title('Number of Comments per Sentiment', fontsize=12, fontweight="bold")
plt.ylim(0, len(df['comments']))
plt.show()

# We remove the neutral compound scores to compare the negative and positive tweets
data = df[(df["sentiment"]!=0)]

# Draw Plot
plt.figure(figsize=(8,6), dpi= 80)
sns.kdeplot(data["compound"], shade=True, color="#3c6382", label="Overall Compound Score", alpha=.7)

# Decoration
plt.title('Density Plot of Overall Compound Score', fontsize=11, fontweight='bold')
plt.axvline(x=0, color='#e55039')
plt.legend()
plt.show()


def lemmatization(tweets, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    tweets_out = []
    for sent in tweets:
        doc = nlp(" ".join(sent))
        tweets_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return tweets_out
# Initialize spacy 'en' model, keeping only tagger component (for efficiency)
# python3 -m spacy download en
nlp = spacy.load('en', disable=['parser', 'ner'])
# Do lemmatization keeping only noun, adj, vb, adv
df['lemmatized'] = lemmatization(df['tokens_no_stop'], allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
df.drop(['tokens_no_stop'], axis=1, inplace=True)
df_pos = df[df['sentiment']==1]
df_neg = df[df['sentiment']==(-1)]
print(df_pos.head())

###
#Wordcloud
# Join the tweet back together
def rejoin_words(row):
    words = row['lemmatized']
    joined_words = (" ".join(words))
    return joined_words

all_words_pos = ' '.join([text for text in df_pos.apply(rejoin_words, axis=1)])
all_words_neg = ' '.join([text for text in df_neg.apply(rejoin_words, axis=1)])
wordcloud = WordCloud(width=900, height=600, random_state=21, max_font_size=110, background_color='white',
                      max_words=200,colormap='summer').generate(all_words_pos)

plt.figure(figsize=(12, 8))
plt.title('WordCloud of Positive Comments', fontsize=14, fontweight="bold")
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()

wordcloud = WordCloud(width=900, height=600, random_state=21, max_font_size=110, background_color='ghostwhite',
                      max_words=200,colormap='autumn').generate(all_words_neg)

plt.figure(figsize=(12, 8))
plt.title('WordCloud of Negative Comments', fontsize=14, fontweight="bold")
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()

# 10 Most positive Tweets
df_pos.sort_values('compound', inplace=True, ascending=False)
df_pos.reset_index(drop=True, inplace=True)
print(df_pos.head(10))

# 10 Most Negative Tweets
df_neg.sort_values('compound', inplace=True)
print(df_neg.reset_index(drop=True).head(10))

df.drop(['tweet_text_p', 'lemmatized'], axis=1, inplace=True)
print(df.head())
df.to_pickle('/Users/prajnyaprabhu/PycharmProjects/MSProject/Models/Sentiments/REDDITSentiments.pkl')