# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myweb', '0006_auto_20170825_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webuser',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
