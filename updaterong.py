import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'gupiao.settings'
import django
django.setup()
from main import models
import pandas as pd
import tushare as ts
import togmail
import time
import datetime
from django.db.models import Q
#寻找未更新日期

pro = ts.pro_api()

lastday=models.Jiaoyiday.objects.filter(isover=True).filter(liangrong=True).last()
muqian = models.Liangrong.objects.filter(dayline__date=lastday)
if len(muqian)<1300:
    print(str(lastday),'前一日两融数据少于1300，正在尝试补充')
    day = str(lastday).replace('-', '')
    df = pro.margin_detail(trade_date=day)
    appendlist = []
    idlist = []
    klinejihe = models.Kline.objects.filter(date=lastday).filter(~Q(liangrong__id__gt=1)).filter(code__liangrong=True)
    for i in klinejihe:
        idlist.append(i.id)
    for klineobj in klinejihe:
        lsname = klineobj.code.code
        lsname = lsname[3:] + '.' + lsname[:2].upper()
        try:
            shuju = df[df['ts_code'] == lsname].iloc[0]
            newobj = models.Liangrong(dayline=klineobj, rzye=shuju['rzye'], rqye=shuju['rqye'], rzmre=shuju['rzmre'],
                                      rqyl=shuju['rqyl'], rzche=shuju['rzche'], rqchl=shuju['rqchl'],
                                      rqmcl=shuju['rqmcl'],
                                      rzrqye=shuju['rzrqye'])
            appendlist.append(newobj)
        except:
            print(day, lsname, 'tushare中没有')
    if len(appendlist) > 1:
        models.Liangrong.objects.bulk_create(appendlist)
        ronglist = models.Liangrong.objects.filter(dayline_id__in=idlist)
        for rongobj in ronglist:
            rongobjs = models.Liangrong.objects.filter(dayline__code=rongobj.dayline.code)
            if len(rongobjs) > 6:
                rongobjs = rongobjs.order_by('-id')[:7]
                rongobj.rzjmr3 = int(rongobjs[0].rzmre - rongobjs[0].rzche + rongobjs[1].rzmre - rongobjs[1].rzche + rongobjs[2].rzmre -rongobjs[2].rzche)
                rongobj.rzjmr5 = int(rongobj.rzjmr3 + rongobjs[3].rzmre - rongobjs[3].rzche + rongobjs[4].rzmre - rongobjs[4].rzche)
                if rongobjs[0].rzmre > rongobjs[0].rzche:
                    for iii in range(1, 7):
                        if rongobjs[iii].rzmre > rongobjs[iii].rzche:
                            iii += 1
                            pass
                        else:
                            break
                    rongobj.rzjzz = iii
                else:
                    for iii in range(1, 7):
                        if rongobjs[iii].rzmre < rongobjs[iii].rzche:
                            iii += 1
                            pass
                        else:
                            break
                    rongobj.rzjzz = -iii
                if rongobjs[0].rqmcl > rongobjs[0].rqchl:
                    for iii in range(1, 7):
                        if rongobjs[iii].rqmcl > rongobjs[iii].rqchl:
                            iii += 1
                            pass
                        else:
                            break
                    rongobj.rqjjx = iii
                else:
                    for iii in range(1, 7):
                        if rongobjs[iii].rqmcl < rongobjs[iii].rqchl:
                            iii += 1
                            pass
                        else:
                            break
                    rongobj.rqjjx = -iii
                rongobj.save()
        changdu = len(appendlist)
        print(changdu,'条数据补充成功')
        togmail.send(to='254370469@qq.com',title=str(lastday)+'两融已补充',content=f'补充{changdu}条')

#=================================================================今天更新=================================

gengxinday=models.Jiaoyiday.objects.filter(isover=True).filter(~Q(liangrong=True))
for i in gengxinday:
    chaju=datetime.datetime.now().date()-i.date
    if (chaju.days == 1 and datetime.datetime.now().hour >= 9) or chaju.days>1:
        day=str(i).replace('-','')
        print('开始更新',day)
        df = pro.margin_detail(trade_date=day)
        appendlist=[]
        klinejihe=models.Kline.objects.filter(date=i).filter(code__liangrong=True)
        for klineobj in klinejihe:
            lsname=klineobj.code.code
            lsname=lsname[3:]+'.'+lsname[:2].upper()
            try:
                shuju = df[df['ts_code'] == lsname].iloc[0]
                newobj = models.Liangrong(dayline=klineobj,rzye=shuju['rzye'],rqye=shuju['rqye'],rzmre=shuju['rzmre'],
                                          rqyl=shuju['rqyl'],rzche=shuju['rzche'],rqchl=shuju['rqchl'],rqmcl=shuju['rqmcl'],
                                          rzrqye=shuju['rzrqye'])
                appendlist.append(newobj)
            except:
                print(day,lsname,'tushare中没有')
        if len(appendlist)>100:
            models.Liangrong.objects.bulk_create(appendlist)
            print('基础数据写入成功，开始计算其他数据')
            ronglist=models.Liangrong.objects.filter(dayline__date=i)
            for rongobj in ronglist:
                rongobjs=models.Liangrong.objects.filter(dayline__code=rongobj.dayline.code)
                if len(rongobjs)>6:
                    rongobjs=rongobjs.order_by('-id')[:7]
                    rongobj.rzjmr3=int(rongobjs[0].rzmre-rongobjs[0].rzche+rongobjs[1].rzmre-rongobjs[1].rzche+rongobjs[2].rzmre-rongobjs[2].rzche)
                    rongobj.rzjmr5=int(rongobj.rzjmr3+rongobjs[3].rzmre-rongobjs[3].rzche+rongobjs[4].rzmre-rongobjs[4].rzche)
                    if rongobjs[0].rzmre>rongobjs[0].rzche:
                        for iii in range(1,7):
                            if rongobjs[iii].rzmre>rongobjs[iii].rzche:
                                iii+=1
                                pass
                            else:
                                break
                        rongobj.rzjzz=iii
                    else:
                        for iii in range(1,7):
                            if rongobjs[iii].rzmre<rongobjs[iii].rzche:
                                iii+=1
                                pass
                            else:
                                break
                        rongobj.rzjzz=-iii
                    if rongobjs[0].rqmcl>rongobjs[0].rqchl:
                        for iii in range(1,7):
                            if rongobjs[iii].rqmcl>rongobjs[iii].rqchl:
                                iii+=1
                                pass
                            else:
                                break
                        rongobj.rqjjx=iii
                    else:
                        for iii in range(1,7):
                            if rongobjs[iii].rqmcl<rongobjs[iii].rqchl:
                                iii+=1
                                pass
                            else:
                                break
                        rongobj.rqjjx=-iii
                    rongobj.save()
            i.liangrong=True
            i.save()
            changdu=len(appendlist)
            print(i.date,'两融已经更新,已更新：',changdu,'条数据')
            togmail.send(to='254370469@qq.com',title=str(i.date)+'两融已更新',content=f'已更新{changdu}条')
        time.sleep(60)
