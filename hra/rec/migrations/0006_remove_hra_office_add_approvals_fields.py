# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-03-27 15:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rec', '0005_remove_England_choice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='committeepage',
            name='hra_office_name',
        ),
        migrations.AddField(
            model_name='committeepage',
            name='approvals_administrator',
            field=models.CharField(blank=True, max_length=255, verbose_name='Approvals Administrator'),
        ),
        migrations.AddField(
            model_name='committeepage',
            name='approvals_officer',
            field=models.CharField(blank=True, max_length=255, verbose_name='Approvals Officer'),
        ),
    ]
