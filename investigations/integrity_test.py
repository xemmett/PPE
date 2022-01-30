""""
Author: Emmett Lawlor
Date: 18-01-22
Purpose: See if there are any contradictions in the UL data between timetable.ul.ie, and bookofmodules
"""

DATA_FOLDER_PATH = '../scrapers/ul_scrapers_data2020'

from itertools import groupby
import pandas as pd
from datetime import datetime
from json import load

def readJSON(filename):
    with open(filename, mode='r') as f:
        return load(f)
    
def countTimetableHours():
    timetables = readJSON(f'{DATA_FOLDER_PATH}/ul_course_timetables.json')
    class_only = [x['class'] for x in timetables]
    course_codes = [x['course_code'] for x in timetables]
    course_years = [x['course_year'] for x in timetables]

    df = pd.read_json(f'{DATA_FOLDER_PATH}/ul_course_timetables.json')
    df = pd.DataFrame()

    index = 0
    for c in class_only:
        class_df = pd.json_normalize(c)
        class_df['course_code'] = course_codes[index]
        class_df['course_year'] = course_years[index]

        df = df.append(class_df)
        index+=1
    
    # convert time strings to time objects
    df = df[df['start_time'] != None]
    df = df[df['end_time'] != None]
    
    str_to_time = lambda t: datetime.strptime(str(t), '%H:%M')
    df['start_time'] = df['start_time'].apply(lambda t: str_to_time(t))
    df['end_time'] = df['end_time'].apply(lambda t: str_to_time(t))
    # calculate, turn seconds into hours, hopefully no remainder
    df['duration'] = (df['end_time'] - df['start_time']).apply(lambda t: t.seconds/60/60)

    df['occurences'] = df['active_weeks'].apply(lambda occurences: countOccurences(occurences))
    df['total_hours'] = df['occurences'] * df['duration']
    
    return df

def countOccurences(o=[]):
    total = 0
    for i in o:
        total += 1 # plus one to include the initial week.
        try:
            weeks_range = [int(x) for x in i.split('-')]
        except ValueError as e:
            return None
        if(len(weeks_range) > 1):
            total += (weeks_range[1] - weeks_range[0]) 
    return total

def countBOMHours():
    bookofmodules = readJSON(f'{DATA_FOLDER_PATH}/ul_module_details.json')
    df = pd.DataFrame()
    for m in bookofmodules:
        required_hours = m['required_hours']
        required_hours['total_hours'] = sum(int(x) for x in required_hours.values())
        required_hours['module'] = m['module_code']
        
        hours_df = pd.json_normalize(required_hours)
        df = df.append(hours_df)

    df['total_hours'] = df['total_hours'] - df['Credits'].fillna(0).astype(int)
    return df

def main():
    hours_tt = countTimetableHours()
    hours_bom = countBOMHours()

    hours_tt.to_csv('integrity_test_data/tt_hours.csv', index = 0)
    hours_bom.to_csv('integrity_test_data/bom_hours.csv', index = 0)

main()