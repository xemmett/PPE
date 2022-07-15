"""
author: emmett lawlor
purpose: to examine similarities between strings
date: 2 mar 22
"""

from statistics import median, mean
import re

from nltk import pos_tag

corpus = [
    'Bachelor of Arts in Applied Languages',
    'Bachelor of Arts in Contemporary Dance',
    'Bachelor of Arts in Criminal Justice',
    'Bachelor of Arts in European Studies',
    'Bachelor of Arts in International Business',
    'Bachelor of Arts in International Insurance and European Studies',
    'Bachelor of Arts in Irish Dance',
    'Bachelor of Arts in Irish Music',
    'Bachelor of Arts in Journalism and New Media',
    'Bachelor of Arts in Law and Accounting',
    'Bachelor of Arts in Psychology and Sociology',
    'Bachelor of Arts in Voice',
    'Bachelor of Arts in World Music',
    'Bachelor of Business Studies',
    'Bachelor of Business Studies with French',
    'Bachelor of Business Studies with German',
    'Bachelor of Business Studies with Japanese',
    'Bachelor of Engineering in Aeronautical Engineering',
    'Bachelor of Engineering in Biomedical Engineering',
    'Bachelor of Engineering in Chemical and Biochemical Engineering',
    'Bachelors of Engineering in Computer and Electronic Engineering'
    ]

class KeywordClassifier():

    def __init__(self, corpus = [], verbose: bool = 0):

        self.verbose = verbose
        # self.tf_full = self.term_frequency(corpus)
        # self.stop_words = self.get_stopwords(self.tf_full)
        # self.tf_no_stopwords = self.term_frequency(corpus, stop_words=self.stop_words)
        # self.upper_boundary, self.lower_boundary = self.calculate_boundaries(tf.values())

    def same_types(self, *items) -> bool:
        return bool([1 for item in items if type(item).__name__ == type(items[0]).__name__])

    def term_frequency(self, corpus: str | list, stop_words: list = []) -> list:
        result = {}
        
        if(type(corpus).__name__ == 'list'): 
            corpus = ' '.join(corpus)

        corpus = corpus.lower()

        punctuation_pattern = "[^A-Za-z0-9' ]"
        corpus = re.sub(punctuation_pattern, ' ', corpus) # remove punctuation

        for word in list(set(corpus.split(' '))):
            print(word)
            if(word not in result.keys() and word not in stop_words):
                search_pattern = r"\b{word}\b".format(word=word)
                result[word] = len(re.findall(search_pattern, corpus))

        # sanity check of maths
        # print(len(corpus.split()))
        # print(len(re.findall(r"\bbachelor\b", corpus))/len(corpus.split()))

        if(self.verbose):
            indexable_list = list(result.values())
            indexable_list.sort()
            avg = mean(result.values())
            med = median(result.values())

            print(f"""
                median: {med}
                average: {avg}
                """)
            
            # plt.plot([result.values(), average, median])
            # plt.show()

        return result

    def tf_bubble(self, tf_dict: dict | str | list, center: float | int, distance: float | int) -> dict:
        """
        low level clustering, bubbles instead of clusters.
        return a group of items according to a term frequency dict, returning 
        the modules of said center and any of said distance
        we will normalize the frequencies to have the center as it's apex of the graph, then use the distance to find logarithmically similar in frequency words
        """
        try:
            tf_dict = self.term_frequency(tf_dict)
        except TypeError as e:
            pass
        
        indexes = []
        if(self.same_types(center, distance) == self.same_types(distance, 0.0) and distance <= 1.0):
            for key, value in tf_dict.items():
                frequency_distance = float(value)/sum(tf_dict.values())
                print(key, ": \t", frequency_distance*100) # stopping here, data set is too saturated with stop words, will work on this tomorrow
                if(frequency_distance <= center+distance and frequency_distance >= center-distance):
                    # print(key, frequency_distance)
                    pass

    def calculate_boundaries(self, freqs: list):
        freqs.sort()

        quartiler = lambda perc: (int(perc*len(freqs)) + 1) if perc*len(freqs) % 1 != 0 else (perc*len(freqs))

        q1 = freqs[quartiler(0.25)]
        q3 = freqs[quartiler(0.75)]
        iqr = q3-q1
        upper_boundary = abs(q3+1.5*iqr)
        lower_boundary = abs(q1-1.5*iqr)

        if(self.verbose):
            print(f"""q1 = {q1}, 
            q3 = {q3}, 
            iqr = {iqr},
            upper_boundary = {upper_boundary}, 
            lower_boundary = {lower_boundary}""")
        
        return lower_boundary, upper_boundary


    def get_stopwords(self, corpus: dict | str | list) -> set:
        
        tagged_corpora = pos_tag(corpus)
        print(tagged_corpora)
        keep = ['NN', 'NNS', 'JJ', 'VB'] # <- ['Nouns', 'Plural Nouns', 'Adjectives']

        stop_words = [x[0] for x in tagged_corpora if x[1] not in keep]

        return stop_words

for c in corpus:
    KeywordClassifier().get_stopwords(c.split(" "))

# # using full corpus, no stop words removed
# tf = term_frequency(corpus, verbose=1)
# data = []
# for key, value in tf.items():
#     data.append({
#         'word': key,
#         'count': value
#     })

# with open('qualifax_tf.json', 'w+') as f:
#     dump(data, f)

# stop_words = get_stopwords(corpus, 1)
# location_tf = term_frequency(list(set([x['location_(districts)'] for x in dataset])))
# data = []
# for key, value in location_tf.items():
#     data.append({
#         'word': key,
#         'count': value
#     })
    
# with open('qualifax_location_tf.json', 'w+') as f:
#     dump(data, f)
# stop_words += list(location_tf.keys())

# tf = term_frequency(corpus, stop_words=stop_words, verbose=1)

# print(calculate_boundaries(tf.values(), 1)) # just printing quartiles

# data = []
# for key, value in tf.items():
#     data.append({
#         'word': key,
#         'count': value
#     })

# with open('qualifax_nostopwords_tf.json', 'w+') as f:
#     dump(data, f)

# # happy with results