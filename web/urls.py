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
    url(r'^jie/page/(\d+)$', myview.jieindex, name='jieindex'),
    url(r'^jie/detail/(.+)$', myview.jiedetail, name='jiedetail'),
    url(r'^jie/delete', myview.jiedelete, name='jiedelete'),
    url(r'^jieadd', myview.jieadd, name='jieadd'),
    url(r'^userindex', myview.userindex, name='userindex'),
    url(r'^userhome/(.+)$', myview.userhome, name='userhome'),
    url(r'^userset', myview.userset, name='userset'),
    url(r'^usermessage', myview.usermessage, name='usermessage'),
    url(r'^useractivate', myview.useractivate, name='useractivate'),
    url(r'^userforget', myview.userforget, name='userforget'),
    url(r'^userlogin', myview.userlogin, name='userlogin'),
    url(r'^userreg', myview.userreg, name='userreg'),
    url(r'^userlogout', myview.userlogout, name='userlogout'),
    url(r'^user/upload', myview.upload_avatar, name='upload_avatar'),
    url(r'^api/upload', myview.upload_img, name='upload_img'),
    url(r'^jie/edit/(.+)$', myview.jieedit, name='jieedit'),
    url(r'^api/mine-jie', myview.myArticle, name='jiemine'),
    url(r'^collection/find', myview.myCollection, name='myCollection'),
    url(r'^jie/reply', myview.jiereply, name='jiereply'),
    url(r'^collection/(.+)$', myview.collection, name='collection'),
    url(r'^api/jieda/(.+)$', myview.jieda, name='jieda'),
    url(r'^jietie/(.+)/(\d+)$', myview.jietie, name='jietie'),
]
