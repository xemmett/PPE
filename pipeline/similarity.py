"""
author: emmett lawlor
purpose: to examine similarities between strings
date: 2 mar 22
"""

from statistics import median, mean
import matplotlib.pyplot as plt
import re

from nltk import pos_tag
from json import load, dump

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
    'Bachelor of Engineering in Civil Engineering',
    'Architecture - Bolton Street'
    ]

with open('ul_course_timetables.json') as of:
    corpus = load(of)

corpus = list(set([x['course_name'] for x in corpus]))

def same_types(*items) -> bool:
    return bool([1 for item in items if type(item).__name__ == type(items[0]).__name__])

def term_frequency(corpus: str | list, verbose=0) -> list:
    result = {}

    if(type(corpus).__name__ == 'list'): 
        corpus = ' '.join(corpus)

    corpus = corpus.lower()

    punctuation_pattern = "[^A-Za-z0-9' ]"
    corpus = re.sub(punctuation_pattern, ' ', corpus) # remove punctuation

    for word in corpus.split(' '):
        if(word not in result.keys()):
            search_pattern = r"\b{word}\b".format(word=word)
            result[word] = len(re.findall(search_pattern, corpus))

    # sanity check of maths
    # print(len(corpus.split()))
    # print(len(re.findall(r"\bbachelor\b", corpus))/len(corpus.split()))

    if(verbose):
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

def tf_bubble(tf_dict: dict | str | list, center: float | int, distance: float | int) -> dict:
    """
    low level clustering, bubbles instead of clusters.
    return a group of items according to a term frequency dict, returning 
    the modules of said center and any of said distance
    we will normalize the frequencies to have the center as it's apex of the graph, then use the distance to find logarithmically similar in frequency words
    """
    try:
        tf_dict = term_frequency(tf_dict)
    except TypeError as e:
        pass
    
    indexes = []
    if(same_types(center, distance) == same_types(distance, 0.0) and distance <= 1.0):
        for key, value in tf_dict.items():
            frequency_distance = float(value)/sum(tf_dict.values())
            print(key, ": \t", frequency_distance*100) # stopping here, data set is too saturated with stop words, will work on this tomorrow
            if(frequency_distance <= center+distance and frequency_distance >= center-distance):
                # print(key, frequency_distance)
                pass

def get_stopwords(corpus: dict | str | list) -> set:
    """
    we want to identify outliers using the inter-quartile range rule.
    identifying the 4 quarters of the dataset, presuming rare numbers will be in quartile 1, we will need to feed back the quartiles to 
    remove quartiles which contain rare words we wish to keep, the larger quartiles will be our stop-words.
    https://articles.outlier.org/calculate-outlier-formula
    """

    stop_words = {}

    try: 
        tf_dict = term_frequency(corpus) # returns sorted dictionary of terms and their number of instances
    except TypeError as e:
        pass
    
    # remove very rare words, like of 1 instance
    # get avg between terms
    freqs = list(tf_dict.values())
    freqs.sort() # in order

    print(tf_dict)

    quartiler = lambda perc: (int(perc*len(freqs)) + 1) if perc*len(freqs) % 1 != 0 else (perc*len(freqs))

    q1 = freqs[quartiler(0.25)]
    q3 = freqs[quartiler(0.75)]
    iqr = q3-q1
    upper_boundary = abs(q3+1.5*iqr)
    lower_boundary = abs(q1-1.5*iqr)

    print(f"""q1 = {q1}, 
    q3 = {q3}, 
    iqr = {iqr},
    upper_boundary = {upper_boundary}, 
    lower_boundary = {lower_boundary}""")

    tagged_corpora = pos_tag(list(tf_dict.keys()))
    print(tagged_corpora)
    keep = ['NN', 'NNS', 'JJ'] # <- ['Nouns', 'Plural Nouns', 'Adjectives']

    stop_words = [x[0] for x in tagged_corpora if x[1] not in keep]

    return stop_words

# using full corpus, no stop words removed
tf = term_frequency(corpus, 1)
data = []
for key, value in tf.items():
    data.append({
        'word': key,
        'count': value
    })

with open('ul_tf.json', 'w+') as f:
    dump(data, f)
# tf_bubble(corpus, center=0.4, distance=0.1)
# get_stopwords(corpus)
