# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myweb', '0002_auto_20170726_1018'),
    ]

    operations = [
        migrations.AddField(
            model_name='webuser',
            name='city',
            field=models.TextField(max_length=50, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='webuser',
            name='qq',
            field=models.TextField(max_length=12, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='webuser',
            name='sex',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='webuser',
            name='weibo',
            field=models.TextField(max_length=50, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='webuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, default='static/images/avatar\\default.jpg', upload_to='avatar'),
        ),
    ]
