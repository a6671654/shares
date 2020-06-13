from django.shortcuts import render,HttpResponse,redirect
from .models import *
from login.models import *
from django.core import serializers
import datetime
from django.db.models import F
import json
import redis
# Create your views here.
def index(request):
    allday=Jiaoyiday.objects.all()
    newday=allday.last()
    if newday.isover == False:
        newdayid=newday.id-1
        while newdayid>1:
            try:
                newday=Jiaoyiday.objects.get(id=newdayid)
                break
            except:
                newdayid=newdayid-1
    zd={}
    zd['newday']=newday
    zd['allday']=serializers.serialize('json',allday)
    if request.session.get('is_login',None):
        zd['username']=request.session.get('username')
        zd['celielist']=usercelve.objects.filter(user__name=zd['username'])
    return render(request,'index.html',zd)

def clchaxun(request):
    if request.method == 'POST':
        print(request.POST)
        return render(request,'shuoming.html')
    return redirect('/')
def chaxun(request):
    if request.method == 'POST':
        zd={}
        all_post = request.POST
        all_keys = all_post.keys()
        if len(all_keys) > 2:
            all_keys=list(all_keys)[2:]
            zd['chaxun']=1
            zd['jieguo'],zd['allname'] = chulishuju(all_post,all_keys)
            zd['jieguo']=zd['jieguo'][:50]
            allday = Jiaoyiday.objects.all()
            newday = allday.last()
            zd['allday'] = serializers.serialize('json',allday)
            zd['newday'] = newday
            zd['nowtime'] = all_post['newtime']
            if request.session.get('is_login', None):
                zd['username'] = request.session.get('username')
            return render(request,'index.html',zd)
        return redirect('/')
    return redirect('/')

def shuoming(request):
    return render(request,'shuoming.html')

def chuchun(request):
    if request.method=='POST':
        username=request.session.get('username',None)
        if username:
            name=request.POST.get('name',None)
            celielist=[]
            celiename=[]
            for i in request.POST.keys():
                if i[:4]=='data':
                    celielist.append(i[5:-1])
                    celiename.append(request.POST[i])
            alljg='|'.join(celielist)
            allname='|'.join(celiename)
            celie=Celve.objects.get_or_create(clcode=alljg,defaults={'clname':allname,'last_time':datetime.datetime.now()})
            userbianliang=Alluser.objects.get(name=username)
            usercelve.objects.create(user=userbianliang,celve=celie[0],clname=name)
            return HttpResponse(f'\'{name}\'策略保存成功')
    return HttpResponse('发生错误')




kline_list={'1-1','1-2','1-3','1-4','1-5','1-6','1-7','1-8','1-9','3-3','3-4','4-3','4-4','5-1','5-2','5-3','5-4',}
kline_set={'1-1':'''.filter(day5__gt=F('day10'))''','1-2':'''.filter(day5__gt=F('day20'))''','1-3':'''.filter(day10__gt=F('day20'))''',
           '1-4':'''.filter(low__gt=F('day5'))''','1-5':'''.filter(low__gt=F('day10'))''','1-6':'''.filter(low__gt=F('day20'))''',
           '1-7':'''.filter(high__lt=F('day5'))''','1-8':'''.filter(high__lt=F('day10'))''','1-9':'''.filter(high__lt=F('day20'))''',
           '3-3':'''.filter(hist__gt=0)''','3-4':'''.filter(hist__lt=0)''','4-3':'''.filter(kdjD__gt=80)''','4-4':'''.filter(kdjD__lt=20)''',
           '5-1':'''.filter(close__gt=F('middle')).filter(open__lt=F('middle'))''','5-2':'''.filter(close__lt=F('middle')).filter(open__gt=F('middle'))''',
           '5-3':'''.filter(low__gt=F('middle'))''','5-4':'''.filter(high__lt=F('middle'))''',
           }

jisuan_list={'1-10','1-11','1-12','1-13','1-14','1-15','2-1','2-2','2-3','3-1','3-2','4-1','4-2',}
jisuan_set={'1-10':'''.filter(day5to10=True)''','1-11':'''.filter(day5to20=True)''','1-12':'''.filter(day10to20=True)''',
            '1-13':'''.filter(day5to10=False)''','1-14':'''.filter(day5to20=False)''','1-15':'''.filter(day10to20=False)''',
            '2-1':'''.filter(buynumtwo=True)''','2-2':'''.filter(buynum5=True)''','2-3':'''.filter(buynum20=True)''',
             '3-1':'''.filter(MACD=True)''','3-2':'''.filter(MACD=False)''','4-1':'''.filter(KDJ=True)''',
            '4-2':'''.filter(KDJ=False)''',
            }


def chulishuju(all_post,all_keys):
    newtime=all_post['newtime']
    newtime=newtime.replace('年','-').replace('月','-').replace('日','')
    all_keys=set(all_keys)

    kline_try = list(all_keys & kline_list)
    jisuan_try = list(all_keys & jisuan_list)
    all_name=[all_post[i] for i in kline_try]+[all_post[i] for i in jisuan_try]
    kline_jieguo = kline.objects.filter(date__date=newtime)
    if len(kline_try)>0:
        for i in kline_try:
            kline_jieguo=eval('''kline_jieguo'''+kline_set[i])
        if len(jisuan_try)>0:
            jisuan_jieguo = jisuan.objects.filter(date__date=newtime)
            for i in jisuan_try:
                jisuan_jieguo = eval('''jisuan_jieguo''' + jisuan_set[i])
            jisuan1 = jisuan_jieguo.values('code')
            kline_jieguo = kline_jieguo.filter(code__id__in=jisuan1)
        return kline_jieguo,all_name
    elif len(jisuan_try)>0:
        jisuan_jieguo = jisuan.objects.filter(date__date=newtime)
        for i in jisuan_try:
            jisuan_jieguo = eval('''jisuan_jieguo''' + jisuan_set[i])
        jisuan1 = jisuan_jieguo.values('code')
        kline_jieguo = kline_jieguo.filter(code__id__in=jisuan1)
        return kline_jieguo, all_name
