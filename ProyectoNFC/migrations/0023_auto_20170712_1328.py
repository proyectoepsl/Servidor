# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-12 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoNFC', '0022_auto_20170709_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registro',
            name='Fecha_Out',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
