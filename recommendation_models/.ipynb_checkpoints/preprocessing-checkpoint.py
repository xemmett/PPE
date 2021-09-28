from pandas import read_csv, DataFrame

dataset = read_csv(r"C:\Users\Emmett\fyp\scrapers\qualifax_scraper\results.csv", encoding='utf8', low_memory=False)

columns = ['course_content', 'careers_or_further_progression', 'attendance_options', 'course_name', 'location_(districts)']
df = DataFrame([], columns=columns)
for c in columns:
    df[c] = dataset[c]

df['fulldesc'] = ""
for index,row in df.iterrows():
    fulldesc = ""
    for val in row.values:
        if(str(val) != 'nan'):
            fulldesc+=val+' '
    df['fulldesc'].iloc[index] = fulldesc.lower().strip()

cleaned_df = df[df['fulldesc']!='']

# remove "'ll" from words like you'll, we'll, they'll
# cleaned_df['fulldesc'] = cleaned_df['fulldesc'].str.replace("'ll", " ")

# remove punctuation
cleaned_df['fulldesc'] = cleaned_df['fulldesc'].replace({"[^A-Za-z0-9]+": " "}, regex=True)
cleaned_df['fulldesc'] = cleaned_df['fulldesc'].str.strip()

# convert the textual data into vectors, only fulldesc
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt

# removes stop_words like if, the, then, will, common ones
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(cleaned_df['fulldesc'])

# check for ideal number of clusters using elbow method
wcss = []
sscores = []
for k in range(2,50):
    print("cluster:", k)
    kmeans = KMeans(n_clusters=k, init='k-means++', max_iter=500, n_init=15)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)
    score = metrics.silhouette_score(X, kmeans.labels_, metric='euclidean')
    sscores.append({str(k):score})

plt.plot(range(2,50),wcss)
plt.title("Elbow Method")
plt.xlabel("Number of clusters")
plt.ylabel("wcss")
plt.show()

# when cluster size is decided upon
# true_k = 43
# model = KMeans(n_clusters=true_k, init='k-means++', max_iter=500, n_init=15)
# model.fit(X)

# filename = f"{true_k}_clustermodel.sav"
# import pickle
# pickle.dump(model, open(filename, 'wb'))
