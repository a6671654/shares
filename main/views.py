from django.shortcuts import render,HttpResponse,redirect
from .models import *
from login.models import *
from django.core import serializers
import datetime
import time
from django.db.models import F,Q
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
    zd['allday']=serializers.serialize('json',allday[2:])
    if request.session.get('is_login',None):
        zd['username']=request.session.get('username')
        zd['celielist']=usercelve.objects.filter(user__name=zd['username']).filter(shanchu=True)
    return render(request,'index.html',zd)

def clchaxun(request):
    if request.method == 'POST':
        if request.session.get('is_login', None):
            if request.session.get('last_time',time.time()-6)+5>time.time():
               return HttpResponse('为保值网站正常运行，每5秒只能查询一次')
            request.session['last_time']=time.time()
            zd={}
            clcode=request.POST['clcode']
            clname=request.POST['clname']
            clid=request.POST['clid']
            clobj=usercelve.objects.get(id=clid)
            clobj.nums+=1
            clobj.save()
            all_post={}
            all_keys=clcode.split('|')
            clname=clname.split('|')
            all_post['newtime']=request.POST['nowtime']
            for i in range(len(clname)):
                all_post[all_keys[i]]=clname[i]
            zd['chaxun'] = 1
            zd['jieguo'],zd['allname'] = chulishuju(all_post,all_keys)
            zd['jieguo']=zd['jieguo'][:50]
            zd['nowtime'] = all_post['newtime']
            return render(request,'jieguo.html',zd)
    return HttpResponse('登入超时')


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
            zd['allday'] = serializers.serialize('json',allday[2:])
            zd['newday'] = newday
            zd['nowtime'] = all_post['newtime']
            if request.session.get('is_login', None):
                zd['username'] = request.session.get('username')
                zd['celielist'] = usercelve.objects.filter(user__name=zd['username']).filter(shanchu=True)
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
            usercelve.objects.create(user=userbianliang,celve=celie[0],clname=name,shanchu=True)
            return HttpResponse(f'\'{name}\'策略保存成功')
    return HttpResponse('发生错误')

klined2_list={'d2-1-1','d2-1-2','d2-1-3','d2-1-4','d2-1-5','d2-1-6','d2-1-7','d2-1-8','d2-1-9','d2-1-10','d2-1-11',
             'd2-1-12','d2-1-13','d2-1-14','d2-1-15','d2-1-16','d2-1-17'}

klined1_list={'d1-1-1','d1-1-2','d1-1-3','d1-1-4','d1-1-5','d1-1-6','d1-1-7','d1-1-8','d1-1-9','d1-1-10','d1-1-11',
             'd1-1-12','d1-1-13','d1-1-14','d1-1-15','d1-1-16','d1-1-17'}

kline_list={'1-1','1-2','1-3','1-4','1-5','1-6','1-7','1-8','1-9','1-10','1-11','1-12','1-13','1-14','1-15','1-16','1-17',
            '2-1','2-2','2-3','2-16','2-17','2-18','2-4','2-5','2-6','2-7','2-8','2-9',
            '4-3','4-4',
            '5-3','5-4','5-5','5-6','5-7','5-8',
            '6-1','6-3','6-4','6-5','6-6',
            '7-1','7-2','7-3','7-4','7-5','7-6','7-7','7-8','7-9','7-10'}
kline_set={'1-1':'''.filter(close__gt=F('preclose'))''','1-2':'''.filter(close__lt=F('preclose'))''','1-3':'''.filter(open__lt=F('close'))''',
            '1-4':'''.filter(open__gt=F('close'))''','1-5':'''.filter(open__gt=F('preclose'))''','1-6':'''.filter(open__lt=F('preclose'))''',
            '1-7':'''.filter(close__gt=F('open')*1.07)''','1-8':'''.filter(close__gt=F('open')*1.03).filter(close__lt=F('open')*1.07)''',
            '1-9':'''.filter(close__gt=F('open')*1.01).filter(close__lt=F('open')*1.03)''','1-10':'''.filter(close__lt=F('open')*0.93)''',
            '1-11':'''.filter(close__lt=F('open')*0.97).filter(close__gt=F('open')*0.93)''','1-12':'''.filter(close__lt=F('open')*0.99).filter(close__gt=F('open')*0.93)''',
            '1-13':'''.filter(high=F('close')).filter(open__lt=F('close'))''','1-14':'''.filter(low=F('open')).filter(close__gt=F('open'))''',
            '1-15':'''.filter(high=F('open')).filter(open__gt=F('close'))''','1-16':'''.filter(close=F('low')).filter(open__gt=F('close'))''',
            '1-17':'''.filter(close=F('open')).filter(high__gt=F('low'))''',
            '2-1':'''.filter(day5__gt=F('day10'))''','2-2':'''.filter(day5__gt=F('day20'))''','2-3':'''.filter(day10__gt=F('day20'))''',
            '2-16':'''.filter(day5__lt=F('day10'))''','2-17':'''.filter(day5__lt=F('day20'))''','2-18':'''.filter(day10__lt=F('day20'))''',
            '2-4':'''.filter(low__gt=F('day5'))''','2-5':'''.filter(low__gt=F('day10'))''','2-6':'''.filter(low__gt=F('day20'))''',
            '2-7':'''.filter(high__lt=F('day5'))''','2-8':'''.filter(high__lt=F('day10'))''','2-9':'''.filter(high__lt=F('day20'))''',
            '4-3':'''.filter(hist__gt=0)''','4-4':'''.filter(hist__lt=0)''',
            '5-3':'''.filter(kdjD__gt=80)''','5-4':'''.filter(kdjD__lt=20)''','5-5':'''.filter(kdjD__gt=50)''','5-6':'''.filter(kdjD__lt=50)''',
            '5-7':'''.filter(kdjK__gt=F('kdjJ'))''','5-8':'''.filter(kdjK__lt=F('kdjJ'))''',
            '6-1':'''.filter(high__gt=F('middle')).filter(low__lt=F('middle'))''','6-3':'''.filter(low__gt=F('middle'))''',
            '6-4':'''.filter(high__lt=F('middle'))''','6-5':'''.filter(low__lt=F('upper')).filter(high__gt=F('upper'))''',
            '6-6':'''.filter(low__lt=F('lower')).filter(high__gt=F('lower'))''',
            '7-1':'''.filter(turn__lt=0.5)''','7-2':'''.filter(turn__gt=0.5)''','7-3':'''.filter(turn__lt=1)''','7-4':'''.filter(turn__gt=1)''',
            '7-5':'''.filter(turn__lt=3)''','7-6':'''.filter(turn__gt=3)''',
            '7-7':'''.filter(turn__lt=7)''','7-8':'''.filter(turn__gt=7)''','7-9':'''.filter(turn__lt=10)''','7-10':'''.filter(turn__gt=10)''',
            }


