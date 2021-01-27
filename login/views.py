from django.shortcuts import render,redirect,HttpResponse,reverse
# Create your views here.
import datetime
from .models import Alluser
import time
def login(request):
    if request.session.get('is_login', None):
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username.strip() and password:
            try:
                user=Alluser.objects.get(name=username)
            except:
                return render(request,'login/login.html',{'msg':'用户不存在'})
            if user.password == password:
                request.session['username']=username
                request.session['is_login']=True
                user.last_login=datetime.datetime.now()
                user.save()
                return redirect('/')
            else:
                return render(request,'login/login.html',{'msg':'密码错误'})
        else:
            return render(request, 'login/login.html', {'msg': '请输入完整信息'})
    return render(request,'login/login.html')

def create(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        if username and password1 and password2:
            if password1 != password2:
                return render(request, 'login/create.html', {'msg': '两次密码不一致'})
            chazhao=Alluser.objects.filter(name=username)
            if chazhao:
                return render(request, 'login/create.html', {'msg': '用户名已存在'})
            if mobile:
                chazhao = Alluser.objects.filter(mobile=mobile)
                if chazhao:
                    return render(request, 'login/create.html', {'msg': '手机号码已被注册'})
            if len(username)>10:
                return render(request, 'login/create.html', {'msg': '用户名太长了'})
            if len(password1)>20:
                return render(request, 'login/create.html', {'msg': '密码不用这么长吧？'})
            if mobile:
                if len(mobile)<15:
                    a = Alluser.objects.create(name=username,password=password1,mobile=mobile)
                else:
                    return render(request, 'login/create.html', {'msg': '手机号码有问题'})
            else:
                a = Alluser.objects.create(name=username, password=password1)
            request.session.set_expiry(None)
            request.session['username'] = username
            request.session['is_login'] = True
            a.last_login=datetime.datetime.now()
            a.save()
            return redirect('/')
        else:
            return render(request, 'login/create.html',{'msg': '输入注册的账号和密码'})
    return render(request,'login/create.html')


def logout(request):
    request.session.flush()
    return redirect(request.META.get('HTTP_REFERER', '/'))