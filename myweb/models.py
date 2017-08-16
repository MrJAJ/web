from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Webuser(models.Model):
    user=models.OneToOneField(User)
    avatar=models.ImageField(upload_to='avatar',blank=True,null=True,default='static/images/avatar\default.png')
    score=models.IntegerField(default=0)#积分
    desc=models.TextField(blank=True,null=True)#签名
    city=models.TextField(max_length=50,blank=True,null=True)#城市
    sex=models.IntegerField(default=0)#0为男，1为女
    qq=models.TextField(max_length=12,blank=True,null=True)
    weibo=models.TextField(max_length=50,blank=True,null=True)
    def __unicode__(self):
        return  self.user.username
class Category(models.Model):
    cid=models.CharField(primary_key=True,max_length=50)
    category=models.CharField(max_length=50)
    group=models.CharField(max_length=50)
    def __unicode__(self):
        return  self.cid
class Article(models.Model):
    aid=models.AutoField(primary_key=True)
    title=models.CharField(max_length=50)
    content=models.TextField()#正文
    creator=models.ForeignKey(Webuser,default=None)
    pubTime=models.DateTimeField(auto_now_add=True)
    parentID=models.CharField(max_length=50,null=True,blank=True)#父贴
    score=models.IntegerField(default=0)#帖子悬赏积分
    Article_Attachment=models.ManyToManyField('Attachment')
    Article_Category = models.ManyToManyField('Category')
    def __unicode__(self):
        return  self.aid

class Attachment(models.Model):
    attachid = models.AutoField(primary_key=True)#附件ID
    price=models.IntegerField(default=0)#附件下载所需积分
    data=models.FilePathField()#附件路径
    def __unicode__(self):
        return  self.attachid



