# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-07 12:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research_summaries', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researchsummarypage',
            name='clinicaltrials_number',
            field=models.CharField(blank=True, max_length=1000, verbose_name='Clinicaltrials.gov Identifier'),
        ),
        migrations.AlterField(
            model_name='researchsummarypage',
            name='contact_email',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='researchsummarypage',
            name='contact_name',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='researchsummarypage',
            name='duration_of_study_in_uk',
            field=models.CharField(blank=True, max_length=1000, verbose_name='Duration of Study in UK'),
        ),
        migrations.AlterField(
            model_name='researchsummarypage',
            name='establishment_organisation',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='researchsummarypage',
            name='establishment_organisation_address_1',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='researchsummarypage',
            name='establishment_organisation_address_2',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='researchsummarypage',
            name='establishment_organisation_address_3',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='researchsummarypage',
            name='establishment_organisation_address_postcode',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='researchsummarypage',
            name='eudract_number',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='researchsummarypage',
            name='iras_id',
            field=models.CharField(blank=True, max_length=1000, verbose_name='IRAS ID'),
        ),
        migrations.AlterField(
            model_name='researchsummarypage',
            name='isrctn_number',
            field=models.CharField(blank=True, max_length=1000, verbose_name='ISRCTN Number'),
        ),
        migrations.AlterField(
            model_name='researchsummarypage',
            name='rec_name',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='researchsummarypage',
            name='rec_reference',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='researchsummarypage',
            name='research_database_title',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='researchsummarypage',
            name='rtb_title',
            field=models.CharField(blank=True, max_length=1000, verbose_name='RTBTitle'),
        ),
        migrations.AlterField(
            model_name='researchsummarypage',
            name='sponsor_organisation',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='researchsummarypage',
            name='storage_license',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
