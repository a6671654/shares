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
    allday=Jiaoyiday.objects.all().filter(isover=True)
    newday=allday.last()
    zd={}
    zd['newday']=newday
    zd['rongday']=allday.filter(liangrong=True).last()
    zd['allday']=serializers.serialize('json',allday[2:])
    if request.session.get('is_login',None):
        zd['username']=request.session.get('username')
        zd['celielist']=usercelve.objects.filter(user__name=zd['username']).filter(shanchu=True)
    return render(request,'index.html',zd)

def riqi(request):
    zd={}
    allday = Jiaoyiday.objects.all().filter(isover=True)
    zd['rongday'] = allday.filter(liangrong=True).last()
    newday = allday.last()
    zd['newday'] = newday
    zd['allday'] = allday.order_by('-id')[:25]
    if request.session.get('is_login', None):
        zd['username'] = request.session.get('username')
        zd['celielist'] = usercelve.objects.filter(user__name=zd['username']).filter(shanchu=True)
    return render(request,'riqi.html',zd)

def riqicx(request):
    zd={}
    if request.method=='POST':
        if request.session.get('is_login', None):
            if request.session.get('last_time',time.time()-6)+5>time.time():
               return HttpResponse('为保值网站正常运行，每5秒只能查询一次')
            request.session['last_time']=time.time()
            username=request.session.get('username')
            allpost = request.POST
            day1=allpost['day1']
            tj1=allpost['tj1']
            day2=allpost['day2']
            tj2=allpost['tj2']
            xsday=allpost['xsday']
            jieguo=Kline.objects.filter(date__date=xsday)
            daylist=[]
            if tj1 != '请选择':
                obj=usercelve.objects.get(id=tj1)
                if obj.user.name==username:
                    allkeys=obj.celve.clcode.split('|')
                    newtime=day1
                    lsjieguo=chulishuju2(newtime,allkeys)
                    lsjieguo=lsjieguo.values('code')
                    jieguo = jieguo.filter(code__id__in=lsjieguo)
                    daylist.append(newtime+' : '+obj.celve.clname)
            if day2 !='请选择' and tj2 != '请选择':
                obj = usercelve.objects.get(id=tj2)
                if obj.user.name == username:
                    allkeys=obj.celve.clcode.split('|')
                    newtime=day2
                    lsjieguo=chulishuju2(newtime,allkeys)
                    lsjieguo=lsjieguo.values('code')
                    jieguo = jieguo.filter(code__id__in=lsjieguo)
                    daylist.append(newtime + ':' + obj.celve.clname)
            if len(daylist)==0:
                return HttpResponse('至少选择一个条件和日期')
            try:
                zd['tablelist'] = Ziliao.objects.get(user__name=username).xianshi
                if zd['tablelist']:
                    zd['tablelist'] = zd['tablelist'].split('|')
            except:
                pass
            zd['lenjieguo']=len(jieguo)
            zd['jieguo']=jieguo[:100]
            zd['nowtime']=xsday
            zd['daylist']=daylist
            return render(request, 'riqijg.html', zd)
    return HttpResponse('错误')

def celve(request):
    if request.method == 'POST':
        if request.session.get('is_login', None):
            caozuo=request.POST['caozuo']#获取操作名称
            if caozuo=='moren':
                morenzd={}
                for i in request.POST.keys():
                    if i[:4]=='data':
                        morenzd[i[5:-1]]=request.POST[i]
                morenlist=[]
                shujuobj=Allshujuname.objects.all()
                for i in morenzd:
                    if shujuobj.get(id=i).name==morenzd[i]:
                        morenlist.append(morenzd[i])
                userojb=Alluser.objects.get(name=request.session.get('username'))
                if len(morenlist)<=6:
                    morenlist='|'.join(morenlist)
                    Ziliao.objects.update_or_create(user=userojb,defaults={'xianshi':morenlist})
                    if morenlist=='':
                        return HttpResponse('未选择，恢复系统默认')
                    return HttpResponse('修改成功')
                return HttpResponse('修改失败')
            clid=request.POST['celveid']
            usecl=usercelve.objects.get(id=clid)
            if request.session.get('username') == usecl.user.name:
                if caozuo=='shanchu':
                    if usecl.nums<5:
                        usecl.delete()
                    else:
                        usecl.shanchu=False
                        usecl.save()
                    return HttpResponse('删除成功')
                elif caozuo=='xiugai':
                    newname=request.POST['name']
                    usecl.clname=newname
                    usecl.save()
                    return HttpResponse('修改成功')
        return HttpResponse('请重新登入')
    zd={}
    if request.session.get('is_login',None):
        zd['username']=request.session.get('username')
        allcelve=usercelve.objects.filter(user__name=zd['username']).filter(shanchu=True)
        zd['allcelve']=allcelve
        zd['moren']= Ziliao.objects.filter(user__name=zd['username'])
        zd['allshuju'] = Allshujuname.objects.all()
    return  render(request,'celve.html',zd)

