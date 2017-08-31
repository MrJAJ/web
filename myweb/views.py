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
    if request.user.is_authenticated():#用户已认证
        attch=Attachment.objects.filter(isTop=1)
        pickedArticles=Article.objects.filter(parentID=0).filter(attach=attch)#获取指置顶文章
        articles = Article.objects.filter(parentID=0).exclude(attach=attch)
        webuser = Webuser.objects.get(user_id=request.user.id)#获取当前用户
        sql = 'select aid,title,clicks from myweb_article,myweb_attachment WHERE attach_id=id and parentID_id=0 ORDER BY clicks DESC LIMIT 10'#获取10个最近热帖
        cursor = connection.cursor()
        cursor.execute(sql)
        mlarticles = cursor.fetchall()
        sql2='select aid,title,replys from myweb_article,myweb_attachment WHERE attach_id=id and parentID_id=0 ORDER BY replys DESC LIMIT 10'#获取10个最近热议
        cursor=connection.cursor()
        cursor.execute(sql2)
        mrarticles=cursor.fetchall()
        us=Article.objects.exclude(parentID=0).values('creator_id').annotate(num_replys=Count('creator_id')).values('creator','num_replys').order_by('-num_replys')[0:12]#获取12个回答榜用户
        users=[]
        for u in us:
            user={}
            user['creator']=Webuser.objects.get(id=u['creator'])#回答榜用户信息
            user['num']=u['num_replys']#回复数
            users.append(user)
        return render(request, 'website/index.html',{'webuser':webuser,"pickedArticles":pickedArticles,"articles":articles,"mlarticles":mlarticles,"mrarticles":mrarticles,"users":users})
    else:
        return render(request, 'website/user/login.html')
def jieindex(request,page=1):
    if request.user.is_authenticated():#用户认证
        page=int(page)
        webuser = Webuser.objects.get(user_id=request.user.id)#获取用户
        num=Article.objects.filter(parentID=0).count()#获取文章总数
        num=int(num/10)+1#总页数
        start=10*(page-1)#起始页
        end=start+10#结束页
        articles=Article.objects.filter(parentID=0).order_by("pubTime").order_by("-attach__isTop")[start:end]#获取始末区间文章
        result={
            "curr":page,#当前页
            "num":num#总页数
        }
        return render(request, 'website/jie/index.html',{'webuser':webuser,"articles":articles,'result':json.dumps(result)})
    else:
        return render(request, 'website/user/login.html')
def jietie(request,type,page=1):
    if request.user.is_authenticated():#用户认证
        webuser=Webuser.objects.get(user=request.user)#用户
        page = int(page)
        start = 10 * (page - 1)
        end = start + 10
        articles=[]
        num=0
        if type == 'unsolved':#获取未结贴文章
            articles = Article.objects.filter(parentID=0).filter(attach__isFinish=0).order_by('pubTime').order_by("-attach__isTop")[start:end]
            num = articles.count()
            num = int(num / 10) + 1
        if type == 'solved':#获取已结贴文章
            articles = Article.objects.filter(parentID=0).filter(attach__isFinish=1).order_by('pubTime').order_by("-attach__isTop")[start:end]
            num = articles.count()
            num = int(num / 10) + 1
        if type == 'picked':#获取精贴
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
    if aid == '0':#游客
        return render(request, 'website/404.html', {'webuser': webuser})
    else:
        replys = Article.objects.filter(parentID=aid).order_by('pubTime')#获取该文章的回复信息
        article=Article.objects.get(aid=aid)#获取文章
        attch = Attachment.objects.get(id=article.attach.id)#获取文章附件信息
        attch.clicks += 1#文章阅览数加1
        attch.save()
        article.attach=attch
        for reply in replys:
            reply.content=json.dumps(reply.content)
        result={
            "content":article.content,#文章内容
            "status":0,
        }
        sql = 'select aid,title,clicks from myweb_article,myweb_attachment WHERE attach_id=id and parentID_id=0 ORDER BY clicks DESC LIMIT 10'#获取最近热帖
        cursor = connection.cursor()
        cursor.execute(sql)
        mlarticles = cursor.fetchall()
        sql2 = 'select aid,title,replys from myweb_article,myweb_attachment WHERE attach_id=id and parentID_id=0 ORDER BY replys DESC LIMIT 10'#最近热议
        cursor = connection.cursor()
        cursor.execute(sql2)
        mrarticles = cursor.fetchall()
        return render(request, 'website/jie/detail.html',{'webuser':webuser, 'replys':replys, "article":article,"mlarticles":mlarticles,"mrarticles":mrarticles,"result":json.dumps(result)})
