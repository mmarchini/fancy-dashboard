# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-19 20:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20170719_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='releasestatus',
            name='style',
            field=models.CharField(default='', max_length=150),
            preserve_default=False,
        ),
    ]