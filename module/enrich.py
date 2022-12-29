# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 14:53:25 2022

@author: Gluhov I.V.
"""

import pandas as pd
import requests
import time


conffile_path = '../cfg/config_extended.xml'

def ParseConfig(file):
    import xml.etree.ElementTree as ET
    tree = ET.parse(file)
    root=tree.getroot()
    apikey = root.find('apiKey').text
    slice = root.find('slice').text

    symbols = root.find('symbols')
    smb =[]
    for symbol in symbols:
        smb.append(symbol.text)

    indics = root.find('indics')
    inds=[]
    for indc in indics:
        inds.append(indc.text)

    return apikey, slice, smb, inds

apikey,  slice, symbols, indicators = ParseConfig(conffile_path)



df = pd.read_csv('../data/everyday_dashboard.csv')
symbols= df['Currency_name']
df.index = df['Currency_name']

for s in symbols:
        for f in indicators:
            url = 'https://www.alphavantage.co/query?function='+ f +'&symbol='+ s +'&interval=' +slice+'&time_period=10&series_type=open&apikey='+apikey
            r = requests.get(url)
            dt = r.json()
            dfObj = pd.DataFrame(list(dt.items()), index=['a', 'b'])
            val = (list(dfObj[1])[1])
            if val !='':
                value = str(list(val.values())[0])
                dd = str(list(val)[0]) 
            
            print(s, '-', f)
            time.sleep(15) # Ограничение бесплатной версии 5 запросов в минуту
            
            row_label   = s 
            column_name = f
            df.at[row_label, column_name] =value
            
df.to_csv('../data/everyday_dashboard_enrich.csv')

