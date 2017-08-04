# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myweb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Webuser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatar/')),
                ('score', models.IntegerField(default=0)),
                ('desc', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='webuser',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
