from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Webuser(models.Model):#用户表
    id = models.AutoField(primary_key=True)  # ID
    user=models.OneToOneField(User)#user一对一
    avatar=models.ImageField(upload_to='avatar',blank=True,null=True,default='static/images/avatar/default.png')#头像
    score=models.IntegerField(default=0)#积分
    desc=models.TextField(blank=True,null=True)#签名
    city=models.TextField(max_length=50,blank=True,null=True)#城市
    sex=models.IntegerField(default=0)#0为男，1为女
    qq=models.TextField(max_length=12,blank=True,null=True)
    weibo=models.TextField(max_length=50,blank=True,null=True)
    collection=models.ManyToManyField('Article')#文章收藏，与文章多对多
    def __unicode__(self):
        return  self.user.username
class Category(models.Model):#目录表
    cid=models.CharField(primary_key=True,max_length=50)
    category=models.CharField(max_length=50)#目录名
    group=models.CharField(max_length=50)#目录分组
    def __unicode__(self):
        return  self.cid
class Attachment(models.Model):
    id = models.AutoField(primary_key=True)#附件ID
    price=models.IntegerField(default=0)#附件下载所需积分
    data=models.FilePathField(default='/')#附件路径
    isTop=models.IntegerField(default=0)#是否置顶
    isPicked=models.IntegerField(default=0)#是否加精（文章时）|采纳（回复时）
    isFinish=models.IntegerField(default=0)#是否完结
    clicks=models.IntegerField(default=0)#点击数（文章时）|点赞数（回复时）
    replys=models.IntegerField(default=0)#回复数
    votes=models.ManyToManyField('Webuser')#点赞数
    def __unicode__(self):
        return  self.id


class Article(models.Model):
    aid=models.AutoField(primary_key=True)
    title=models.CharField(max_length=50,default="这是标题")#文章标题
    content=models.TextField()#正文
    creator=models.ForeignKey(Webuser,default=None)#作者
    pubTime=models.DateTimeField(auto_now_add=True)#发布时间
    parentID=models.ForeignKey('self',default=0)#父贴。0表示为文章，否则为回复
    score=models.IntegerField(default=0,null=True)#帖子悬赏积分
    attach=models.ForeignKey(Attachment,null=True)#帖子附加信息
    Article_Category = models.ManyToManyField('Category')#文章目录
    def __unicode__(self):
        return  self.aid




