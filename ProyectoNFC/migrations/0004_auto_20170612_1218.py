# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-12 10:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoNFC', '0003_auto_20170611_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registro',
            name='Sala_Id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProyectoNFC.Sala'),
        ),
        migrations.AlterField(
            model_name='registro',
            name='Usuario_Id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProyectoNFC.Usuario'),
        ),
    ]
