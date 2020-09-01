from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from hra.utils.models import SocialFields, ListingFields


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
    page = ParentalKey('FAQPage', related_name='faqs', on_delete=models.CASCADE)
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


class FAQPage(Page, SocialFields, ListingFields):
    content_panels = Page.content_panels + [
        InlinePanel('faqs', label="FAQs"),
    ]

    promote_panels = (
        Page.promote_panels +
        SocialFields.promote_panels +
        ListingFields.promote_panels
    )

    subpage_types = []

    class Meta:
        verbose_name = "FAQ page"

    def get_faqs(self):
        return FAQ.objects.filter(faq_entries__page=self).order_by('faq_entries__sort_order')
