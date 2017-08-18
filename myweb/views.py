from django.shortcuts import render,redirect,render_to_response
import os,json
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate,login,logout
from .models import Webuser,Category,Attachment,Article
from .forms import LoginForm,RegForm
from django.http import HttpResponse
from django.contrib import messages
from django.core import serializers
import time,datetime
from  django.conf import settings
# Create your views here.


def temp(request):
    return render(request, 'website/temp.html')
def tips(request):
    return render(request, 'website/tips.html')
def h404(request):
    return render(request, 'website/404.html')
def index(request):
    if request.user.is_authenticated():
        articles = Article.objects.filter(parentID=0)
        webuser = Webuser.objects.get(user_id=request.user.id)
        return render(request, 'website/index.html',{'webuser':webuser,"articles":articles})
    else:
        return render(request, 'website/user/login.html')
def jieindex(request,page=1):
    if request.user.is_authenticated():
        page=int(page)
        webuser = Webuser.objects.get(user_id=request.user.id)
        num=Article.objects.filter(parentID=0).count()
        num=int(num/10)+1
        start=10*(page-1)
        end=start+10
        articles=Article.objects.filter(parentID=0).order_by("pubTime")[start:end]
        result={
            "curr":page,
            "num":num
        }
        return render(request, 'website/jie/index.html',{'webuser':webuser,"articles":articles,'result':json.dumps(result)})
    else:
        return render(request, 'website/user/login.html')
def jiedetail(request,aid):
    webuser = Webuser.objects.get(user_id=request.user.id)
    if aid == '0':
        return render(request, 'website/404.html', {'webuser': webuser})
    else:
        replys = Article.objects.filter(parentID=aid).order_by('pubTime')
        article=Article.objects.get(aid=aid)
        attch = Attachment.objects.get(id=article.attach.id)
        attch.clicks += 1
        attch.save()
        article.attach=attch
        for reply in replys:
            reply.content=json.dumps(reply.content)
        result={
            "content":article.content,
            "status":0,
        }
        print(replys[0].content)
        return render(request, 'website/jie/detail.html',{'webuser':webuser, 'replys':replys, "article":article,"result":json.dumps(result)})
def jieadd(request):
    webuser = Webuser.objects.get(user_id=request.user.id)
    title = request.POST.get('title')
    if title:
        content = request.POST.get('content')
        category = request.POST.get('class')
        experience = request.POST.get('experience')
        article=Article.objects.create(creator=webuser)
        article.title=title
        article.content=content
        article.score=experience
        article.Article_Category=category
        attach=Attachment.objects.create()
        attach.save()
        article.attach=attach
        article.save()
        result = {
            "content": article.content,
            "status": 0
        }
        replys = Article.objects.filter(parentID=article.aid).order_by('pubTime')
        return render(request, 'website/jie/detail.html', {'webuser': webuser, 'replys': replys, "article":article,"result":json.dumps(result)})
    else:
        category=Category.objects.all()
        return render(request, 'website/jie/add.html',{'webuser':webuser,'category':category})
def userindex(request):
    webuser = Webuser.objects.get(user_id=request.user.id)
    return render(request, 'website/user/index.html',{'webuser':webuser})
def userhome(request,uid):
    webuser = Webuser.objects.get(user_id=request.user.id)
    user=Webuser.objects.get(user_id=uid)
    articles=Article.objects.filter(creator=user).filter(parentID=0).order_by('-pubTime')
    replys=Article.objects.filter(creator=user).exclude(parentID=0).order_by('-pubTime')[0:5]
    for reply in replys:
        reply.content = json.dumps(reply.content)
        print(reply.content)
    return render(request, 'website/user/home.html',{'webuser':webuser,'user':user,'articles':articles,"replys":replys})
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
                articles = Article.objects.filter(parentID=0)
                webuser = Webuser.objects.get(user_id=request.user.id)
                return render(request, 'website/index.html', {'webuser': webuser, "articles": articles})
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
    filepath=open(os.path.join("static/images/avatar/", file.name), 'wb+')
    webuser = Webuser.objects.get(user_id=request.user.id)
    webuser.avatar=filepath.name
    webuser.save()
    for chunk in file.chunks():  # 分块写入文件
        filepath.write(chunk)
        filepath.close()
    result={
        "status":0,
        "url":filepath.name,
        "msg":"头像上传成功"
    }
    return HttpResponse(json.dumps(result))
def upload_img(request):
    file=request.FILES['file']
    filepath=open(os.path.join("static/images/images/", file.name), 'wb+')
    for chunk in file.chunks():  # 分块写入文件
        filepath.write(chunk)
        filepath.close()
    result={
        "status":0,
        "url":filepath.name,
        "msg":"图像上传成功"
    }
    return HttpResponse(json.dumps(result))
def jieedit(request,aid):
    webuser = Webuser.objects.get(user_id=request.user.id)
    if aid != '0':
        article = Article.objects.get(aid=aid)
        category = Category.objects.all()
        category_id=article.Article_Category.all().values('cid')
        return render(request, 'website/jie/edit.html',{'webuser':webuser, 'article': article,'category':category})
    else:
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('class')
        experience = request.POST.get('experience')
        article = Article.objects.get(aid=int(request.POST.get('articleId')))
        article.title = title
        article.content = content
        article.score = experience
        article.Article_Category = category
        article.save()
        replys = Article.objects.filter(parentID=int(request.POST.get('articleId'))).order_by('pubTime')
        result = {
            "content": article.content,
            "status": 0
        }
        return  render(request, 'website/jie/detail.html', {'webuser': webuser, 'replys': replys, "article":article,"result":json.dumps(result)})
def myArticle(request):
    user=request.user
    page=int(request.POST['page'])
    start = 10 * (page - 1)
    end = start + 10
    webuser = Webuser.objects.get(user_id=user.id)
    num= Article.objects.filter(creator=webuser).filter(parentID=0).count()
    articles = Article.objects.filter(creator=webuser).filter(parentID=0).order_by("pubTime")[start:end]
    rows=[]
    for article in articles:
        row = {}
        row['id']=article.aid
        row['title']=article.title
        row['status']=1#是否加精
        row['accept']=-1#是否已解决
        row['time']=str(article.pubTime)
        row['comment']=article.attach.replys
        row['hits']=article.attach.clicks
        rows.append(row)
    result={
        "status":0,
        "rows":rows,
        "num":num
    }
    return HttpResponse(json.dumps(result))
def myCollection(request):
    user=request.user
    webuser = Webuser.objects.get(user_id=user.id)
    articles = Article.objects.filter(creator=webuser)
    rows = []
    for article in articles:
        row = {}
        row['id'] = article.aid
        row['title'] = article.title
        row['collection_time'] = str(article.pubTime)
        rows.append(row)
    result = {
        "status": 0,
        "rows": rows
    }
    return HttpResponse(json.dumps(result))
def jiereply(request):
    webuser = Webuser.objects.get(user_id=request.user.id)
    content = request.POST.get('content')
    jid=request.POST.get('jid')
    parentArticle=Article.objects.get(aid=jid)
    print(jid)
    print(parentArticle.title)
    article = Article.objects.create(creator=webuser)
    article.content = content
    article.parentID =parentArticle
    attach=Attachment.objects.create()
    article.attach=attach
    parentArticle.attach.replys += 1
    attach.save()
    article.save()
    parentArticle.attach.save()
    result = {
        "status": 0,
        "msg": 'sussess'
    }
    return HttpResponse(json.dumps(result))