# Simple program to parse & clean the values from qualifax_search_results.csv
# This was primarily to format the providers results (host college)
# I created sortdata in June of 2021, but now in 28/09/2021 wrote searchsort.
# Author: Emmett Lawlor

import ast
import pandas as pd
from pandas.core.base import DataError
from pandas.core.frame import DataFrame

def sortdata():
    df = pd.read_csv('data/qualifax_search_results.csv', encoding='utf8')

    columns = list(df.columns)
    columns += ['provider_1', 'provider_link_1', 'provider_2', 'provider_link_2', 'provider_3', 'provider_link_3', 'provider_4', 'provider_link_4', 'provider_5', 'provider_link_5']
    cleaned_df = pd.DataFrame([], columns=columns)

    for column in columns:
        try:
            cleaned_df[column] = df[column].astype('str')
        except KeyError as e:
            cleaned_df[column] = ''


    for i,row in cleaned_df.iterrows():
        providers = ast.literal_eval(row['[provider, link]'])
        for provider in providers:
            index = providers.index(provider)+1
            header_name = f'provider_{index}'
            header_link = f'provider_link_{index}'

            cleaned_df[header_name][i] = provider[0]
            cleaned_df[header_link][i] = provider[1]
            cleaned_df[i] = row
            print(cleaned_df[i])

    columns.pop(columns.index('[provider, link]'))
    cleaned_df.to_csv('data/cleaned_search_results.csv', encoding='utf8')

def searchSort():
    df = pd.read_csv('data/qualifax_search_results.csv', encoding='utf8')
    columns = list(df.columns)
    cleaned_df = DataFrame([], columns=columns)

    for i,row in df.iterrows():
        print(i)
        providers = ast.literal_eval(row['[provider, link]'])
        index = 0
        for provider in providers:
            name = f'provider_{index}'
            link = f'provider_link_{index}'

            row[name] = provider[0]
            row[link] = provider[1]

        cleaned_df = cleaned_df.append(row)

    cleaned_df = cleaned_df.drop(columns='[provider, link]')
    cleaned_df.to_csv('data/cleaned_search_results.csv', encoding='utf8')