import pandas as pd

import matplotlib.pyplot as plt

from collections import Counter

from nltk.corpus import stopwords
from nltk.probability import FreqDist
    

df = pd.read_csv('master_courses.csv', low_memory = False)
print(df.head())

df['course_content'].dropna(inplace=True)

course_contents = ' '.join([i.lower() for i in df['course_content'].astype(str)]).split()
course_contents = [i for i in course_contents if i not in set(stopwords.words('english')) and i.isalpha()]

two_word_combs = [(course_contents[i-1]+' '+course_contents[i]) for i in range(1, len(course_contents)-1, 2)]

fdist = FreqDist(course_contents)

fdist.plot(30, cumulative=False)
plt.show()

print(Counter(course_contents).most_common(10))
print('-------------')

