from django.shortcuts import render,HttpResponse,redirect
from . import models
from django.core import serializers
from django.db.models import F
import json
import redis
# Create your views here.
def index(request):
    allday=models.Jiaoyiday.objects.all()
    newday=allday.last()
    if newday.isover == False:
        newdayid=newday.id-1
        while newdayid>1:
            try:
                newday=models.Jiaoyiday.objects.get(id=newdayid)
                break
            except:
                newdayid=newdayid-1
    zd={}
    zd['newday']=newday
    zd['allday']=serializers.serialize('json',allday)
    return render(request,'index.html',zd)


def chaxun(request):
    if request.method == 'POST':
        zd={}
        all_post = request.POST
        all_keys = all_post.keys()
        if len(all_keys) > 2:
            all_keys=list(all_keys)[2:]
            zd['chaxun']=1
            zd['jieguo'],zd['allname'] = chulishuju(all_post,all_keys)
            allday = models.Jiaoyiday.objects.all()
            newday = allday.last()
            zd['allday'] = serializers.serialize('json',allday)
            zd['newday'] = newday
            zd['nowtime'] = all_post['newtime']
            return render(request,'index.html',zd)
        return redirect('/')
    return redirect('/')

def shuoming(requeset):
    return render(requeset,'shuoming.html')



kline_list={'chekc-1-1','chekc-1-2','chekc-1-3','chekc-1-4','chekc-1-5','chekc-1-6','chekc-1-7','chekc-1-8','chekc-1-9',
            'chekc-3-3','chekc-3-4','chekc-4-3','chekc-4-4','chekc-5-1','chekc-5-2','chekc-5-3','chekc-5-4',}
kline_set={'chekc-1-1':'''.filter(day5__gt=F('day10'))''','chekc-1-2':'''.filter(day5__gt=F('day20'))''','chekc-1-3':'''.filter(day10__gt=F('day20'))''',
           'chekc-1-4':'''.filter(low__gt=F('day5'))''','chekc-1-5':'''.filter(low__gt=F('day10'))''','chekc-1-6':'''.filter(low__gt=F('day20'))''',
           'chekc-1-7':'''.filter(high__lt=F('day5'))''','chekc-1-8':'''.filter(high__lt=F('day10'))''','chekc-1-9':'''.filter(high__lt=F('day20'))''',
           'chekc-3-3':'''.filter(hist__gt=0)''','chekc-3-4':'''.filter(hist__lt=0)''','chekc-4-3':'''.filter(kdjD__gt=80)''','chekc-4-4':'''.filter(kdjD__lt=20)''',
           'chekc-5-1':'''.filter(close__gt=F('middle')).filter(open__lt=F('middle'))''','chekc-5-2':'''.filter(close__lt=F('middle')).filter(open__gt=F('middle'))''',
           'chekc-5-3':'''.filter(low__gt=F('middle'))''','chekc-5-4':'''.filter(high__lt=F('middle'))''',
           }

jisuan_list={'chekc-1-10','chekc-1-11','chekc-1-12','chekc-1-13','chekc-1-14','chekc-1-15','chekc-2-1','chekc-2-2','chekc-2-3',
             'chekc-3-1','chekc-3-2','chekc-4-1','chekc-4-2',}
jisuan_set={'chekc-1-10':'''.filter(day5to10=True)''','chekc-1-11':'''.filter(day5to20=True)''','chekc-1-12':'''.filter(day10to20=True)''',
            'chekc-1-13':'''.filter(day5to10=False)''','chekc-1-14':'''.filter(day5to20=False)''','chekc-1-15':'''.filter(day10to20=False)''',
            'chekc-2-1':'''.filter(buynumtwo=True)''','chekc-2-2':'''.filter(buynum5=True)''','chekc-2-3':'''.filter(buynum20=True)''',
             'chekc-3-1':'''.filter(MACD=True)''','chekc-3-2':'''.filter(MACD=False)''','chekc-4-1':'''.filter(KDJ=True)''',
            'chekc-4-2':'''.filter(KDJ=False)''',
            }


def chulishuju(all_post,all_keys):
    newtime=all_post['newtime']
    newtime=newtime.replace('年','-').replace('月','-').replace('日','')
    all_keys=set(all_keys)

    kline_try = list(all_keys & kline_list)
    jisuan_try = list(all_keys & jisuan_list)
    all_name=[all_post[i] for i in kline_try]+[all_post[i] for i in jisuan_try]
    kline_jieguo = models.kline.objects.filter(date__date=newtime)
    if len(kline_try)>0:
        for i in kline_try:
            kline_jieguo=eval('''kline_jieguo'''+kline_set[i])
        if len(jisuan_try)>0:
            jisuan_jieguo = models.jisuan.objects.filter(date__date=newtime)
            for i in jisuan_try:
                jisuan_jieguo = eval('''jisuan_jieguo''' + jisuan_set[i])
                jisuan = jisuan_jieguo.values('code')
                kline_jieguo = kline_jieguo.filter(code__id__in=jisuan)
        return kline_jieguo,all_name
    elif len(jisuan_try)>0:
        jisuan_jieguo = models.jisuan.objects.filter(date__date=newtime)
        for i in jisuan_try:
            jisuan_jieguo = eval('''jisuan_jieguo''' + jisuan_set[i])
            jisuan = jisuan_jieguo.values('code')
            kline_jieguo = kline_jieguo.filter(code__id__in=jisuan)
        return kline_jieguo, all_name


def chulishuju1(all_post,all_keys):
    newtime=all_post['newtime']
    newtime=newtime.replace('年','-').replace('月','-').replace('日','')
    all_keys=set(all_keys)

    kline_try = list(all_keys & kline_list)
    jisuan_try = list(all_keys & jisuan_list)
    all_name=[all_post[i] for i in kline_try]+[all_post[i] for i in jisuan_try]
    if len(kline_try)>0:
        kline_jieguo = models.kline.objects.filter(date__date=newtime)
        for i in kline_try:
            kline_jieguo=eval('''kline_jieguo'''+kline_set[i])
        kline=kline_jieguo.values('code')
        if len(jisuan_try)>0:
            jisuan_jieguo = models.jisuan.objects.filter(date__date=newtime)
            for i in jisuan_try:
                jisuan_jieguo = eval('''jisuan_jieguo''' + jisuan_set[i])
            jisuan = jisuan_jieguo.values('code')
            jiaoji=kline.intersection(jisuan)
            a = models.Gupiaolist.objects.filter(id__in=jiaoji)
            return a,all_name
        else:
            a = models.Gupiaolist.objects.filter(id__in=kline)
            return a,all_name
    elif len(jisuan_try)>0:
        jisuan_jieguo = models.jisuan.objects.filter(date__date=newtime)
        for i in jisuan_try:
            jisuan_jieguo = eval('''jisuan_jieguo''' + jisuan_set[i])
        jisuan = jisuan_jieguo.values('code')
        a = models.Gupiaolist.objects.filter(id__in=jisuan)
        return a,all_name

