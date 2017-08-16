# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('attachid', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.IntegerField(default=0)),
                ('data', models.FilePathField()),
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
    ]
