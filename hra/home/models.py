from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel

from hra.home.blocks import HomePageBodyBlock
from hra.utils.models import (
    CallToActionSnippet,
    SocialFields
)


class HomePage(Page, SocialFields):
    call_to_action = models.ForeignKey(CallToActionSnippet, blank=True, null=True, on_delete=models.SET_NULL, related_name='+')
    header_image = models.ForeignKey('images.CustomImage', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    body = StreamField(HomePageBodyBlock())

    content_panels = Page.content_panels + [
        SnippetChooserPanel('call_to_action'),
        StreamFieldPanel('body'),
    ]

    promote_panels = (
        Page.promote_panels +  # slug, seo_title, show_in_menus, search_description
        SocialFields.promote_panels
    )

    # Only allow creating HomePages at the root level
    parent_page_types = ['wagtailcore.Page']
