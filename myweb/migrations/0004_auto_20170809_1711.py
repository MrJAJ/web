# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myweb', '0003_auto_20170809_1654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='creator_id',
        ),
        migrations.AddField(
            model_name='article',
            name='creator',
            field=models.ForeignKey(default=None, to='myweb.Webuser'),
        ),
    ]
