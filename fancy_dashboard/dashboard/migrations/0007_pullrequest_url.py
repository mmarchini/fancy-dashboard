# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 19:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_releasestatus_style'),
    ]

    operations = [
        migrations.AddField(
            model_name='pullrequest',
            name='url',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
