# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 15:58:21 2022

@author: Gluhov I.V.
"""

import pandas as pd
from alpha_vantage.timeseries import TimeSeries


conffile_path = '../cfg/config_history.xml'

def ParseConfig(file):
    import xml.etree.ElementTree as ET
    tree = ET.parse(file)
    root=tree.getroot()
    apikey = root.find('apiKey').text
    interval = root.find('interval').text
    slice = root.find('slice').text
    symbols = root.find('symbols')
 
    smb =[]
    for symbol in symbols:
        smb.append(symbol.text)
    return apikey, interval, slice, smb


apikey, interval, slice, symbols = ParseConfig(conffile_path)
print(apikey)

ts = TimeSeries(key = apikey, output_format = 'csv')
all_res = []
for symbol in symbols:
    totalData = ts.get_intraday_extended(symbol = symbol, interval = interval, slice = slice)
    df = pd.DataFrame(list(totalData[0]))
    header_row=0
    df.columns = df.iloc[header_row]
    df = df.drop(header_row)
    df['symbol'] = symbol
    df.head()
    all_res.append(df)

df_res = pd.concat(all_res)
df_res.to_csv("../data/history.csv")
