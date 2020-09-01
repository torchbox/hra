# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-28 11:20
from __future__ import unicode_literals

from django.db import migrations
import hra.utils.blocks
import hra.utils.models
import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks
import wagtail.snippets.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_image_block_longdesc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspage',
            name='body',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title', icon='title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.core.blocks.CharBlock(required=False)), ('longdesc', wagtail.core.blocks.PageChooserBlock(help_text='If this image conveys infomation not given in the page text, provide a page with an full description for non-sighted users.', label='Long description', required=False, target_model=['standardpage.StandardPage']))))), ('quote', wagtail.core.blocks.StructBlock((('quote', wagtail.core.blocks.RichTextBlock()), ('quotee', wagtail.core.blocks.CharBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(required=False))))), ('embed', wagtail.embeds.blocks.EmbedBlock()), ('call_to_action', wagtail.core.blocks.StructBlock((('call_to_action', wagtail.snippets.blocks.SnippetChooserBlock(hra.utils.models.CallToActionSnippet)), ('side_text', wagtail.core.blocks.RichTextBlock())))), ('highlight', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('text', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(required=False))))), ('table', wagtail.contrib.table_block.blocks.TableBlock(template='blocks/table_block.html')), ('lms_login', hra.utils.blocks.LMSLoginBlock()))),
        ),
    ]
