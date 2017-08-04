from django.shortcuts import render,redirect,render_to_response
import os,json
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate,login,logout
from .models import Webuser
from .forms import LoginForm,RegForm
from django.http import HttpResponse
from django.contrib import messages
from django.core import serializers
from  django.conf import settings
# Create your views here.


def temp(request):
    return render(request, 'website/temp.html')
def tips(request):
    return render(request, 'website/tips.html')
def h404(request):
    return render(request, 'website/404.html')
def index(request):
    user=request.user
    webuser = Webuser.objects.get(user_id=request.user.id)
    return render(request, 'website/index.html',{'webuser':webuser})
def full(request):
    return render(request, 'website/full.html')
def jieindex(request):
    webuser = Webuser.objects.get(user_id=request.user.id)
    return render(request, 'website/jie/index.html',{'webuser':webuser})
def jiedetail(request):
    webuser = Webuser.objects.get(user_id=request.user.id)
    return render(request, 'website/jie/detail.html',{'webuser':webuser})
def jieadd(request):
    webuser = Webuser.objects.get(user_id=request.user.id)
    return render(request, 'website/jie/add.html',{'webuser':webuser})
def userindex(request):
    webuser = Webuser.objects.get(user_id=request.user.id)
    return render(request, 'website/user/index.html',{'webuser':webuser})
def userhome(request):
    webuser = Webuser.objects.get(user_id=request.user.id)
    return render(request, 'website/user/home.html',{'webuser':webuser})
def userset(request):
    user = request.user
    nowpass = request.POST.get("nowpass")
    sign=request.POST.get("sign")
    if nowpass is not None and sign is None:
        password = request.POST.get("pass")
        if user.check_password(nowpass):
            messages.success(request,"密码修改成功")
            user.set_password(password)
            user.save()
            logout(request)
            return render(request, 'website/user/login.html')
        else:
            messages.error(request,"当前密码错误")
            webuser = Webuser.objects.get(user_id=request.user.id)
            return render(request, 'website/user/set.html', {'webuser': webuser})
    if nowpass is None and sign is not None:
        email=request.POST.get("email")
        username=request.POST.get("username")
        city=request.POST.get("city")
        sex=request.POST.get("sex")
        desc=request.POST.get("sign")
        webuser = Webuser.objects.get(user_id=request.user.id)
        webuser.desc=desc
        webuser.sex=sex
        webuser.city=city
        webuser.save()
        user.username=username
        user.email=email
        user.save()
        messages.success(request,"资料修改成功")
        return render(request, 'website/user/set.html', {'webuser': webuser})
    else:
        webuser = Webuser.objects.get(user_id=request.user.id)
        return render(request, 'website/user/set.html',{'webuser':webuser})
def usermessage(request):
    webuser = Webuser.objects.get(user_id=request.user.id)
    return render(request, 'website/user/message.html',{'webuser':webuser})
def useractivate(request):
    return render(request, 'website/user/activate.html')
def userforget(request):
    return render(request, 'website/user/forget.html')
def userlogin(request):
    if request.user.is_authenticated():
        return HttpResponse("用户已登录")
    if request.method == 'POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username=request.POST.get('username')
            password = request.POST.get('password')
            user=authenticate(username=username,password=password)
            if user:
                login(request,user)
                webuser = Webuser.objects.get(user_id=user.id)
                return render(request,'website/user/home.html',{'webuser':webuser})
            else:
                return render(request, 'website/user/login.html')
        else:
            return render(request, 'website/user/login.html')
    else:
        return render(request, 'website/user/login.html')
def userreg(request):
    nowpass = request.POST.get("nowpass")
    password = request.POST.get("pass")
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        User.objects.create_user(username=username, password=password, email=email)
        user=authenticate(username=username,password=password)
        if user is not None:
            webuser=Webuser(user=user)
            webuser.save()
            login(request,user)
            return render(request, 'website/user/login.html')
        else:
            print("user is null")
    else:
        return render(request, 'website/user/reg.html')
def userlogout(request):
    logout(request)
    return render(request, 'website/user/login.html')
def upload_avatar(request):
    file=request.FILES['file']
    filepath=open(os.path.join("static/images/avatar", file.name), 'wb+')
    webuser = Webuser.objects.get(user_id=request.user.id)
    webuser.avatar=filepath.name
    webuser.save()
    for chunk in file.chunks():  # 分块写入文件
        filepath.write(chunk)
        filepath.close()
    #return render(request, 'website/user/set.html',{'webuser':webuser})
    result={
        "status":0,
        "url":filepath.name,
        "msg":"头像上传成功"

    }
    return HttpResponse(json.dumps(result))
