# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myweb', '0005_auto_20170809_1713'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('aid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('pubTime', models.DateTimeField(auto_now_add=True)),
                ('parentID', models.CharField(max_length=50, blank=True, null=True)),
                ('score', models.IntegerField(default=0)),
                ('Article_Attachment', models.ManyToManyField(to='myweb.Attachment')),
                ('Article_Category', models.ManyToManyField(to='myweb.Category')),
                ('creator', models.ForeignKey(default=None, to='myweb.Webuser')),
            ],
        ),
    ]
