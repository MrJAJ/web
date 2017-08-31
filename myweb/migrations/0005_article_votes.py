# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myweb', '0004_auto_20170823_0928'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='votes',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
