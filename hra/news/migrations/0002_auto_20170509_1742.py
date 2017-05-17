# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-09 16:42
from __future__ import unicode_literals

from django.db import migrations
import hra.utils.models
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks
import wagtail.wagtailsnippets.blocks
import wagtail.contrib.table_block.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('heading', wagtail.wagtailcore.blocks.CharBlock(classname='full title', icon='title')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('caption', wagtail.wagtailcore.blocks.CharBlock(required=False))))), ('quote', wagtail.wagtailcore.blocks.StructBlock((('quote', wagtail.wagtailcore.blocks.CharBlock(classname='title')), ('quotee', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())))), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('call_to_action', wagtail.wagtailcore.blocks.StructBlock((('call_to_action', wagtail.wagtailsnippets.blocks.SnippetChooserBlock(hra.utils.models.CallToActionSnippet)), ('side_text', wagtail.wagtailcore.blocks.RichTextBlock())))), ('highlight', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.RichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False))))), ('table', wagtail.contrib.table_block.blocks.TableBlock(template='blocks/table_block.html')))),
        ),
    ]
