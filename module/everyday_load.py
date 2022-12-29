# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 16:16:27 2022

@author: Glyuhov I.V.
"""

import pandas as pd
from alpha_vantage.timeseries import TimeSeries

conffile_path = '../cfg/config_everyday.xml'

def ParseConfig(file):
    import xml.etree.ElementTree as ET
    tree = ET.parse(file)
    root=tree.getroot()
    apikey = root.find('apiKey').text
    interval = root.find('interval').text
    symbols = root.find('symbols')
    smb =[]
    for symbol in symbols:
        smb.append(symbol.text)
    return apikey, interval, 'year1month2', smb

apikey, interval, slice, symbols = ParseConfig(conffile_path)

ts = TimeSeries(key = apikey, output_format = 'csv')
all_res = []
for symbol in symbols:
    totalData = ts.get_intraday_extended(symbol = symbol, interval = interval, slice = slice)
    df = pd.DataFrame(list(totalData[0]))
    header_row=0
    df.columns = df.iloc[header_row]
    df = df.drop(header_row)
    df['symbol'] = symbol
    all_res.append(df)

df_res = pd.concat(all_res)
df_res['time'] = pd.to_datetime(df_res['time'])
df_res = df_res[df_res['time'].dt.date==df_res['time'].dt.date.max()]
df_res.to_csv("../data/everyday.csv")