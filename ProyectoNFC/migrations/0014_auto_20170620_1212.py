# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-20 10:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoNFC', '0013_auto_20170619_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='Clave',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='Dni',
            field=models.CharField(max_length=9),
        ),
    ]
