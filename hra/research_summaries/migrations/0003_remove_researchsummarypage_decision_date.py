# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-07 14:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('research_summaries', '0002_embiggen_strings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='researchsummarypage',
            name='decision_date',
        ),
    ]
