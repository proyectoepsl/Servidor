# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-09 16:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoNFC', '0018_auto_20170704_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sala',
            name='Hash',
            field=models.CharField(max_length=14, unique=True),
        ),
    ]
