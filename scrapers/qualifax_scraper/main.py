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
    # searchQualifax(driver=driver)
    # searchSort()
    getCoursePage(driver=driver)
    sortResults()
    print("completed.")

main()