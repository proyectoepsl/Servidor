# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-25 16:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoNFC', '0024_auto_20170712_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='sala',
            name='Aforo_Maximo',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sala',
            name='Aforo',
            field=models.PositiveIntegerField(default=0),
        ),
    ]