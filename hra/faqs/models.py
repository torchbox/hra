from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

from hra.utils.models import SocialFields


@register_snippet
class FAQ(index.Indexed, models.Model):
    title = models.CharField(max_length=255)
    body = RichTextField(blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('body'),
    ]

    search_fields = [
        index.SearchField('title'),
        index.SearchField('body'),
    ]

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.title


class FAQPageItem(Orderable):
    page = ParentalKey('FAQPage', related_name='faqs')
    faq = models.ForeignKey(
        'FAQ',
        on_delete=models.CASCADE,
        related_name='faq_entries'
    )

    panels = [
        SnippetChooserPanel('faq'),
    ]

    def __str__(self):
        return self.page.title + ": " + self.faq.title


class FAQPage(Page, SocialFields):
    content_panels = Page.content_panels + [
        InlinePanel('faqs', label="FAQs"),
    ]

    promote_panels = Page.promote_panels + SocialFields.promote_panels

    subpage_types = []

    class Meta:
        verbose_name = "FAQ page"

    def get_faqs(self):
        return FAQ.objects.filter(faq_entries__page=self)
