# Simple program to remove grades from descriptions
# Cleans dataset and we extract the requirements
# produces: processable.csv
# uses: grades.json, cleaned_courses_dataset.csv
# Author: Emmett Lawlor
# 29/09/2021

from pandas import DataFrame, read_csv, read_json
from json import load
from re import sub

def get_lookoutgrades():
    # grades in which we are looking out for
    with open('grades.json', mode='r', encoding='utf8') as of:
        lookouts = load(of)[0]
    grades = []
    for lvl in lookouts['level']:
        for grade in lookouts['grades']:
            lvl_grade = lvl+str(grade)
            grades.append(lvl_grade)

    lookouts['lvl_grades'] = grades
    return lookouts

def get_grades(df: DataFrame, lookouts: dict):
    for requirement in df:
        requirement = "2 H5 and 4 O6/H7 grades, to include a language (English, Irish or another language) and Maths.".lower()
        for lvlgrade in lookouts['lvl_grades']:
            if(lvlgrade in requirement):
                print(lvlgrade)
                grade_index = requirement.index(lvlgrade) # remove grade from description.
                presight = requirement[:grade_index]
                foresight = requirement[grade_index+2:]
                
                subject_pred = get_subjects(lookouts=lookouts, body=presight)
                if(subject_pred == None):
                    subject_pred = get_subjects(lookouts=lookouts, body=foresight)

def get_subjects(lookouts: dict, body: str):
    subjects = lookouts['subjects']
    grades = lookouts['lvl_grades']
    new_grade = False

    body = sub(r'[^\w\s]', '', body).split(" ") # pattern to remove punctuation from string

    for word in body:
        word = word.strip().lower()
        if(word in subjects):
            return word
        for grade in grades:
            if(grade in word):
                new_grade = True

        if(new_grade):
            break


def main():
    lookouts = get_lookoutgrades()

    df = read_json('../scrapers/qualifax_scraper/data/sample_output.json', encoding='utf8')
    df = df[df["course_type"] == "Higher Education CAO"][:1]
    columns = list(df.columns)
    for column in columns:
        if('requirement' in column):
            df[column] = df[column].astype('str').replace('nan', '').replace('\n', ' ')
            df[column] = df[column].str.lower()
            get_grades(df=df[column], lookouts=lookouts)

main()