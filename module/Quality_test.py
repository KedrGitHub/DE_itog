# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 12:40:25 2022

@author: Gluhov I.V.
"""
import pandas as pd

def replace_by_mean(data):
    data['open'].fillna(data['open'].mean(), inplace = True)
    data['high'].fillna(data['high'].mean(), inplace = True)
    data['low'].fillna(data['low'].mean(), inplace = True)
    data['close'].fillna(data['close'].mean(), inplace = True)
    data['volume'].fillna(data['volume'].mean(), inplace = True)
    return data

def dropna(data):
    data.dropna(how='all')



df = pd.read_csv('../data/everyday.csv')
df = replace_by_mean(df)

if df.isnull().any().any():
    df = dropna(df)
    
df.to_csv("../data/everyday_valid.csv")