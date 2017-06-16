from django.db import models
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, StreamFieldPanel,
    InlinePanel,
    MultiFieldPanel
)

from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel

from hra.utils.blocks import StoryBlock
from hra.utils.models import ListingFields, SocialFields, RelatedPage, CallToActionSnippet


class StandardPagePageType(models.Model):
    page = ParentalKey(
        'standardpage.StandardPage',
        related_name='page_type_relationships'
    )
    page_type = models.ForeignKey(
        'categories.PageType',
        related_name='+',
        on_delete=models.CASCADE
    )

    panels = [
        SnippetChooserPanel('page_type')
    ]


class StandardPageRelatedPage(RelatedPage):
    source_page = ParentalKey('standardpage.StandardPage', related_name='related_pages')


class StandardPage(Page, SocialFields, ListingFields):
    hero_image = models.ForeignKey('images.CustomImage', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='+')
    introduction = RichTextField(blank=True)
    body = StreamField(StoryBlock())

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('hero_image'),
        FieldPanel('introduction'),
        StreamFieldPanel('body'),
        InlinePanel('related_pages', label="Related pages"),
    ]

    promote_panels = (
        Page.promote_panels +
        SocialFields.promote_panels +
        ListingFields.promote_panels + [
            InlinePanel('page_type_relationships', label='Page types')
        ]
    )

    @cached_property
    def page_types(self):
        page_types = [
            n.page_type for n in self.page_type_relationships.all()
        ]
        return page_types


class StandardIndexSectionPage(RelatedPage):
    source_page = ParentalKey('standardpage.StandardIndex', related_name='section_pages')


class StandardIndex(Page, SocialFields, ListingFields):
    hero_image = models.ForeignKey('images.CustomImage', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='+')
    hero_introduction = models.CharField(blank=True, max_length=120,
                                         help_text='Short text to appear under page title')
    introduction = RichTextField(blank=True)
    call_to_action = models.ForeignKey(CallToActionSnippet, blank=True, null=True, on_delete=models.SET_NULL,
                                       related_name='+')

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('hero_image'),
            FieldPanel('hero_introduction'),
        ], heading="Hero block"),
        FieldPanel('introduction'),
        SnippetChooserPanel('call_to_action'),
        InlinePanel('section_pages', label='Section pages'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
    ]

    promote_panels = (
        Page.promote_panels +
        SocialFields.promote_panels +
        ListingFields.promote_panels
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context['siblings'] = self.get_siblings().live().public()

        return context
