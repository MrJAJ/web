# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myweb', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='Article_Category',
        ),
        migrations.RemoveField(
            model_name='article',
            name='attach',
        ),
        migrations.RemoveField(
            model_name='article',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='article',
            name='parentID',
        ),
        migrations.RemoveField(
            model_name='webuser',
            name='user',
        ),
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.DeleteModel(
            name='Attachment',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Webuser',
        ),
    ]
