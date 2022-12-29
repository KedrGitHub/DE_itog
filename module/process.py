# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 12:40:25 2022

@author: Gluhov I.V.
"""
import pandas as pd
import datetime 



df = pd.read_csv('../data/everyday_valid.csv', parse_dates=['time'])
del df['Unnamed: 0']

data=pd.DataFrame(columns=['Surrogate_key','Currency_name','Volume_sum','Open_exchange_rate','Close_exchange_rate','Percent_difference','Biggest_volume_timeinterval','Max_exchange_rate_timeinterval','Min_exchange_rate_timeinterval'])

for s in df.symbol.unique():
    tmp = df[df['symbol']==s]
    vdate = pd.to_datetime(tmp['time']).dt.date.min()
    vkey = s + '-' + str(vdate) # Сурогантый ключ
    vsum = tmp.volume.sum() #Суммарный объем торгов за последние сутки
    vopen = list(tmp[tmp['time'] == tmp['time'].min()]['open'])[0]#Курс валюты на момент открытия торгов для данных суток
    vclose = list(tmp[tmp['time'] == tmp['time'].max()]['close'])[0]#Курс валюты на момент закрытия торгов для данных суток
    vdiff = -1*( round((vopen*100)/vclose) -100)  #Разница(в %) курса с момента открытия до момента закрытия торгов для данных суток
    vmax_t = list(tmp[tmp['volume'] == tmp['volume'].max()]['time'])[0]
    #Минимальный временной интервал, на котором был зафиксирован самый крупный объем торгов для данных суток
    vhigh_t_max = list(tmp[tmp['high'] == tmp['high'].max()]['time'])[0]
    #Минимальный временной интервал, на котором был зафиксирован максимальный курс для данных суток
    vlow_t_min = list( tmp[tmp['low'] == tmp['low'].min()]['time'])[0]
    #Минимальный временной интервал, на котором был зафиксирован минимальный курс торгов для данных суток
    
    data = data.append({'Surrogate_key':vkey, 'Currency_name':s, 'Volume_sum':vsum, 'Open_exchange_rate':vopen, 'Close_exchange_rate':vclose,'Percent_difference':vdiff,'Biggest_volume_timeinterval':vmax_t,'Max_exchange_rate_timeinterval':vhigh_t_max, 'Min_exchange_rate_timeinterval':vlow_t_min}, ignore_index=True)

data.to_csv('../data/everyday_dashboard.csv')