def clchaxun(request):
    if request.method == 'POST':
        if request.session.get('is_login', None):
            if request.session.get('last_time',time.time()-6)+3>time.time():
               return HttpResponse('为保值网站正常运行，每3秒只能查询一次')
            request.session['last_time']=time.time()
            zd={}
            clcode=request.POST['clcode']
            clname=request.POST['clname']
            clid=request.POST['clid']
            clobj=usercelve.objects.get(id=clid)
            if clobj.user.name != request.session['username']:
                return HttpResponse('发送错误')
            clobj.nums+=1
            clobj.last_time=datetime.datetime.now()
            clobj.save()
            all_post={}
            all_keys=clcode.split('|')
            clname=clname.split('|')
            all_post['newtime']=request.POST['nowtime']
            for i in range(len(clname)):
                all_post[all_keys[i]]=clname[i]
            if clobj.xianshi:
                zd['tablelist']=clobj.xianshi.split('|')
            else:
                try:
                    zd['tablelist'] = Ziliao.objects.get(user__name=clobj.user.name).xianshi
                    if zd['tablelist']:
                        zd['tablelist'] = zd['tablelist'].split('|')
                except:
                    pass
            zd['chaxun'] = 1
            zd['jieguo'],zd['allname'] = chulishuju(all_post,all_keys)
            zd['lenjieguo']=len(zd['jieguo'])
            zd['jieguo']=zd['jieguo'][:100]
            zd['nowtime'] = all_post['newtime']
            conn = redis.Redis(host='127.0.0.1', port='6379',decode_responses=True)
            conn.incr(datetime.datetime.now().strftime('%Y-%m-%d'))
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
            zd['lenjieguo']=len(zd['jieguo'])
            zd['jieguo']=zd['jieguo'][:100]
            allday = Jiaoyiday.objects.all().filter(isover=True)
            newday = allday.last()
            zd['allday'] = serializers.serialize('json',allday[2:])
            zd['newday'] = newday
            zd['nowtime'] = all_post['newtime']
            if request.session.get('is_login', None):
                zd['username'] = request.session.get('username')
                zd['celielist'] = usercelve.objects.filter(user__name=zd['username']).filter(shanchu=True)
                try:
                    zd['tablelist'] = Ziliao.objects.get(user__name=zd['username']).xianshi
                    if zd['tablelist']:
                        zd['tablelist'] = zd['tablelist'].split('|')
                except:
                    pass
            conn = redis.Redis(host='127.0.0.1', port='6379',decode_responses=True)
            conn.incr(datetime.datetime.now().strftime('%Y-%m-%d'))
            return render(request,'index.html',zd)
        return redirect('/')
    return redirect('/')

def shuoming(request):
    zd={}
    if request.session.get('is_login', None):
        zd['username'] = request.session.get('username')
    return render(request,'shuoming.html',zd)
