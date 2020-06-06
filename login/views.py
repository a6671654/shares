from django.shortcuts import render,redirect,HttpResponse
# Create your views here.
def login(request):
    # if request.method=='POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     if username.strip() and password:
    #         try:
    #             user=User.objects.get(name=username)
    #         except:
    #             return render(request,'login/login.html',{'msg':'用户不存在'})
    #         if user.password==password:
    #             request.session.set_expiry(1800)
    #             request.session['username']=username
    #             request.session['is_login']=True
    #             return redirect('/')
    #         else:
    #             return render(request,'login/login.html',{'msg':'密码错误'})
    return render(request,'login/login.html')
def create(request):
    return render(request,'login/create.html')

def logout(request):
    request.session['is_login']=False
    return redirect('/')