jisuan_list={'2-10','2-11','2-12','2-13','2-14','2-15','2-19','2-20','2-21',
             '3-1','3-2','3-3','3-4','3-5','3-6','3-7','3-8','3-9','3-10','3-11','3-12','3-13','3-14',
             '4-1','4-2','4-5','4-6','4-7','4-8','4-9','4-10','4-11','4-12','4-13','4-14','4-15','4-16',
             '5-1','5-2',
             '6-7','6-8','6-9','6-10'
             }
jisuan_set={'2-10':'''.filter(day5to10=True)''','2-11':'''.filter(day5to20=True)''','2-12':'''.filter(day10to20=True)''',
            '2-13':'''.filter(day5to10=False)''','2-14':'''.filter(day5to20=False)''','2-15':'''.filter(day10to20=False)''',
            '2-19':'''.filter(day5keep5=True)''','2-20':'''.filter(day5keep10=True)''','2-21':'''.filter(day5keep20=True)''',
            '3-1':'''.filter(buynumtwo=True)''','3-2':'''.filter(buynumtwo=False)''','3-3':'''.filter(buynum5=True)''',
            '3-4':'''.filter(buynum5=False)''','3-5':'''.filter(buynum20=True)''','3-6':'''.filter(buynum20=False)''',
            '3-7':'''.filter(buynum3up=True)''','3-8':'''.filter(buynum3up=False)''','3-9':'''.filter(buynum5up=True)''',
            '3-10':'''.filter(buynum5up=False)''','3-11':'''.filter(buynum3chang=True)''','3-12':'''.filter(buynum3chang=False)''',
            '3-13':'''.filter(buynum5chang=True)''','3-14':'''.filter(buynum5chang=False)''',
            '4-1':'''.filter(MACD=True)''','4-2':'''.filter(MACD=False)''','4-5':'''.filter(MACD3up=True)''','4-6':'''.filter(MACD3up=False)''',
            '4-7':'''.filter(MACD5up=True)''','4-8':'''.filter(MACD5up=False)''','4-9':'''.filter(MACD3chang=True)''',
            '4-10':'''.filter(MACD3chang=False)''','4-11':'''.filter(MACD3chang2=True)''','4-12':'''.filter(MACD3chang2=False)''',
            '4-13':'''.filter(MACD5chang=True)''','4-14':'''.filter(MACD5chang=False)''','4-15':'''.filter(MACD5chang2=True)''',
            '4-16':'''.filter(MACD5chang2=False)''',
            '5-1':'''.filter(KDJ=True)''','5-2':'''.filter(KDJ=False)''',
            '6-7':'''.filter(BOLL3big=False)''','6-8':'''.filter(BOLL3big=True)''','6-9':'''.filter(BOLL5big=False)''','6-10':'''.filter(BOLL5big=True)''',
            }


def chulishuju(all_post,all_keys):
    newtime=all_post['newtime']
    newtime=newtime.replace('年','-').replace('月','-').replace('日','')
    all_keys=set(all_keys)
    kline_try = list(all_keys & kline_list)
    jisuan_try = list(all_keys & jisuan_list)
    klined1_try = list(all_keys & klined1_list)
    klined2_try = list(all_keys & klined2_list)
    all_name=[all_post[i] for i in kline_try]+[all_post[i] for i in jisuan_try]+[all_post[i] for i in klined1_try]+[all_post[i] for i in klined2_try]
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
    if len(klined1_try)>0:
        lastday=Jiaoyiday.objects.get(date=newtime)
        klined1_jieguo = kline.objects.filter(date=lastday.id-1)
        for i in klined1_try:
            klined1_jieguo = eval('''klined1_jieguo'''+kline_set[i[3:]])
        jisuan2 = klined1_jieguo.values('code')
        kline_jieguo = kline_jieguo.filter(code__id__in=jisuan2)
    if len(klined2_try)>0:
        lastday=Jiaoyiday.objects.get(date=newtime)
        klined1_jieguo = kline.objects.filter(date=lastday.id-2)
        for i in klined2_try:
            klined1_jieguo = eval('''klined1_jieguo'''+kline_set[i[3:]])
        jisuan2 = klined1_jieguo.values('code')
        kline_jieguo = kline_jieguo.filter(code__id__in=jisuan2)
    return kline_jieguo,all_name