def jieadd(request):#添加文章
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
        sql = 'select aid,title,clicks from myweb_article,myweb_attachment WHERE attach_id=id and parentID_id=0 ORDER BY clicks DESC LIMIT 10'  # 获取最近热帖
        cursor = connection.cursor()
        cursor.execute(sql)
        mlarticles = cursor.fetchall()
        sql2 = 'select aid,title,replys from myweb_article,myweb_attachment WHERE attach_id=id and parentID_id=0 ORDER BY replys DESC LIMIT 10'  # 最近热议
        cursor = connection.cursor()
        cursor.execute(sql2)
        mrarticles = cursor.fetchall()
        return render(request, 'website/jie/detail.html', {'webuser': webuser, 'replys': replys, "article":article,"result":json.dumps(result),"mlarticles":mlarticles,"mrarticles":mrarticles})
    else:
        category=Category.objects.all()
        return render(request, 'website/jie/add.html',{'webuser':webuser,'category':category})
def userindex(request):#用户中心
    webuser = Webuser.objects.get(user_id=request.user.id)
    return render(request, 'website/user/index.html',{'webuser':webuser})
def userhome(request,uid):#用户主页
    webuser = Webuser.objects.get(user_id=request.user.id)
    try:
        us=User.objects.get(username=uid)#按用户名获取用户
    except:
        us=User.objects.get(id=uid)#按id获取用户a
    user=Webuser.objects.get(user=us)
    articles=Article.objects.filter(creator=user).filter(parentID=0).order_by('-pubTime')#用户发表文章
    replys=Article.objects.filter(creator=user).exclude(parentID=0).order_by('-pubTime')[0:5]#用户发表回复
    for reply in replys:
        reply.content = json.dumps(reply.content)
    return render(request, 'website/user/home.html',{'webuser':webuser,'user':user,'articles':articles,"replys":replys})
def userset(request):#用户设置，尚未对密码进行判断，只进行密码比对
    user = request.user
    nowpass = request.POST.get("nowpass")#当前密码
    sign=request.POST.get("sign")#验证
    if nowpass is not None and sign is None:#密码修改
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
    if nowpass is None and sign is not None:#用户信息修改
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
        result = {
            'status': 0,
        }
        return HttpResponse(json.dumps(result))
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
    if request.user.is_authenticated():#用户已认证
        return HttpResponse("用户已登录")
    if request.method == 'POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username=request.POST.get('username')
            password = request.POST.get('password')
            user=authenticate(username=username,password=password)
            if user:
                login(request,user)
                attch = Attachment.objects.filter(isTop=1)
                pickedArticles = Article.objects.filter(parentID=0).filter(attach=attch)  # 获取指置顶文章
                articles = Article.objects.filter(parentID=0).exclude(attach=attch)
                webuser = Webuser.objects.get(user_id=request.user.id)
                sql = 'select aid,title,clicks from myweb_article,myweb_attachment WHERE attach_id=id and parentID_id=0 ORDER BY clicks DESC LIMIT 10'  # 获取10个最近热帖
                cursor = connection.cursor()
                cursor.execute(sql)
                mlarticles = cursor.fetchall()
                sql2 = 'select aid,title,replys from myweb_article,myweb_attachment WHERE attach_id=id and parentID_id=0 ORDER BY replys DESC LIMIT 10'  # 获取10个最近热议
                cursor = connection.cursor()
                cursor.execute(sql2)
                mrarticles = cursor.fetchall()
                us = Article.objects.exclude(parentID=0).values('creator_id').annotate(
                    num_replys=Count('creator_id')).values('creator', 'num_replys').order_by('-num_replys')[
                     0:12]  # 获取12个回答榜用户
                users = []
                for u in us:
                    user = {}
                    user['creator'] = Webuser.objects.get(id=u['creator'])  # 回答榜用户信息
                    user['num'] = u['num_replys']  # 回复数
                    users.append(user)
                return render(request, 'website/index.html',{'webuser': webuser, "pickedArticles": pickedArticles, "articles": articles, "mlarticles": mlarticles, "mrarticles": mrarticles, "users": users})
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
        return render(request, 'website/user/reg.html')
def userlogout(request):
    logout(request)#取消用户认证
    return render(request, 'website/user/login.html')
