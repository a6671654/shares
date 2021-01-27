import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'gupiao.settings'
import django
django.setup()
from main import models
import pandas as pd
import time
import baostock as bs
import datetime
import talib
import togmail
import tushare as ts

pro = ts.pro_api()
#=============================更新基本信息，行业等=======================================================
'''
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
gupiaolist = models.Gupiaolist.objects.all()
for obj in gupiaolist:
    lsname = obj.code
    tusharecode = lsname[3:] + '.' + lsname[:2].upper()
    lsdata=data[data['ts_code']==tusharecode].iloc[0]
    dongfangcaifu = lsname.replace('.','')
    lsdate = lsdata['list_date']
    lsdate = lsdate[:4]+'-'+lsdate[4:6]+'-'+lsdate[6:]
    models.Gupiaomsg.objects.update_or_create(code=obj,defaults={'tusharecode':tusharecode,'dongfangcaifu':dongfangcaifu,
                                                                 'listdate':lsdate,'industry':lsdata['industry']})
'''
#=======================================更新股东人数===================================================================
print('开始更新股东人数')
gupiaomsglist = models.Gupiaomsg.objects.all()
nowday = models.Jiaoyiday.objects.last()
nowday = str(nowday).replace('-','')
allnum=len(gupiaomsglist)
n=0
for obj in gupiaomsglist:
    df = pro.stk_holdernumber(ts_code=obj.tusharecode, start_date='20190101', end_date=nowday)
    df=df.iloc[0]
    lsdate = df['end_date']
    obj.holderenddate = lsdate[:4]+'-'+lsdate[4:6]+'-'+lsdate[6:]
    obj.holdernum = df['holder_num']
    try:
        obj.save()
    except:
        print(obj.code)
    n+=1
    if n%10 == 0:
        print(str(round(n/allnum*100,2))+'%')
    time.sleep(1)

#=======================================更新市值===================================================================
print('开始更新市值')
gupiaomsglist = models.Gupiaomsg.objects.all()
changdu=len(gupiaomsglist)
n=0
for i in gupiaomsglist:
    n+=1
    df = pro.daily_basic(ts_code=str(i.tusharecode), trade_date=str(i.holderenddate).replace('-',''),fields='ts_code,float_share,circ_mv')
    try:
        i.holderfloat = df['float_share'].iloc[0]
        i.holdercirc = df['circ_mv'].iloc[0]
        i.save()
    except:
        print(i,'跳过')
    if n%10==0:
        print(round(n/changdu*100,2),'%')
    time.sleep(1)
