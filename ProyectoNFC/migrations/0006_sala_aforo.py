# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-12 10:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoNFC', '0005_auto_20170612_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='sala',
            name='Aforo',
            field=models.IntegerField(null=True),
        ),
    ]
