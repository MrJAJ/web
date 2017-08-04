# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('userName', models.CharField(max_length=50)),
                ('email', models.EmailField(primary_key=True, max_length=50, serialize=False)),
                ('password', models.CharField(max_length=50)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatar/')),
                ('score', models.IntegerField(default=0)),
                ('desc', models.TextField(blank=True, null=True)),
                ('joined_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
