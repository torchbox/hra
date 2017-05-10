from django.db import models
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, StreamFieldPanel,
    InlinePanel
)

from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch import index

from hra.utils.blocks import StoryBlock
from hra.utils.models import (
    ListingFields,
    SocialFields,
    RelatedDocument,
    RelatedPage
)


class StandardPageRelatedDocument(RelatedDocument):
    page = ParentalKey('standardpage.StandardPage', related_name='related_documents')


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
        # TODO: Cleanup if we decide that we don't need related docs here
        # InlinePanel('related_documents', label="Related documents"),
        InlinePanel('related_pages', label="Related pages"),
    ]

    promote_panels = Page.promote_panels + SocialFields.promote_panels + ListingFields.promote_panels


class StandardIndex(Page, SocialFields):
    introduction = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
    ]

    promote_panels = Page.promote_panels + SocialFields.promote_panels

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context['siblings'] = self.get_siblings().live().public()

        return context
