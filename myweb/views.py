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
from django.db.models import Count
from django.db import connection,transaction
# Create your views here.


def temp(request):
    return render(request, 'website/temp.html')
def tips(request):
    return render(request, 'website/tips.html')
def h404(request):
    return render(request, 'website/404.html')
def index(request):
    if request.user.is_authenticated():
        attch=Attachment.objects.filter(isTop=1)
        pickedArticles=Article.objects.filter(parentID=0).filter(attach=attch)
        articles = Article.objects.filter(parentID=0).exclude(attach=attch)
        webuser = Webuser.objects.get(user_id=request.user.id)
        sql = 'select aid,title,clicks from myweb_article,myweb_attachment WHERE attach_id=id and parentID_id=0 ORDER BY clicks DESC LIMIT 10'
        cursor = connection.cursor()
        cursor.execute(sql)
        mlarticles = cursor.fetchall()


        sql2='select aid,title,replys from myweb_article,myweb_attachment WHERE attach_id=id and parentID_id=0 ORDER BY replys DESC LIMIT 10'
        cursor=connection.cursor()
        cursor.execute(sql2)
        mrarticles=cursor.fetchall()
        us=Article.objects.exclude(parentID=0).values('creator_id').annotate(num_replys=Count('creator_id')).values('creator','num_replys').order_by('-num_replys')[0:10]
        users=[]
        for u in us:
            user={}
            user['creator']=Webuser.objects.get(id=u['creator'])
            user['num']=u['num_replys']
            users.append(user)
        return render(request, 'website/index.html',{'webuser':webuser,"pickedArticles":pickedArticles,"articles":articles,"mlarticles":mlarticles,"mrarticles":mrarticles,"users":users})
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
        articles=Article.objects.filter(parentID=0).order_by("pubTime").order_by("-attach__isTop")[start:end]
        print(str(articles.query))
        result={
            "curr":page,
            "num":num
        }
        return render(request, 'website/jie/index.html',{'webuser':webuser,"articles":articles,'result':json.dumps(result)})
    else:
        return render(request, 'website/user/login.html')
def jietie(request,type,page=1):
    if request.user.is_authenticated():
        webuser=Webuser.objects.get(user=request.user)
        page = int(page)
        start = 10 * (page - 1)
        end = start + 10
        articles=[]
        num=0
        if type == 'unsolved':
            articles = Article.objects.filter(parentID=0).filter(attach__isFinish=0).order_by('pubTime').order_by("-attach__isTop")[start:end]
            num = articles.count()
            num = int(num / 10) + 1
        if type == 'solved':
            articles = Article.objects.filter(parentID=0).filter(attach__isFinish=1).order_by('pubTime').order_by("-attach__isTop")[start:end]
            num = articles.count()
            num = int(num / 10) + 1
        if type == 'picked':
            articles = Article.objects.filter(parentID=0).filter(attach__isPicked=1).order_by('pubTime').order_by("-attach__isTop")[start:end]
            num = articles.count()
            num = int(num / 10) + 1
        result = {
            "curr": page,
            "num": num
        }
        return render(request, 'website/jie/index.html',{'webuser': webuser, "articles": articles, 'result': json.dumps(result)})

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
    try:
        us=User.objects.get(username=uid)
    except:
        us=User.objects.get(id=uid)
    user=Webuser.objects.get(user=us)
    articles=Article.objects.filter(creator=user).filter(parentID=0).order_by('-pubTime')
    replys=Article.objects.filter(creator=user).exclude(parentID=0).order_by('-pubTime')[0:5]
    for reply in replys:
        reply.content = json.dumps(reply.content)
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
        row['status']=article.attach.isPicked#是否加精
        row['accept']=article.attach.isFinish#是否已解决
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
    articles = webuser.collection.all()
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
def collection(request,type):
    user = request.user
    webuser = Webuser.objects.get(user_id=user.id)
    aid=request.POST['cid']
    if type=="add/":
        article=Article.objects.get(aid=aid)
        webuser.collection.add(article)
        webuser.save()
        result = {
            "status": 0,
            "msg": "收藏成功"
        }
    elif type=="remove/":
        article = Article.objects.get(aid=aid)
        webuser.collection.remove(article)
        webuser.save()
        result = {
            "status": 0,
            "msg": "取消收藏成功"
        }
    else:
        result = {
            "status": 1,
            "msg": "收藏失败"
        }
    return HttpResponse(json.dumps(result))
def jieda(request,type):
    user = request.user
    webuser = Webuser.objects.get(user_id=user.id)
    aid = request.POST['id']
    article = Article.objects.get(aid=aid)
    if type== 'zan/':
        article.attach.clicks+=1
        article.attach.save()
        result = {
            "status": 0,
            "msg": "点赞失败"
        }
        return HttpResponse(json.dumps(result))
    if type=='accept/':
        article.attach.isPicked=1
        article.parentID.attach.isFinish=1
        article.parentID.attach.save()
        article.attach.save()
        result = {
            "status": 0,
            "msg": "采纳成功"
        }
        return HttpResponse(json.dumps(result))
    if type=='delete/':
        article.delete()
        article.parentID.attach.replys-=1
        article.parentID.attach.save()
        result = {
            "status": 0,
            "msg": "删除成功"
        }
        return HttpResponse(json.dumps(result))
    if type == 'getDa/':
        rows={}
        rows["content"]=article.content
        result = {
            "status": 0,
            "msg": "获取回复数据",
            "rows":rows
        }
        return HttpResponse(json.dumps(result))
    if type == 'updateDa/':
        article.content=request.POST['content']
        article.save()
        result = {
            "status": 0,
            "msg": "更新回复"
        }
        return HttpResponse(json.dumps(result))
    if type =='set/':
        rank=request.POST['rank']
        field=request.POST['field']
        print(field)
        print(rank)

        if field == 'stick':
            if rank == '1':
                print("置顶")
                article.attach.isTop = 1
            else:
                print("取消置顶")
                article.attach.isTop = 0
        if field == 'status':
            if rank == '1':
                print("加精")
                article.attach.isPicked=1
            else:
                print("取消加精")
                article.attach.isPicked=0
        article.attach.save()
        result = {
            "status": 0,
        }
        return HttpResponse(json.dumps(result))
def jiedelete(request):
    print("删除文章")
    aid=request.POST['id']
    print(aid)
    webuser = Webuser.objects.get(user_id=request.user.id)
    articel=Article.objects.get(aid=aid)
    try:
        articel.delete()
        msg=""
    except:
        msg="删除失败"
    result = {
        "status": 0,
        "msg": msg
    }
    return HttpResponse(json.dumps(result))