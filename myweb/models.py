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
