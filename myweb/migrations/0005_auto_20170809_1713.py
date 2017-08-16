# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myweb', '0004_auto_20170809_1711'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='Article_Attachment',
        ),
        migrations.RemoveField(
            model_name='article',
            name='Article_Category',
        ),
        migrations.RemoveField(
            model_name='article',
            name='creator',
        ),
        migrations.DeleteModel(
            name='Article',
        ),
    ]
