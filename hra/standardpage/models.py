from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, StreamFieldPanel,
    InlinePanel
)

from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel

from hra.utils.blocks import StoryBlock
from hra.utils.models import ListingFields, SocialFields, RelatedPage, CallToActionSnippet


class StandardPageRelatedPage(RelatedPage):
    source_page = ParentalKey('standardpage.StandardPage', related_name='related_pages')


class StandardPage(Page, SocialFields, ListingFields):
    introduction = models.TextField(blank=True)
    body = StreamField(StoryBlock())

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        StreamFieldPanel('body'),
        InlinePanel('related_pages', label="Related pages"),
    ]

    promote_panels = Page.promote_panels + SocialFields.promote_panels + ListingFields.promote_panels


class StandardIndexSectionPage(RelatedPage):
    source_page = ParentalKey('standardpage.StandardIndex', related_name='section_pages')


class StandardIndex(Page, SocialFields):
    hero_introduction = models.CharField(blank=True, max_length=120,
                                         help_text='Short text to appear under page title')
    introduction = models.TextField(blank=True)
    call_to_action = models.ForeignKey(CallToActionSnippet, blank=True, null=True, on_delete=models.SET_NULL,
                                       related_name='+')

    content_panels = Page.content_panels + [
        FieldPanel('hero_introduction'),
        FieldPanel('introduction'),
        SnippetChooserPanel('call_to_action'),
        InlinePanel('section_pages', label='Section pages'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
    ]

    promote_panels = Page.promote_panels + SocialFields.promote_panels

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context['siblings'] = self.get_siblings().live().public()

        return context