def update(request):
    zd={}
    zd['update'] = Update.objects.all().order_by('-updateday')
    if request.session.get('is_login', None):
        zd['username'] = request.session.get('username')
    return render(request,'update.html',zd)


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
            '7-1','7-2','7-3','7-4','7-5','7-6','7-7','7-8','7-9','7-10',
            '8-1-1','8-1-2','8-1-3','8-1-4','8-1-5','8-1-6','8-1-7','8-1-8','8-1-9','8-1-10','8-1-11','8-1-12',
            '8-2-1','8-2-2','8-2-3','8-2-4','8-2-5','8-2-6','8-2-7','8-2-8','8-2-9','8-2-10','8-2-11','8-2-12',
            '8-3-1','8-3-2','8-3-3','8-3-4','8-3-5','8-3-6','8-3-7','8-3-8','8-3-9','8-3-10','8-3-11','8-3-12',
            '9-1', '9-2', '9-3', '9-4', '9-5', '9-6', '9-7', '9-8', '9-9', '9-10',
            '10-1','10-2','10-3','10-4','10-5','10-6','10-7','10-8','10-9','10-10',
            '10-11','10-12','10-13','10-14','10-15','10-16','10-17','10-18','10-19','10-20',
            '10-21','10-22','10-23','10-24','10-25','10-26','10-27','10-28',
            }
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
            '8-1-1':'''.filter(pe__lt=5)''','8-1-2':'''.filter(pe__gt=5)''','8-1-3':'''.filter(pe__lt=13)''','8-1-4':'''.filter(pe__gt=13)''',
            '8-1-5':'''.filter(pe__lt=20)''','8-1-6':'''.filter(pe__gt=20)''','8-1-7':'''.filter(pe__lt=28)''','8-1-8':'''.filter(pe__gt=28)''',
            '8-1-9':'''.filter(pe__lt=40)''','8-1-10':'''.filter(pe__gt=40)''','8-1-11':'''.filter(pe__lt=80)''','8-1-12':'''.filter(pe__gt=80)''',
            '8-2-1':'''.filter(pb__lt=1)''','8-2-2':'''.filter(pb__gt=1)''','8-2-3':'''.filter(pb__lt=1.5)''','8-2-4':'''.filter(pb__gt=1.5)''',
            '8-2-5':'''.filter(pb__lt=2)''','8-2-6':'''.filter(pb__gt=2)''','8-2-7':'''.filter(pb__lt=3)''','8-2-8':'''.filter(pb__gt=3)''',
            '8-2-9':'''.filter(pb__lt=5)''','8-2-10':'''.filter(pb__gt=5)''','8-2-11':'''.filter(pb__lt=10)''','8-2-12':'''.filter(pb__gt=10)''',
            '8-3-1':'''.filter(ps__lt=0.5)''','8-3-2':'''.filter(ps__gt=0.5)''','8-3-3':'''.filter(ps__lt=1)''','8-3-4':'''.filter(ps__gt=1)''',
            '8-3-5':'''.filter(ps__lt=2)''','8-3-6':'''.filter(ps__gt=2)''','8-3-7':'''.filter(ps__lt=3)''','8-3-8':'''.filter(ps__gt=3)''',
            '8-3-9':'''.filter(ps__lt=5)''','8-3-10':'''.filter(ps__gt=5)''','8-3-11':'''.filter(ps__lt=10)''','8-3-12':'''.filter(ps__gt=10)''',
            '9-1':'''.filter(circ_mv__lt=120000)''','9-2':'''.filter(circ_mv__gt=120000)''','9-3':'''.filter(circ_mv__lt=200000)''',
            '9-4':'''.filter(circ_mv__gt=200000)''','9-5':'''.filter(circ_mv__lt=500000)''','9-6':'''.filter(circ_mv__gt=500000)''',
            '9-7':'''.filter(circ_mv__lt=1000000)''','9-8':'''.filter(circ_mv__gt=1000000)''','9-9':'''.filter(circ_mv__lt=3000000)''',
            '9-10':'''.filter(circ_mv__gt=3000000)''',
            '10-1':'''.filter(liangrong__rzye__lt=F('circ_mv')*100)''','10-2':'''.filter(liangrong__rzye__gt=F('circ_mv')*100)''',
            '10-3':'''.filter(liangrong__rzye__lt=F('circ_mv')*300)''','10-4':'''.filter(liangrong__rzye__gt=F('circ_mv')*300)''',
            '10-5':'''.filter(liangrong__rzye__lt=F('circ_mv')*500)''','10-6':'''.filter(liangrong__rzye__gt=F('circ_mv')*500)''',
            '10-7':'''.filter(liangrong__rzye__lt=F('circ_mv')*700)''','10-8':'''.filter(liangrong__rzye__gt=F('circ_mv')*700)''',
            '10-9':'''.filter(liangrong__rzye__lt=F('circ_mv')*1000)''','10-10':'''.filter(liangrong__rzye__gt=F('circ_mv')*1000)''',
            '10-11':'''.filter(circ_mv__gt=(F('liangrong__rzmre')-F('liangrong__rzche'))*10000/10000).filter(liangrong__rzmre__gt=F('liangrong__rzche'))''',
            '10-12':'''.filter(circ_mv__lt=(F('liangrong__rzmre')-F('liangrong__rzche'))*10000/10000).filter(liangrong__rzmre__gt=F('liangrong__rzche'))''',
            '10-13':'''.filter(circ_mv__gt=(F('liangrong__rzmre')-F('liangrong__rzche'))*2000/10000).filter(liangrong__rzmre__gt=F('liangrong__rzche'))''',
            '10-14':'''.filter(circ_mv__lt=(F('liangrong__rzmre')-F('liangrong__rzche'))*2000/10000).filter(liangrong__rzmre__gt=F('liangrong__rzche'))''',
            '10-15':'''.filter(circ_mv__gt=(F('liangrong__rzmre')-F('liangrong__rzche'))*1000/10000).filter(liangrong__rzmre__gt=F('liangrong__rzche'))''',
            '10-16':'''.filter(circ_mv__lt=(F('liangrong__rzmre')-F('liangrong__rzche'))*1000/10000).filter(liangrong__rzmre__gt=F('liangrong__rzche'))''',
            '10-17':'''.filter(circ_mv__gt=(F('liangrong__rzmre')-F('liangrong__rzche'))*200/10000).filter(liangrong__rzmre__gt=F('liangrong__rzche'))''',
            '10-18':'''.filter(circ_mv__lt=(F('liangrong__rzmre')-F('liangrong__rzche'))*200/10000).filter(liangrong__rzmre__gt=F('liangrong__rzche'))''',
            '10-19':'''.filter(circ_mv__gt=(F('liangrong__rzmre')-F('liangrong__rzche'))*100/10000).filter(liangrong__rzmre__gt=F('liangrong__rzche'))''',
            '10-20':'''.filter(circ_mv__lt=(F('liangrong__rzmre')-F('liangrong__rzche'))*100/10000).filter(liangrong__rzmre__gt=F('liangrong__rzche'))''',
            '10-21':'''.filter(liangrong__rzjzz__gt=2)''','10-22':'''.filter(liangrong__rzjzz__lt=-2)''','10-23':'''.filter(liangrong__rzjzz__gt=4)''',
            '10-24':'''.filter(liangrong__rzjzz__lt=-4)''','10-25':'''.filter(liangrong__rqjjx__gt=2)''','10-26':'''.filter(liangrong__rqjjx__lt=-2)''',
            '10-27':'''.filter(liangrong__rqjjx__gt=4)''','10-28':'''.filter(liangrong__rqjjx__lt=-4)'''
            }


