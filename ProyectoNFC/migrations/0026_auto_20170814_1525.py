# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-14 13:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoNFC', '0025_auto_20170725_1829'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sala',
            old_name='Hash',
            new_name='Imei',
        ),
    ]
