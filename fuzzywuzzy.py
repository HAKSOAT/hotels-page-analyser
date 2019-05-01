#!/usr/bin/env python
# coding: utf-8

# In[35]:


from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import pandas as pd
df=pd.read_csv('/home/hotelsng/FinalCsv.csv' , names=['Url', 'Label'])
df.head()
url=input()
def get_category(row):
    choices= row['Label']
    possibilities = process.extract(url, choices, scorer=fuzz.token_sort_ratio)
    print(possibilities[0]) #the first result is the category it should belong, the second result is the similarity score, the third is the position on the csv
get_category(df)

