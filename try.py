import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'gupiao.settings'
import django
django.setup()
from main import models
import pandas as pd
import time



#导入gupiaolist
a=pd.read_csv('all.csv')
for i in range(len(a.index)):
    print(a.iloc[i,1],a.iloc[i,3])
    b=models.Gupiaolist(code=a.iloc[i,1],codename=a.iloc[i,3])
    b.save()
print('股票列表导入成功')
#导入近30个交易日jiaoyiday
a=pd.read_csv('try/sh.600000.csv')
a=a.tail(30)
daorulist=[]
for i in list(a['date']):
    obj= models.Jiaoyiday(date=i,isover=True)
    daorulist.append(obj)
models.Jiaoyiday.objects.bulk_create(daorulist)
print('交易日导入成功')

#删除不要的股票，需要移动到11文件夹
name_list=os.listdir('11')
for i in name_list:
    code1=models.Gupiaolist.objects.get(code=i[:-4])
    print(code1.code,code1.codename)
    code1.delete()
print('已删除不要的股票')
#导入数据

a=models.Jiaoyiday.objects.all()
allday=[i.date for i in a]
a=models.Gupiaolist.objects.all()
allcode=[ i.code for i in a ]
for i in allday:
    dayobject=models.Jiaoyiday.objects.get(date=i)
    print(dayobject.date)
    appendlist=[]
    for ii in allcode:
        codeobject=models.Gupiaolist.objects.get(code=ii)
        a=pd.read_csv(f'try/{ii}.csv')
        a['date']=pd.to_datetime(a['date'])

        try:
            a=a[a['date']==pd.Timestamp(i)].iloc[0]
            obj=models.kline(code=codeobject,date=dayobject,open=a['open'],close=a['close'],
                             high=a['high'],low=a['low'],volume=a['volume'],
                             turn=a['turn'],preclose=a['preclose'],dif=a['DIF'],
                             dea=a['DEA'],hist=a['hist'],kdjK=a['K'],kdjD=a['D'],
                             kdjJ=a['J'],day5=a['5day'],day10=a['10day'],
                             day20=a['20day'],upper=a['upper'],middle=a['middle'],lower=a['lower'])
            appendlist.append(obj)
        except Exception as E:
            print(ii)
            print(E)
            pass

    models.kline.objects.bulk_create(appendlist)
