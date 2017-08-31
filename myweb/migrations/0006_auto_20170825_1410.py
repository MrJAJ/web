# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myweb', '0005_article_votes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='votes',
        ),
        migrations.AddField(
            model_name='attachment',
            name='votes',
            field=models.ManyToManyField(to='myweb.Webuser'),
        ),
    ]
