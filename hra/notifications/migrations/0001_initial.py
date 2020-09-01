# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-17 16:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0033_remove_golive_expiry_help_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationBarSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('default', 'Notification'), ('error', 'Error'), ('success', 'Success')], help_text='Set empty type to hide the notification', max_length=32)),
                ('title', models.CharField(max_length=128)),
                ('text', wagtail.core.fields.RichTextField(blank=True, max_length=128)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
