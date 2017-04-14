from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch import index

from hra.utils.models import (
    CallToActionSnippet,
    SocialFields
)


class HomePage(Page, SocialFields):
    strapline = models.CharField(blank=True, max_length=255)
    call_to_action = models.ForeignKey(CallToActionSnippet, blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    search_fields = Page.search_fields + [
        index.SearchField('strapline'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('strapline'),
        FieldPanel('call_to_action'),
    ]

    promote_panels = (
        Page.promote_panels +  # slug, seo_title, show_in_menus, search_description
        SocialFields.promote_panels
    )

    # Only allow creating HomePages at the root level
    parent_page_types = ['wagtailcore.Page']
