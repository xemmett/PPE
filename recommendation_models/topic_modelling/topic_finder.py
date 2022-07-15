import matplotlib.pyplot as plt
from pandas import read_csv, DataFrame

from gensim import corpora
from gensim.models import TfidfModel, LdaModel, LsiModel
from gensim.models.coherencemodel import CoherenceModel

import re

from keyword_deriver import KeywordClassifier
keyword_classifier = KeywordClassifier()

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from datetime import datetime

# for stemming approach
from nltk.stem.porter import PorterStemmer
from numpy.ma.core import power

p_stemmer = PorterStemmer()
# end

# for lemmatize approach

lemmatizer = WordNetLemmatizer()
# end

def open_data(filename=r"../../scrapers/qualifax_scraper/data/master_courses.csv"):
    print("opening data")
    documents = []
    titles = []

    dataset = read_csv(filename, encoding='utf8', low_memory=False)
    columns = ['course_name']
    df = DataFrame([], columns=columns)
    for c in columns:
        df[c] = dataset[c]

    df['fulldesc'] = ""
    for index, row in df.iterrows():
        fulldesc = ""

        for val in row.values[:1]:
            if(str(val) != 'nan' and val != None and val != 'null'):
                fulldesc += val.strip()+' '

        fulldesc = fulldesc.lower()
        punctuation_pattern = "[^A-Za-z0-9 ]"
        fulldesc = re.sub(punctuation_pattern, ' ', fulldesc) # remove punctuation
        fulldesc = fulldesc.strip()
        df['fulldesc'].iloc[index] = fulldesc

    cleaned_df = df[df['fulldesc'] != '']

    # titles = cleaned_df['course_name'].to_list()
    documents = cleaned_df['fulldesc'].to_list()

    return documents, 0, cleaned_df

def preprocess(documents=[], token_method='stem'):
    print("preprocessing data")
    # tokenizer = RegexpTokenizer(r'\w+')
    # print(documents)
    processed_docs = []

    if(token_method == 'stem'):
        def reduce(tokens): return [p_stemmer.stem(x) for x in tokens]
    elif(token_method == 'lemmatize'):
        def reduce(tokens): return [lemmatizer.lemmatize(x) for x in tokens]

    print("getting custom_stopwords")
    custom_stop_words = [] # keyword_classifier.get_stopwords(documents)
    stop_words = list(stopwords.words('english'))

    print("removing stopwords")
    for d in documents:
        go_tokens = [
            x for x in d.split(' ') if x not in stop_words and x not in custom_stop_words and len(x) > 5 or x == 'it']
        processed_d = reduce(go_tokens)
        # print('processed d: ', processed_d)
        processed_docs.append(processed_d)
    print('preprocessed')
    return processed_docs

def prepare_corpus(cleaned_docs=[]):
    """
    create term dictionary for our corpus and converting list of documents into document term matrix
    """
    print("preparing corpus")
    # assign each unique term an index
    dictionary = corpora.Dictionary(cleaned_docs)
    
    dictionary.filter_extremes(no_below=15, no_above=0.3, keep_n=100000)

    bow = [dictionary.doc2bow(doc) for doc in cleaned_docs]
    return dictionary, bow

docs, titles, _ = open_data(filename=r"../../scrapers/qualifax_scraper/data2020/results.csv")

if(__name__ == "__main__"): 
    cleaned_docs = preprocess(docs, 'lemmatize')
    dictionary, bow = prepare_corpus(cleaned_docs)

    tfidfmodel = TfidfModel(corpus=bow, dictionary=dictionary)
    corpus_tfidf  = tfidfmodel[bow]

lsi_tfidf = LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=20)

lsi_transformed_corpus = lsi_tfidf[corpus_tfidf]
for i, doc in lsi_tfidf.print_topics():
    print(i, doc)

lsi_tfidf = LsiModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=20)

lsi_transformed_corpus = lsi_tfidf[corpus_tfidf]
for i, doc in lsi_tfidf.print_topics(5):
    print(i, doc)