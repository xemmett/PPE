"""
Author: Emmett Lawlor
Purpose: Any processes needed to manipulate UL data.
Date: 16 FEB 2022
"""

from operator import concat
import pandas as pd

"""
Author: Emmett Lawlor
Purpose: Aggregate Ul_scraper_data into one large data source
Data: 16 FEB 2022
"""


def agg(dfs=[]):
    master = pd.DataFrame()
    for df in dfs:
        master = master.append(df)
    
    return master

def agg_timetables():
    new_timetables = timetables.copy()
    for t in new_timetables:
        new_timetables[t]['academic_period'] = t
    
    master = agg(new_timetables.values())
    master.to_excel('ul_course_timetables.xlsx', index=0)

def agg_classes():
    classes = pd.DataFrame()
    for a in timetables:
        for c in timetables[a]['class']:
            class_df = pd.json_normalize(c)
            class_df['academic_period'] = a
            classes = classes.append(class_df)
    classes.to_excel('ul_course_timetables_classes.xlsx', index=0)

def agg_course_year_modules():
    course_year_modules = {
        '2020SEM2': pd.read_json('../../scrapers/ul_scrapers_data2020/module_course_details.json'),
        '2021SEM1': pd.read_json('../../scrapers/ul_scrapers_data2021/module_course_details.json'),
        '2022SEM2': pd.read_json('../../scrapers/ul_scrapers_data2022/module_course_details.json')
    }
    master = pd.DataFrame()
    
    for a in course_year_modules:
        i = 0
        for c in course_year_modules[a]['classes']:
            class_df = pd.json_normalize(c)
            print(class_df)
            class_df['academic_period'] = a
            class_df['course_code'] = course_year_modules[a]['course_code'][i]
            class_df['course_year'] = course_year_modules[a]['course_year'][i]
            master = master.append(class_df)
            i += 1

    master.to_excel('ul_module_course_details.xlsx', index=0)


def main():
    # agg_timetables()
    # agg_classes()
    agg_course_year_modules()


if __name__ == '__main__':

    timetables = {
        '2020SEM2': pd.read_json('../../scrapers/ul_scrapers_data2020/ul_course_timetables.json'),
        '2021SEM1': pd.read_json('../../scrapers/ul_scrapers_data2021/ul_course_timetables.json'),
        '2022SEM2': pd.read_json('../../scrapers/ul_scrapers_data2022/ul_course_timetables.json')
    }

    book_of_modules = {
        '2020SEM2': pd.read_json('../../scrapers/ul_scrapers_data2020/ul_module_details.json'),
        '2021SEM1': pd.read_json('../../scrapers/ul_scrapers_data2021/ul_module_details.json'),
        '2022SEM2': pd.read_json('../../scrapers/ul_scrapers_data2022/ul_module_details.json')
    }

    main()