# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-14 18:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoNFC', '0010_auto_20170614_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registro',
            name='Sala',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProyectoNFC.Sala'),
        ),
        migrations.AlterField(
            model_name='registro',
            name='Usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProyectoNFC.Usuario'),
        ),
    ]
