# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myweb', '0003_auto_20170818_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='webuser',
            name='collection',
            field=models.ManyToManyField(to='myweb.Article'),
        ),
        migrations.AlterField(
            model_name='webuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, default='static/images/avatar/default.png', upload_to='avatar'),
        ),
    ]
