from django.db import models
from django.db.models.functions import Coalesce
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import (
    StreamFieldPanel, FieldPanel, InlinePanel
)
from wagtail.wagtailsearch import index

from hra.utils.models import (
    ListingFields, SocialFields, RelatedPage,
    RelatedDocument
)
from hra.utils.blocks import StoryBlock


class NewsPageCategory(models.Model):
    page = ParentalKey(
        'news.NewsPage',
        related_name='categories'
    )
    category = models.ForeignKey(
        'categories.Category',
        related_name='+',
        on_delete=models.CASCADE
    )

    panels = [
        SnippetChooserPanel('category')
    ]


class NewsPageRelatedDocument(RelatedDocument):
    page = ParentalKey(
        'news.NewsPage',
        related_name='related_documents'
    )


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
    introduction = models.TextField(blank=True)
    body = StreamField(StoryBlock())

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
        index.SearchField('body')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('publication_date'),
        FieldPanel('introduction'),
        StreamFieldPanel('body'),
        InlinePanel('categories', label="Categories"),
        InlinePanel('related_documents', label="Related documents"),
        InlinePanel('related_pages', label="Related pages"),
    ]

    promote_panels = Page.promote_panels + SocialFields.promote_panels + \
        ListingFields.promote_panels

    subpage_types = []
    parent_page_types = ['NewsIndex']

    @property
    def display_date(self):
        if self.publication_date:
            return self.publication_date
        else:
            return self.first_published_at


class NewsIndex(Page, SocialFields):
    def get_context(self, request, *args, **kwargs):
        news = NewsPage.objects.live().public().descendant_of(self).annotate(
            date=Coalesce('publication_date', 'first_published_at')
        ).order_by('-date')

        if request.GET.get('category'):
            news = news.filter(categories=request.GET.get('category'))

        # Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(news, settings.DEFAULT_PER_PAGE)
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)

        context = super().get_context(request, *args, **kwargs)
        context.update(
            news=news,
            # Only show categories that have been used
            categories=NewsPageCategory.objects.all().values_list(
                'category__pk', 'category__name'
            ).distinct()
        )
        return context

    subpage_types = ['NewsPage']
    parent_page_types = ['home.HomePage']