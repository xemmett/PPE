from re import search
from selenium import webdriver

from qualifax_scraper import searchQualifax
from sort_search_results import searchSort

from qualifax_course_scraper import getCoursePage
from sort_results import sortResults

def define_driver():
    driver = webdriver.Chrome()
    return driver

def main():
    driver = define_driver()
    # searchQualifax(driver=driver) # produces qualifax_search_results.csv
    # searchSort(read_from = 'data/qualifax_search_results.csv', destination_file = 'data/cleaned_search_results.csv') # produces cleaned_search_results.csv
    getCoursePage(driver=driver, read_from='data/cleaned_search_results.csv', destination_file = 'data/results.json') # produces results.json
    
    sortResults(read_from = "data/results.json", destination_file = "data/master_courses.csv") # produces results.csv -> master_courses.csv
    print("completed.")

main()