# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-04-22 12:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '用户', 'verbose_name_plural': '用户'},
        ),
        migrations.AlterModelTable(
            name='user',
            table='tb_users',
        ),
    ]
