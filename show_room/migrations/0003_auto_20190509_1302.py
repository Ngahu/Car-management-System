# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-05-09 10:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('show_room', '0002_auto_20190509_0724'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
