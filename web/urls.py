"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
#from django.contrib import admin
from myweb import views as myview

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^temp', myview.temp, name='temp'),
    url(r'^$', myview.index, name='index'),
    url(r'^tips', myview.tips, name='tips'),
    url(r'^404', myview.h404, name='404'),
    url(r'^jie/page/(\d+)$', myview.jieindex, name='jieindex'),#问答的特定页
    url(r'^jie/detail/(.+)$', myview.jiedetail, name='jiedetail'),#文章详细信息
    url(r'^jie/delete', myview.jiedelete, name='jiedelete'),#删除文章
    url(r'^jieadd', myview.jieadd, name='jieadd'),#添加文章
    url(r'^userindex', myview.userindex, name='userindex'),#用户中心
    url(r'^userhome/(.+)$', myview.userhome, name='userhome'),#用户主页
    url(r'^userset', myview.userset, name='userset'),#用户设置
    url(r'^usermessage', myview.usermessage, name='usermessage'),#用户消息
    url(r'^useractivate', myview.useractivate, name='useractivate'),#激活邮件
    url(r'^userforget', myview.userforget, name='userforget'),#忘记密码
    url(r'^userlogin', myview.userlogin, name='userlogin'),#用户登录
    url(r'^userreg', myview.userreg, name='userreg'),#用户注册
    url(r'^userlogout', myview.userlogout, name='userlogout'),#用户注销
    url(r'^user/upload', myview.upload_avatar, name='upload_avatar'),#上传头像
    url(r'^api/upload', myview.upload_img, name='upload_img'),#上传图片
    url(r'^jie/edit/(.+)$', myview.jieedit, name='jieedit'),#文章编辑
    url(r'^api/mine-jie', myview.myArticle, name='jiemine'),#我的文章
    url(r'^collection/find', myview.myCollection, name='myCollection'),#我的收藏
    url(r'^jie/reply', myview.jiereply, name='jiereply'),#回复文章
    url(r'^collection/(.+)$', myview.collection, name='collection'),#收藏文章
    url(r'^api/jieda/(.+)$', myview.jieda, name='jieda'),#回复操作
    url(r'^jietie/(.+)/(\d+)$', myview.jietie, name='jietie'),#搜贴
    url(r'^message/(.+)$', myview.message, name='message'),#消息处理
]
