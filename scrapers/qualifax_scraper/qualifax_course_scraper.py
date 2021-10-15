# produces results.json
# reads from cleaned_search_results.csv
# 29/09/2021
# Author: Emmett Lawlor

from selenium import webdriver
import pandas as pd
import re
import json
from time import sleep

def check_for_link(value):
    try:
        link_obj = value.find_element_by_xpath('a')
        link = link_obj.get_attribute("href")
    except:
        link = value.get_attribute("innerHTML")
        pass
    finally:
        return link

def format_text(text):
    text = text.replace("\t", "")
    text = text.replace("&amp;", "and")
    text = text.replace("&nbsp;More info...", "")
    text = text.replace("Expand+", "")
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    text = text.strip()
    if('Hide-' in text):
        text = text.split("Hide-")[1]
    return text

def read_subtable(value):
    data = {}

    try:
        subtable = value.find_elements_by_xpath('table/tbody/tr')
        headers = subtable[0].find_elements_by_xpath("td")
        values = subtable[1].find_elements_by_xpath("td")
        index = 0
        for header in headers:
            header = header.get_attribute("innerHTML")
            header = format_headers(header)
            info = values[index].get_attribute('innerHTML')
            info = format_text(info)
            data[header] = info
            index+=1

    except:
        pass

    finally:
        return data

def format_headers(text):
    text = text.lower().strip()
    text = text.replace("<br>", "")
    text = text.replace(" ", "_")
    return text

def define_course(table):
    rows = table.find_elements_by_xpath('tr')
    course = {}
    i=0

    for row in rows:
        values = [x for x in row.find_elements_by_xpath('td')]
        column_name = values[0].get_attribute('innerHTML')
        column_name = format_headers(column_name)
        column_value = values[1].get_attribute("innerHTML")
        column_value = format_text(column_value)

        if(column_name == 'qualifications'):
            subtable = read_subtable(values[1])
            column_value = subtable
        else:
            if(column_value == 'Web Page - Click Here'):
                column_value = check_for_link(values[1])

        course[column_name] = column_value
    return course

def getCoursePage(driver, read_from:str, destination_file: str):
    search_results = pd.read_csv(read_from)
    courses = []
    errors=0
    errorenous_links = []
    for i,row in search_results.iterrows():
        sleep(1.5)
        with open(destination_file, 'w+', encoding='utf8') as of:
            link = row['link']
            driver.get(link)
            try:
                table = driver.find_element_by_xpath('/html/body/div/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody')
                course = define_course(table)

                try:
                    points_table = driver.find_element_by_xpath('/html/body/div/div/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody')
                    points = define_course(points_table)
                    points.pop('year')
                    course['points'] = points
                except:
                    pass

                finally:
                    courses.append(course)
                    json.dump(courses, of)

            except:
                errors+=1
                errorenous_links.append(link)
                pass
    print('errors:', errors)
    print('links', errorenous_links)

    return courses