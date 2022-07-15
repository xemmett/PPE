# this is a scraper to extract all course details on qualifax
# produces = qualifax_search_results.csv
# 1st step, run this in Windows command
# next step, run sort_Search_results.py
# Author: Emmett Lawlor

import pandas as pd

def get_results(driver):
    driver.get("https://www.qualifax.ie/qf/QFPublic/?Mainsec=courses&Subsec=search_courses&CRAsort=&action=search&display=&CRT_ID=0,0&CSH_ID=18&PREV_CSH_ID=&AdvancedKeyword=&keywords_and_titles=title&all_or_any_words=all&full_or_part_words=full&FCT_ID=&FDM_ID=&keywords=&QUA_ID=0&CTP_ID=0&COL_ID=0&RES_ID=0&points=&CRS_CODE=&CRA_ID=0&ATT_ID=0&PRV_ID=0&COU_ID=0&DST_ID=0")
    search_all_tag = '//*[@id="main"]/table/tbody/tr/td[3]/table/tbody/tr[6]/td/button[1]'
    driver.find_element_by_xpath(search_all_tag).click()

def get_courses(driver):
    base_link = 'https://www.qualifax.ie/qf/QFPublic/?Mainsec=courses&Subsec=search_courses&CRAsort=&action=search&display=&CRT_ID=0&CSH_ID=18&PREV_CSH_ID=&AdvancedKeyword=&keywords_and_titles=title&all_or_any_words=all&full_or_part_words=full&FCT_ID=&FDM_ID=&keywords=&QUA_ID=0&CTP_ID=0&COL_ID=0&RES_ID=0&points=&CRS_CODE=&CRA_ID=0&ATT_ID=0&PRV_ID=0&COU_ID=0&DST_ID=0'
    pagination_query = '&firstpage=1&vStart=1&Idx={}&searchaction=current'
    df = pd.DataFrame([], columns=['code', 'name', 'link', '[provider, link]', 'nfq_level', 'nfq_classification'])
    urls = []
    for i in range(2, 299):
        table_rows = driver.find_elements_by_xpath("/html/body/div/div/form/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr[*]")
        
        for row in table_rows:
            cells = row.find_elements_by_xpath("td")
            try:
                code = cells[2].get_attribute("innerHTML").strip()
                course_box = cells[3].find_element_by_xpath("a")

                course_name = course_box.get_attribute("text").strip()
                course_link = course_box.get_attribute("href").strip()
                course_provider = cells[4].find_elements_by_xpath("a")
                providers = []
                for provider in course_provider:
                    provider_link = provider.get_attribute("href").strip()
                    provider_name = provider.get_attribute("text").strip()
                    providers+=[[provider_name, provider_link]]
                nfq_level = cells[5].get_attribute("innerHTML").strip()
                nfq_classification = cells[6].get_attribute("innerHTML").strip()

                new_entry = {
                    'code': code, 
                    'name': course_name, 
                    'link': course_link, 
                    '[provider, link]': providers,
                    'nfq_level': nfq_level, 
                    'nfq_classification': nfq_classification
                }

                df = df.append(new_entry, ignore_index=True)
            except:
                pass # no rows

        df.to_csv('qualifax_search_results.csv')
        query = base_link+pagination_query.format(i)
        driver.get(query)

def searchQualifax(driver):
    get_results(driver)
    get_courses(driver)