jisuan_list={'1-18','1-19','1-20','1-21','1-22','1-23','1-24','1-25','1-26','1-27','1-28','1-29',
             '2-10','2-11','2-12','2-13','2-14','2-15','2-19','2-20','2-21',
             '3-1','3-2','3-3','3-4','3-5','3-6','3-7','3-8','3-9','3-10','3-11','3-12','3-13','3-14',
             '4-1','4-2','4-5','4-6','4-7','4-8','4-9','4-10','4-11','4-12','4-13','4-14','4-15','4-16',
             '5-1','5-2',
             '6-7','6-8','6-9','6-10'
             }
jisuan_set={'1-18':'''.filter(jisuan__yang__gt=2)''','1-19':'''.filter(jisuan__yang__gt=4)''','1-20':'''.filter(jisuan__yang__gt=6)''',
            '1-21':'''.filter(jisuan__yang__lt=-2)''','1-22':'''.filter(jisuan__yang__lt=-4)''','1-23':'''.filter(jisuan__yang__lt=-6)''',
            '1-24':'''.filter(jisuan__zhang__gt=2)''','1-25':'''.filter(jisuan__zhang__gt=4)''','1-26':'''.filter(jisuan__zhang__gt=6)''',
            '1-27':'''.filter(jisuan__zhang__lt=-2)''','1-28':'''.filter(jisuan__zhang__lt=-4)''','1-29':'''.filter(jisuan__zhang__lt=-6)''',
            '2-10':'''.filter(jisuan__day5to10=True)''','2-11':'''.filter(jisuan__day5to20=True)''','2-12':'''.filter(jisuan__day10to20=True)''',
            '2-13':'''.filter(jisuan__day5to10=False)''','2-14':'''.filter(jisuan__day5to20=False)''','2-15':'''.filter(jisuan__day10to20=False)''',
            '2-19':'''.filter(jisuan__day5keep5=True)''','2-20':'''.filter(jisuan__day5keep10=True)''','2-21':'''.filter(jisuan__day5keep20=True)''',
            '3-1':'''.filter(jisuan__buynumtwo=True)''','3-2':'''.filter(jisuan__buynumtwo=False)''','3-3':'''.filter(jisuan__buynum5=True)''',
            '3-4':'''.filter(jisuan__buynum5=False)''','3-5':'''.filter(jisuan__buynum20=True)''','3-6':'''.filter(jisuan__buynum20=False)''',
            '3-7':'''.filter(jisuan__buynum3up=True)''','3-8':'''.filter(jisuan__buynum3up=False)''','3-9':'''.filter(jisuan__buynum5up=True)''',
            '3-10':'''.filter(jisuan__buynum5up=False)''','3-11':'''.filter(jisuan__buynum3chang=True)''','3-12':'''.filter(jisuan__buynum3chang=False)''',
            '3-13':'''.filter(jisuan__buynum5chang=True)''','3-14':'''.filter(jisuan__buynum5chang=False)''',
            '4-1':'''.filter(jisuan__MACD=True)''','4-2':'''.filter(jisuan__MACD=False)''','4-5':'''.filter(jisuan__MACD3up=True)''','4-6':'''.filter(jisuan__MACD3up=False)''',
            '4-7':'''.filter(jisuan__MACD5up=True)''','4-8':'''.filter(jisuan__MACD5up=False)''','4-9':'''.filter(jisuan__MACD3chang=True)''',
            '4-10':'''.filter(jisuan__MACD3chang=False)''','4-11':'''.filter(jisuan__MACD3chang2=True)''','4-12':'''.filter(jisuan__MACD3chang2=False)''',
            '4-13':'''.filter(jisuan__MACD5chang=True)''','4-14':'''.filter(jisuan__MACD5chang=False)''','4-15':'''.filter(jisuan__MACD5chang2=True)''',
            '4-16':'''.filter(jisuan__MACD5chang2=False)''',
            '5-1':'''.filter(jisuan__KDJ=True)''','5-2':'''.filter(jisuan__KDJ=False)''',
            '6-7':'''.filter(jisuan__BOLL3big=False)''','6-8':'''.filter(jisuan__BOLL3big=True)''','6-9':'''.filter(jisuan__BOLL5big=False)''','6-10':'''.filter(jisuan__BOLL5big=True)''',
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
    kline_jieguo = Kline.objects.filter(date__date=newtime)
    if len(kline_try)>0:
        for i in kline_try:
            kline_jieguo = eval('''kline_jieguo''' + kline_set[i])
    if len(jisuan_try)>0:
        for i in jisuan_try:
            kline_jieguo = eval('''kline_jieguo''' + jisuan_set[i])
    if len(klined1_try)>0:
        lastday=Jiaoyiday.objects.get(date=newtime)
        klined1_jieguo = Kline.objects.filter(date=lastday.id-1)
        for i in klined1_try:
            klined1_jieguo = eval('''klined1_jieguo'''+kline_set[i[3:]])
        jisuan2 = klined1_jieguo.values('code')
        kline_jieguo = kline_jieguo.filter(code__id__in=jisuan2)
    if len(klined2_try)>0:
        lastday=Jiaoyiday.objects.get(date=newtime)
        klined1_jieguo = Kline.objects.filter(date=lastday.id-2)
        for i in klined2_try:
            klined1_jieguo = eval('''klined1_jieguo'''+kline_set[i[3:]])
        jisuan2 = klined1_jieguo.values('code')
        kline_jieguo = kline_jieguo.filter(code__id__in=jisuan2)
    return kline_jieguo,all_name

def chulishuju2(newtime,all_keys):
    all_keys=set(all_keys)
    kline_try = list(all_keys & kline_list)
    jisuan_try = list(all_keys & jisuan_list)
    klined1_try = list(all_keys & klined1_list)
    klined2_try = list(all_keys & klined2_list)
    kline_jieguo = Kline.objects.filter(date__date=newtime)
    if len(kline_try)>0:
        for i in kline_try:
            kline_jieguo = eval('''kline_jieguo''' + kline_set[i])
    if len(jisuan_try)>0:
        for i in jisuan_try:
            kline_jieguo = eval('''kline_jieguo''' + jisuan_set[i])
    if len(klined1_try)>0:
        lastday=Jiaoyiday.objects.get(date=newtime)
        klined1_jieguo = Kline.objects.filter(date=lastday.id-1)
        for i in klined1_try:
            klined1_jieguo = eval('''klined1_jieguo'''+kline_set[i[3:]])
        jisuan2 = klined1_jieguo.values('code')
        kline_jieguo = kline_jieguo.filter(code__id__in=jisuan2)
    if len(klined2_try)>0:
        lastday=Jiaoyiday.objects.get(date=newtime)
        klined1_jieguo = Kline.objects.filter(date=lastday.id-2)
        for i in klined2_try:
            klined1_jieguo = eval('''klined1_jieguo'''+kline_set[i[3:]])
        jisuan2 = klined1_jieguo.values('code')
        kline_jieguo = kline_jieguo.filter(code__id__in=jisuan2)
    return kline_jieguo
