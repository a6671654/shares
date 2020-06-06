import pandas as pd 
import numpy as np
import time
import os
import talib

name_list=os.listdir('try')
n=0
num=len(name_list)

for i in name_list:
    a=pd.read_csv(f'try/{i}',index_col=0)
    a=a[a['tradestatus']==1]
    if len(a.index)>50:
        a['DIF'],a['DEA'],a['hist']=talib.MACD(a['close'], fastperiod=12, slowperiod=26, signalperiod=9)
        df_status=a
        low = df_status['low'].astype(float)
        del df_status['low']
        df_status.insert(0, 'low', low)
        high = df_status['high'].astype(float)
        del df_status['high']
        df_status.insert(0, 'high', high)
        close = df_status['close'].astype(float)
        del df_status['close']
        df_status.insert(0, 'close', close)
        low_list = df_status['low'].rolling(window=9).min()
        high_list = df_status['high'].rolling(window=9).max()
        rsv = (df_status['close'] - low_list) / (high_list - low_list) *100
        a['K'] = rsv.ewm(com=2).mean()
        a['D'] = a['K'].ewm(com=2).mean()
        a['J'] = 3 * a['K'] - 2 * a['D']
        a['5day']=talib.SMA(a['close'],timeperiod=5)
        a['10day']=talib.SMA(a['close'],timeperiod=10)
        a['20day']=talib.SMA(a['close'],timeperiod=20)
        a['upper'], a['middle'], a['lower'] = talib.BBANDS(a['close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        a['EMA12'] = talib.EMA(a['close'], timeperiod=12)
        a['EMA26'] = talib.EMA(a['close'], timeperiod=26)
        a.to_csv(f'try/{i}')
        n+=1
        print(i,f'已完成{round((n/num)*100,2)}%')
    else:
        print(i,'未计算')
