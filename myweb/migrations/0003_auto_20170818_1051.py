# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myweb', '0002_auto_20170818_1050'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('aid', models.AutoField(primary_key=True, serialize=True)),
                ('title', models.CharField(max_length=50, default='这是标题')),
                ('content', models.TextField()),
                ('pubTime', models.DateTimeField(auto_now_add=True)),
                ('score', models.IntegerField(null=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.IntegerField(default=0)),
                ('data', models.FilePathField(default='/')),
                ('isTop', models.IntegerField(default=0)),
                ('isPicked', models.IntegerField(default=0)),
                ('isFinish', models.IntegerField(default=0)),
                ('clicks', models.IntegerField(default=0)),
                ('replys', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('cid', models.CharField(primary_key=True, max_length=50, serialize=False)),
                ('category', models.CharField(max_length=50)),
                ('group', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Webuser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('avatar', models.ImageField(blank=True, null=True, default='static/images/avatar\\default.png', upload_to='avatar')),
                ('score', models.IntegerField(default=0)),
                ('desc', models.TextField(blank=True, null=True)),
                ('city', models.TextField(max_length=50, blank=True, null=True)),
                ('sex', models.IntegerField(default=0)),
                ('qq', models.TextField(max_length=12, blank=True, null=True)),
                ('weibo', models.TextField(max_length=50, blank=True, null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='Article_Category',
            field=models.ManyToManyField(to='myweb.Category'),
        ),
        migrations.AddField(
            model_name='article',
            name='attach',
            field=models.ForeignKey(null=True, to='myweb.Attachment'),
        ),
        migrations.AddField(
            model_name='article',
            name='creator',
            field=models.ForeignKey(default=None, to='myweb.Webuser'),
        ),
        migrations.AddField(
            model_name='article',
            name='parentID',
            field=models.ForeignKey(default=0, to='myweb.Article'),
        ),
    ]
