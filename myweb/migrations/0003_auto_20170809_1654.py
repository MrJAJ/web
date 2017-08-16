# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myweb', '0002_article'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='creator_id',
            field=models.IntegerField(),
        ),
    ]
