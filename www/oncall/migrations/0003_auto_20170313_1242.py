# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 17:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oncall', '0002_auto_20170313_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactmethod',
            name='user',
        ),
        migrations.AddField(
            model_name='contactmethod',
            name='user_profile',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='oncall.UserProfile'),
            preserve_default=False,
        ),
    ]