print('K线部分以导入完成，开始导入最后计算部分')
a=models.kline.objects.all()
allnum=len(a)
jishu=0
print(allnum)
for i in a:
    jishu+=1
    name=i.code.code
    nowdate=i.date.date
    a = pd.read_csv(f'try/{name}.csv')
    a['date'] = pd.to_datetime(a['date'])
    b=a[a['date']==pd.Timestamp(nowdate)]
    newindex=(b.index.values)[0]
    buymean20=(a['volume'].iloc[newindex-20:newindex].mean())
    buymean5=(a['volume'].iloc[newindex-5:newindex].mean())
    jihelist=[]
    if a['volume'].iloc[newindex]>buymean20*2:
        jihelist.append('buynum20=True')
    elif a['volume'].iloc[newindex]<buymean20*0.5:
        jihelist.append('buynum20=False')
    if a['volume'].iloc[newindex]>buymean5*2:
        jihelist.append('buynum5=True')
    elif a['volume'].iloc[newindex]<buymean5*0.5:
        jihelist.append('buynum5=False')
    if a['hist'].iloc[newindex]>0 and a['hist'].iloc[newindex-1]<0:
        jihelist.append('MACD=True')
    elif a['hist'].iloc[newindex]<0 and a['hist'].iloc[newindex-1]>0:
        jihelist.append('MACD=False')
    if a['5day'].iloc[newindex]>a['10day'].iloc[newindex] and a['5day'].iloc[newindex-1]<a['10day'].iloc[newindex-1]:
        jihelist.append('day5to10=True')
    elif a['5day'].iloc[newindex]<a['10day'].iloc[newindex] and a['5day'].iloc[newindex-1]>a['10day'].iloc[newindex-1]:
        jihelist.append('day5to10=False')
    if a['5day'].iloc[newindex]>a['20day'].iloc[newindex] and a['5day'].iloc[newindex-1]<a['20day'].iloc[newindex-1]:
        jihelist.append('day5to20=True')
    elif a['5day'].iloc[newindex]<a['20day'].iloc[newindex] and a['5day'].iloc[newindex-1]>a['20day'].iloc[newindex-1]:
        jihelist.append('day5to20=False')
    if a['10day'].iloc[newindex]>a['20day'].iloc[newindex] and a['10day'].iloc[newindex-1]<a['20day'].iloc[newindex-1]:
        jihelist.append('day10to20=True')
    elif a['10day'].iloc[newindex]<a['20day'].iloc[newindex] and a['10day'].iloc[newindex-1]>a['20day'].iloc[newindex-1]:
        jihelist.append('day10to20=False')
    if a['volume'].iloc[newindex]>a['volume'].iloc[newindex-1]*2:
        jihelist.append('buynumtwo=True')
    elif a['volume'].iloc[newindex]<a['volume'].iloc[newindex-1]*0.5:
        jihelist.append('buynumtwo=False')
    if a['K'].iloc[newindex]>a['D'].iloc[newindex] and a['K'].iloc[newindex-1]<a['D'].iloc[newindex-1]:
        jihelist.append('KDJ=True')
    elif a['K'].iloc[newindex]<a['D'].iloc[newindex] and a['K'].iloc[newindex-1]>a['D'].iloc[newindex-1]:
        jihelist.append('KDJ=False')
    if a['volume'].iloc[newindex+1-1] > a['volume'].iloc[newindex+1-2]:
        if a['volume'].iloc[newindex+1-2] > a['volume'].iloc[newindex+1-3]:
            if a['volume'].iloc[newindex+1-3] > a['volume'].iloc[newindex+1-4]:
                jihelist.append('buynum3up=True')
                if a['volume'].iloc[newindex+1-4] > a['volume'].iloc[newindex+1-5] and a['volume'].iloc[newindex+1-5] > a['volume'].iloc[newindex+1-6]:
                    jihelist.append('buynum5up=True')
        else:
            if a['volume'].iloc[newindex+1-3] < a['volume'].iloc[newindex+1-4] and a['volume'].iloc[newindex+1-4] < a['volume'].iloc[newindex+1-5]:
                jihelist.append('buynum3chang=False')
                if a['volume'].iloc[newindex+1-5] < a['volume'].iloc[newindex+1-6] and a['volume'].iloc[newindex+1-6] < a['volume'].iloc[newindex+1-7]:
                    jihelist.append('buynum5chang=False')
    else:
        if a['volume'].iloc[newindex+1-2] < a['volume'].iloc[newindex+1-3]:
            if a['volume'].iloc[newindex+1-3] < a['volume'].iloc[newindex+1-4]:
                jihelist.append('buynum3up=False')
                if a['volume'].iloc[newindex+1-4] < a['volume'].iloc[newindex+1-5] and a['volume'].iloc[newindex+1-5] < a['volume'].iloc[newindex+1-6]:
                    jihelist.append('buynum5up=False')
        else:
            if a['volume'].iloc[newindex+1-3] > a['volume'].iloc[newindex+1-4] and a['volume'].iloc[newindex+1-4] > a['volume'].iloc[newindex+1-5]:
                jihelist.append('buynum3chang=True')
                if a['volume'].iloc[newindex+1-5] > a['volume'].iloc[newindex+1-6] and a['volume'].iloc[newindex+1-6] > a['volume'].iloc[newindex+1-7]:
                    jihelist.append('buynum5chang=True')



    if len(jihelist)>0:
        zxnr=''
        for ii in jihelist:
            zxnr=zxnr+ii+','
        zxnr=zxnr[:-1]
        ojc=eval(f'models.jisuan(code=i.code,date=i.date,{zxnr})')
        ojc.save()
        print(round((jishu/allnum)*100,4),'%')