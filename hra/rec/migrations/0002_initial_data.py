# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def create_committee_types(apps, schema_editor):
    CommitteeType = apps.get_model('rec.CommitteeType')

    names = [
        'Authorised REC',
        'RECs not authorised to review clinical trials',
        'RECs recognised to review CTIMPS in healthy volunteers - type i',
        'RECs recognised to review CTIMPS in patients - type iii',
    ]

    objects = []
    for name in names:
        objects.append(CommitteeType(name=name))

    CommitteeType.objects.bulk_create(objects)


def create_committee_flags(apps, schema_editor):
    CommitteeFlag = apps.get_model('rec.CommitteeFlag')

    names = [
        'Establishing Research Databases',
        'Establishing Research Tissue Banks',
        'Gene Therapy or Stem Cell Clinical Trials',
        'IRB Registered',
        'Medical Device Study',
        'Phase 1 Studies in Healthy Volunteers',
        'Phase 1 Studies in Patients',
        'Qualitative Research',
        'Research Involving Adults Lacking Capacity',
        'Research Involving Children',
        'Research Involving Prisoners or Prisons',
        'Social Care Research',
    ]

    objects = []
    for name in names:
        objects.append(CommitteeFlag(name=name))

    CommitteeFlag.objects.bulk_create(objects)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rec', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_committee_types, migrations.RunPython.noop),
        migrations.RunPython(create_committee_flags, migrations.RunPython.noop),
    ]
