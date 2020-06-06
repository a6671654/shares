import pandas as pd 
import numpy as np
import time
import baostock as bs
import os

a=pd.read_csv('all.csv')
num=len(a['code'])
n=0
print(num)
name_list=os.listdir('try')


lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

for i in a['code']:
    n+=1
    if f'{i}.csv' in name_list:
        print(i,'已完成:',f'{round(n/num*100,2)}%')
        continue
        
    rs = bs.query_history_k_data_plus(i,"date,open,high,low,close,preclose,volume,amount,turn,tradestatus,pctChg,isST,peTTM,psTTM,pcfNcfTTM,pbMRQ",start_date='2019-09-01', end_date='2020-04-27',frequency="d", adjustflag="2")
    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)

    #### 结果集输出到csv文件 ####   
    result.to_csv(f"try/{i}.csv", index=False)
    print(i,'已完成:',f'{round(100*n/num,2)}%')
    if n%500==499:
        bs.logout()
        print('已完成500，休息15秒')
        time.sleep(15)
        lg = bs.login()
        
bs.logout()

