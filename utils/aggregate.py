"""
Author: Emmett Lawlor
Purpose: Aggregate Ul_scraper_data into one large data source
Data: 16 FEB 2022
"""
import pandas as pd


def agg(dfs=[]):
    master = pd.DataFrame()
    for df in dfs:
        master = master.append(df)
    
    return master