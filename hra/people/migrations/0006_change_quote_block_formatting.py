# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-16 13:55
from __future__ import unicode_literals

from django.db import migrations
import hra.utils.models
import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks
import wagtail.snippets.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0005_add_listing_and_social_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personpage',
            name='biography',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title', icon='title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.core.blocks.CharBlock(required=False))))), ('quote', wagtail.core.blocks.StructBlock((('quote', wagtail.core.blocks.RichTextBlock()), ('quotee', wagtail.core.blocks.CharBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(required=False))))), ('embed', wagtail.embeds.blocks.EmbedBlock()), ('call_to_action', wagtail.core.blocks.StructBlock((('call_to_action', wagtail.snippets.blocks.SnippetChooserBlock(hra.utils.models.CallToActionSnippet)), ('side_text', wagtail.core.blocks.RichTextBlock())))), ('highlight', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('text', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(required=False))))), ('table', wagtail.contrib.table_block.blocks.TableBlock(template='blocks/table_block.html'))), blank=True),
        ),
    ]