def upload_avatar(request):#头像上传
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
def upload_img(request):#图像上传
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
def jieedit(request,aid):#文章修改，aid为文章标识
    webuser = Webuser.objects.get(user_id=request.user.id)
    if aid != '0':#跳转文章编辑页面
        article = Article.objects.get(aid=aid)
        category = Category.objects.all()#分类列表
        category_id=article.Article_Category.all().values('cid')#文章分类
        return render(request, 'website/jie/edit.html',{'webuser':webuser, 'article': article,'category':category})
    else:#编辑文章
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
        # 获取该文章的回复信息
        replys = Article.objects.filter(parentID=int(request.POST.get('articleId'))).order_by('pubTime')
        for reply in replys:
            reply.content=json.dumps(reply.content)
        result = {
            "content": article.content,
            "status": 0
        }
        sql = 'select aid,title,clicks from myweb_article,myweb_attachment WHERE attach_id=id and parentID_id=0 ORDER BY clicks DESC LIMIT 10'  # 获取最近热帖
        cursor = connection.cursor()
        cursor.execute(sql)
        mlarticles = cursor.fetchall()
        sql2 = 'select aid,title,replys from myweb_article,myweb_attachment WHERE attach_id=id and parentID_id=0 ORDER BY replys DESC LIMIT 10'  # 最近热议
        cursor = connection.cursor()
        cursor.execute(sql2)
        mrarticles = cursor.fetchall()
        return  render(request, 'website/jie/detail.html', {'webuser': webuser, 'replys': replys, "article":article,"mlarticles":mlarticles,"mrarticles":mrarticles,"result":json.dumps(result)})
def myArticle(request):#我发的贴
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
        row['time']=str(article.pubTime)#发布时间
        row['comment']=article.attach.replys#评论数
        row['hits']=article.attach.clicks#阅览数
        rows.append(row)
    result={
        "status":0,
        "rows":rows,
        "num":num#发帖文章总数
    }
    return HttpResponse(json.dumps(result))
def myCollection(request):#我的收藏
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
def jiereply(request):##文章回复
    webuser = Webuser.objects.get(user_id=request.user.id)
    content = request.POST.get('content')
    jid=request.POST.get('jid')#回复文章ID
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
    if type=="add/":#添加收藏
        article=Article.objects.get(aid=aid)
        webuser.collection.add(article)
        webuser.save()
        result = {
            "status": 0,
            "msg": "收藏成功"
        }
    elif type=="remove/":#取消收藏
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
        flag=article.attach.votes.filter(id=webuser.id)#当前用户是否已点赞
        msg=""
        if flag:#已点赞
            article.attach.votes.remove(webuser)#取消点赞
            article.attach.clicks -= 1
            article.attach.save()
        else:
            article.attach.clicks += 1
            try:
                article.attach.votes.add(webuser)#点赞
            except:
                msg="点赞失败"
            article.attach.save()
        result = {
            "status": 0,
            "msg": msg
        }
        return HttpResponse(json.dumps(result))
    if type=='accept/':#采纳回复
        article.attach.isPicked=1
        article.parentID.attach.isFinish=1
        article.parentID.attach.save()
        article.attach.save()
        result = {
            "status": 0,
            "msg": "采纳成功"
        }
        return HttpResponse(json.dumps(result))
    if type=='delete/':#删除回复
        article.delete()
        article.parentID.attach.replys-=1
        article.parentID.attach.save()
        result = {
            "status": 0,
            "msg": "删除成功"
        }
        return HttpResponse(json.dumps(result))
    if type == 'getDa/':#获取回复内容
        rows={}
        rows["content"]=article.content
        result = {
            "status": 0,
            "msg": "获取回复数据",
            "rows":rows
        }
        return HttpResponse(json.dumps(result))
    if type == 'updateDa/':#更新回复
        article.content=request.POST['content']
        article.save()
        result = {
            "status": 0,
            "msg": "更新回复"
        }
        return HttpResponse(json.dumps(result))
    if type =='set/':#文章设置
        rank=request.POST['rank']#
        field=request.POST['field']
        if field == 'stick':#置顶
            if rank == '1':#置顶
                article.attach.isTop = 1
            else:
                article.attach.isTop = 0
        if field == 'status':#加精
            if rank == '1':#加精
                article.attach.isPicked=1
            else:
                article.attach.isPicked=0
        article.attach.save()
        result = {
            "status": 0,
        }
        return HttpResponse(json.dumps(result))
def jiedelete(request):#删除文章
    aid=request.POST['id']
    webuser = Webuser.objects.get(user_id=request.user.id)
    article=Article.objects.get(aid=aid)
    try:
        article.delete()
        msg=""
    except:
        msg="删除失败"
    result = {
        "status": 0,
        "msg": msg
    }
    return HttpResponse(json.dumps(result))
def message(request,type):#消息处理
    result={}
    if type=='nums/':#消息数
        result={
            'status':0,
            'count':2
        }
    if type=='read/':#读取消息
        result = {
            'status': 0,
        }
    return HttpResponse(json.dumps(result))