import re
import numpy as np
import pandas as pd
from pprint import pprint
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import spacy
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use','http','www','comment','post','like','https'])

#comments = pd.read_csv('/Users/prajnyaprabhu/PycharmProjects/MSProject/Reddit/CoronavirusRecession.csv')
#data = comments['body'].to_list()

tweets = pd.read_csv('/Users/prajnyaprabhu/PycharmProjects/MSProject/Covid-19/output19Jul1.csv', header=None)
data = tweets[2].to_list()
data = [re.sub('\S*@\S*\s?', '', sent) for sent in data]
data = [re.sub('\s+', ' ', sent) for sent in data]
data = [re.sub("\'", "", sent) for sent in data]

#print(data_words[:4]) #it will print the data after prepared for stopwords
bigram = gensim.models.Phrases(data, min_count=5, threshold=100)
trigram = gensim.models.Phrases(bigram[data], threshold=100)
bigram_mod = gensim.models.phrases.Phraser(bigram)
trigram_mod = gensim.models.phrases.Phraser(trigram)

def remove_stopwords(texts):
   return [[word for word in simple_preprocess(str(doc))
   if word not in stop_words] for doc in texts]

def make_bigrams(texts):
   return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts):
   return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

data_words_nostops = remove_stopwords(data)
data_words_bigrams = make_bigrams(data_words_nostops)
nlp1 = spacy.load("en_core_web_md")
nlp = spacy.load('en_core_web_md', disable=['parser', 'ner'])
data_lemmatized = lemmatization(
   data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']
)
#print(data_lemmatized[:4]) #it will print the lemmatized data.
id2word = corpora.Dictionary(data_lemmatized)
texts = data_lemmatized
corpus = [id2word.doc2bow(text) for text in texts]
#print(corpus[:4]) #it will print the corpus we created above.
[[(id2word[id], freq) for id, freq in cp] for cp in corpus[:4]]
#it will print the words with their frequencies.

lsi_model = gensim.models.lsimodel.LsiModel(
   corpus=, id2word=id2word, num_topics=20,chunksize=100
)

#pprint(lsi_model.print_topics())
doc_lsi = lsi_model[corpus]

file1 = open("/Users/prajnyaprabhu/PycharmProjects/MSProject/Models/Tweets/listtest.txt","w")
for t in lsi_model.print_topics():
  file1.write(' '.join(str(s) for s in t) + '\n')

file1.close()