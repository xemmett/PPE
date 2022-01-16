# https://www.datacamp.com/community/tutorials/discovering-hidden-topics-python

import matplotlib.pyplot as plt
from pandas import read_csv, DataFrame

import string

from gensim import corpora
from gensim.models import LsiModel
from gensim.models.coherencemodel import CoherenceModel

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


# open data

def open_data(filename=r"..\..\scrapers\qualifax_scraper\data2020\results.csv"):
    documents = []
    titles = []

    dataset = read_csv(filename, encoding='utf8', low_memory=False)

    columns = ['careers_or_further_progression', 'course_name', 'course_content',
               'attendance_options', 'location_(districts)']
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
        fulldesc = fulldesc.strip()
        fulldesc = fulldesc.translate(
            fulldesc.maketrans("", "", string.punctuation))

        df['fulldesc'].iloc[index] = fulldesc

    cleaned_df = df[df['fulldesc'] != '']

    titles = cleaned_df['course_name'].to_list()
    documents = cleaned_df['fulldesc'].to_list()

    return documents, titles, cleaned_df


class LsaModel():

    def preprocess(self, documents=[], token_method='lemmatize'):
        """
        Tokenize, remove stopwords, stemming
        try: implement lemmatization instead of stemming?
        """
        tokenizer = RegexpTokenizer(r'\w+')

        en_stop = set(stopwords.words('english'))

        texts = []

        if(token_method == 'stem'):
            def tm(tokens): return [p_stemmer.stem(x) for x in tokens]
        elif(token_method == 'lemmatize'):
            def tm(tokens): return [lemmatizer.lemmatize(x) for x in tokens]

        for d in documents:
            raw = d.lower()
            tokens = tokenizer.tokenize(raw)
            stopped_tokens = [
                x for x in tokens if not x in en_stop and len(x) > 3]
            reduced_tokens = tm(stopped_tokens)
            texts.append(reduced_tokens)

        return texts

    def prepare_corpus(self, cleaned_doc=[]):
        """
        create term dictionary for our corpus and converting list of documents into document term matrix
        """
        # assign each unique term an index
        dictionary = corpora.Dictionary(cleaned_doc)

        dictionary.filter_n_most_frequent(14)
        self.dictionary = dictionary

        doc_term_matrix = [dictionary.doc2bow(doc) for doc in cleaned_doc]
        return dictionary, doc_term_matrix

    def create_gensim_lsa_model(self, cleaned_doc, number_of_topics, words, power_iters=4):
        dictionary, doc_term_matrix = self.prepare_corpus(cleaned_doc)

        # generate lsa model
        lsamodel = LsiModel(doc_term_matrix, num_topics=number_of_topics,
                            id2word=dictionary, power_iters=power_iters)
        # print("\t>>Topics\n", lsamodel.print_topics(
        #     num_topics=number_of_topics, num_words=words))

        return lsamodel

    def compute_coherence(self, dictionary, doc_term_matrix, cleaned_doc, start=2, stop=12, step=1):
        """ 
        compute coherence values for various number of topics
        """

        coherence_values = []
        model_list = []

        for i in range(start, stop, step):
            print(i)
            model = LsiModel(doc_term_matrix, num_topics=5,
                             id2word=dictionary, power_iters=i)
            model_list.append(model)
            coherencemodel = CoherenceModel(
                model=model, texts=cleaned_doc, dictionary=dictionary, coherence='c_v')
            coherence_values.append(coherencemodel.get_coherence())

        return model_list, coherence_values

    def plot_coherence(self, cleaned_doc, start=2, stop=12, step=1):
        dictionary, doc_term_matrix = self.prepare_corpus(cleaned_doc)
        model_list, coherence_values = self.compute_coherence(
            dictionary, doc_term_matrix, cleaned_doc, start, stop, step)

        x = range(start, stop, step)
        plt.plot(x, coherence_values)
        plt.xlabel("Power Iteration")
        plt.ylabel("Coherence Value")
        plt.legend(("coherence_values"), loc='best')
        plt.show()

    def __init__(self, token_method='lemmatize', number_of_topics=5, num_words=10, power_iters=4, document_stop_index=None) -> None:
        print("start")
        self.number_of_topics = number_of_topics
        self.num_words = num_words

        training_docs, self.titles, _ = open_data(
            filename=r"..\..\scrapers\qualifax_scraper\data2020\results.csv")
        print("cleaning text")
        self.training_docs = training_docs

        if(document_stop_index):
            training_docs = training_docs[:document_stop_index]

        self.documents = self.preprocess(training_docs, token_method)
        print("creating lsa model")
        self.model = self.create_gensim_lsa_model(
            self.documents, number_of_topics, num_words, power_iters=power_iters)


lm = LsaModel(document_stop_index=7500)

print(len(lm.training_docs))

topics = lm.model.print_topics(num_topics=5, num_words=10)
topic_indexes = [x[0] for x in topics]

_, _, df = open_data()

df['topic'] = ''
df['similarity'] = ''
for i, row in df:
    new_text_corpus = lm.dictionary.doc2bow(row.full_desc.split())
    # lm.model[new_text_corpus]

    for c in lm.model[new_text_corpus]:
        # [(Topics, Perc Contrib)]
        print("Document Topics      : ", c[0], c[1])
        # [(Word id, [Topics])]
        print("Word id, Topics      : ", topics[topic_indexes.index(c[0])])

        row['topic_{}'] = c[0]
        row['similarity'] = c[1]
