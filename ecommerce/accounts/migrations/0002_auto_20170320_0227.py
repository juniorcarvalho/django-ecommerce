# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-20 05:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Nome'),
        ),
    ]
