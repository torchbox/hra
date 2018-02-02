from django.db import models
from django.db.models.functions import Coalesce
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailadmin.edit_handlers import (
    StreamFieldPanel, FieldPanel, InlinePanel,
    PageChooserPanel)
from wagtail.wagtailsearch import index

from hra.utils.models import ListingFields, SocialFields, RelatedPage, get_adjacent_pages
from hra.utils.blocks import StoryBlock


class NewsPageCategory(models.Model):
    page = ParentalKey(
        'news.NewsPage',
        related_name='category_relationships'
    )
    category = models.ForeignKey(
        'categories.Category',
        related_name='+',
        on_delete=models.CASCADE
    )

    panels = [
        SnippetChooserPanel('category')
    ]


class NewsPageRelatedPage(RelatedPage):
    source_page = ParentalKey(
        'news.NewsPage',
        related_name='related_pages'
    )


class NewsPage(Page, SocialFields, ListingFields):
    # It's datetime for easy comparison with first_published_at
    publication_date = models.DateTimeField(
        null=True, blank=True,
        help_text="Use this field to override the date that the "
        "news item appears to have been published."
    )
    author = models.CharField(blank=True, max_length=128)
    introduction = RichTextField(blank=True)
    body = StreamField(StoryBlock())

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
        index.SearchField('body')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('publication_date'),
        FieldPanel('author'),
        FieldPanel('introduction'),
        StreamFieldPanel('body'),
        InlinePanel('category_relationships', label="Categories"),
        InlinePanel('related_pages', label="Related pages"),
    ]

    promote_panels = (
        Page.promote_panels +
        SocialFields.promote_panels +
        ListingFields.promote_panels
    )

    subpage_types = []
    parent_page_types = ['NewsIndex']

    @property
    def display_date(self):
        if self.publication_date:
            return self.publication_date
        else:
            return self.first_published_at

    @cached_property
    def categories(self):
        categories = [
            n.category for n in self.category_relationships.all()
        ]
        return categories


class NewsIndexFeaturedPage(RelatedPage):
    source_page = ParentalKey('news.NewsIndex', related_name='featured_pages')

    panels = [
        PageChooserPanel('page', page_type='news.NewsPage'),
    ]


class NewsIndex(Page, SocialFields, ListingFields):
    def get_context(self, request, *args, **kwargs):
        news = NewsPage.objects.live().public().descendant_of(self).annotate(
            date=Coalesce('publication_date', 'first_published_at')
        ).order_by('-date')

        # Pagination
        page_number = request.GET.get('page', 1)
        paginator = Paginator(news, settings.DEFAULT_PER_PAGE)
        try:
            news = paginator.page(page_number)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)

        context = super().get_context(request, *args, **kwargs)
        context.update(
            news=news,
            sidebar_pages=self.get_siblings().live().public(),
        )
        context.update(get_adjacent_pages(paginator, page_number))
        return context

    subpage_types = ['NewsPage']

    content_panels = Page.content_panels + [
        InlinePanel('featured_pages', label='Featured pages'),
    ]

    promote_panels = (
        Page.promote_panels +
        SocialFields.promote_panels +
        ListingFields.promote_panels
    )
