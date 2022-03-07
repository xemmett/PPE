"""
Generation of the recommendation model. 
Author: Emmett Lawlor
Date: 22/6/21
"""

import pickle
from pandas import read_csv, DataFrame
from sklearn.feature_extraction.text import TfidfVectorizer
from re import sub

def prepareandfitvect(dataset):
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
    # remove words like you'll, we'll, they'll
    cleaned_df['fulldesc'] = cleaned_df['fulldesc'].str.replace("'ll", " ")
    # remove punctuation
    cleaned_df['fulldesc'] = cleaned_df['fulldesc'].replace({"[^A-Za-z0-9]+": " "}, regex=True)
    cleaned_df['fulldesc'] = cleaned_df['fulldesc'].str.strip()
    # removes stop_words like if, the, then, will, common ones
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(cleaned_df['fulldesc'])
    print(X.shape)
    print(vectorizer.build_preprocessor())
    return vectorizer

def predict_cluster(input_str):
    Y = vectorizer.transform(input_str.split(" "))
    prediction = model.predict(Y)
    return prediction

def cluster_considerations(vector):
    data = {}
    vector.sort()
    prev_n=-1
    count=0
    for n in vector:
        if(n!=prev_n):
            prev_n=n
            count=1
            data[prev_n] = count/len(vector)
        else:
            count+=1
            data[prev_n] = count/len(vector)
    return data

def recommendation_util(input_str, df):
    # remove words like you'll, we'll, they'll
    input_str = sub("\w+('ll)", "", input_str)
    # remove punctuation
    input_str = sub("[^A-Za-z0-9]+", " ", input_str)
    input_str = input_str.strip()
    prediction = predict_cluster(input_str)
    print(prediction)
    # prediction = int(prediction)
    # resulting_df = df.loc[df.cluster_prediction == prediction]
    # return resultind_df.sample(5)
    return prediction

def clusterexistingdata(df):
    df['1_degreecluster'] = ""
    df['2_degreecluster'] = ""
    df['3_degreecluster'] = ""
    df['fulldesc'] = ""
    df['cluster_prediction'] = ""
    columns = ['course_content', 'careers_or_further_progression', 'attendance_options', 'course_name', 'location_(districts)']
    for index,row in df.iterrows():
        fulldesc = ""
        for c in columns:
            val = str(row[c])
            if(val != 'nan'):
                    fulldesc+=val+' '    
        # remove words like you'll, we'll, they'll
        fulldesc = sub("\w+('ll)", "", fulldesc)
        # remove punctuation
        fulldesc = sub("[^A-Za-z0-9]+", " ", fulldesc)
        fulldesc = fulldesc.lower()
        df['fulldesc'].iloc[index] = fulldesc
        df['cluster_prediction'].iloc[index] = predict_cluster(fulldesc)
        clustcons = cluster_considerations(df['cluster_prediction'].iloc[index])
        ccs = list(clustcons.values())
        ccs.sort()
        ccs.reverse()
        degree = 0
        header = '{}_degreecluster'
        for density in ccs:
            degree+=1
            if(degree==3):
                break
            else:
                for cluster in clustcons:
                    if(clustcons[cluster] == density):
                        df[header.format(degree)].iloc[index] = cluster
    return df

def startup():
    coursedf = read_csv(r'../../scrapers/qualifax_scraper/data2020/results.csv', encoding='utf8', low_memory=False)
    coursedf['cluster_prediction'] = ""
    cao_courses = coursedf # .loc[coursedf.course_type == "Higher Education CAO"].reset_index()
    cao_courses = clusterexistingdata(cao_courses)
    return cao_courses

def main():
    userdescr = "computer engineering"
    recommended_courses = recommendation_util(userdescr, modelled_dataset)
    print(recommended_courses)

filename = '8_clustermodel.sav'
model = pickle.load(open(filename, 'rb'))
dataset = r'../../scrapers/qualifax_scraper/data2020/results.csv'
dataset = read_csv(dataset, encoding='utf8', low_memory=False)
print('START: PREPARING AND VECTORIZING')
vectorizer = prepareandfitvect(dataset)
# print('START: MODELLING DATASET')
# modelled_dataset = startup()
# print('START: RECOMMENDED COURSE')
# main()
