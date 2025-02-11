import os.path
from gensim import corpora
from gensim.models import LsiModel
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim.models.coherencemodel import CoherenceModel
import matplotlib.pyplot as plt
import pandas as pd

def load_data():
    tweets = pd.read_csv('/Users/prajnyaprabhu/PycharmProjects/MSProject/Covid-19/output10dec.csv',header = None)
    documents_list = []
    titles = []
    tweet_list = tweets[2].to_list()
    for tweet in tweet_list:
        text = tweet
        documents_list.append(text)
    titles.append(text[0:min(len(text), 100)])
    return documents_list, titles

def load_reddit_data():
    comments = pd.read_csv('/Users/prajnyaprabhu/PycharmProjects/MSProject/Reddit/CoronavirusComments.csv')
    documents_list = []
    titles = []
    comm_list = comments['comments'].to_list()
    for comm in comm_list:
        text = comm
        documents_list.append(text)
    titles.append(text[0:min(len(text), 100)])
    return documents_list, titles

#def load_data(path,file_name):
 #   documents_list = []
  #  titles = []
   # with open(os.path.join(path, file_name), "r") as fin:
    #    for line in fin.readlines():
     #       text = line.strip()
      #      documents_list.append(text)
  #  print("Total Number of Documents:", len(documents_list))
   # titles.append(text[0:min(len(text), 100)])
    #return documents_list, titles

def preprocess_data(doc_set):
    tokenizer = RegexpTokenizer(r'\w+')
    en_stop = set(stopwords.words('english'))
    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()
    texts = []
    for i in doc_set:
        raw = i.lower()
        tokens = tokenizer.tokenize(raw)
        stopped_tokens = [i for i in tokens if not i in en_stop]
        stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
        texts.append(stemmed_tokens)
    return texts

def prepare_corpus(doc_clean):
    dictionary = corpora.Dictionary(doc_clean)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    # generate LDA model
    return dictionary, doc_term_matrix

def create_gensim_lsa_model(doc_clean,number_of_topics,words):
    dictionary, doc_term_matrix = prepare_corpus(doc_clean)
    # generate LSA model
    lsamodel = LsiModel(doc_term_matrix, num_topics=number_of_topics, id2word=dictionary)  # train model
    print(lsamodel.print_topics(num_topics=number_of_topics, num_words=words))
    return lsamodel

def compute_coherence_values(dictionary, doc_term_matrix, doc_clean, stop, start=2, step=3):
    coherence_values = []
    model_list = []
    for num_topics in range(start, stop, step):
        # generate LSA model
        model = LsiModel(doc_term_matrix, num_topics=number_of_topics, id2word=dictionary)  # train model
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=doc_clean, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())
    return model_list, coherence_values

def plot_graph(doc_clean,start, stop, step):
    dictionary,doc_term_matrix=prepare_corpus(doc_clean)
    model_list, coherence_values = compute_coherence_values(dictionary, doc_term_matrix,doc_clean,
                                                            stop, start, step)
    # Show graph
    x = range(start, stop, step)
    plt.plot(x, coherence_values)
    plt.xlabel("Number of Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence_values"), loc='best')
    plt.show()



number_of_topics=9
words=10
#tweets
#document_list,titles=load_data()

#reddit
document_list,titles=load_reddit_data()

clean_text=preprocess_data(document_list)
start, stop, step = 2, 12, 1
#plot_graph(clean_text, start, stop, step)

model=create_gensim_lsa_model(clean_text,number_of_topics,words)
print(model.print_topics())