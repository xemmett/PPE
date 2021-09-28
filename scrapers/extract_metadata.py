from pandas import DataFrame, read_csv
from json import load

def get_lookoutgrades():
    # grades in which we are looking out for
    with open(r'C:\Users\xemme\fyp\scrapers\grades.json', mode='r', encoding='utf8') as of:
        lookouts = load(of)

    grades = []
    for lvl in lookouts['level']:
        for grade in lookouts['grades']:
            lvl_grade = lvl+str(grade)
            grades.append(lvl_grade)
    
    lookouts['level_grade'] = grades

    return lookouts

def get_grades(sections = [], lookouts={}):
    for requirement in sections:
        req = requirement
        for lvlgrade in lookouts['level_grade']:
            if(lvlgrade in req):
                rm_index = req.index(lvlgrade)



