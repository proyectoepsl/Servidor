# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-17 15:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoNFC', '0011_auto_20170614_2024'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sala',
            old_name='Localizacion',
            new_name='Hash',
        ),
    ]
