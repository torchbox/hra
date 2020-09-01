from django.core.exceptions import ValidationError
from django.db import models

from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    PageChooserPanel
)
from wagtail.core.models import Orderable, Page
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.contrib.settings.models import BaseSetting, register_setting


class LinkFields(models.Model):
    """
    Adds fields for internal and external links with some methods to simplify the rendering:

    {% if page.link_page %}
        <a href="{% pageurl page.link_page %}">{{ page.get_link_text }}</a>
    {% elif page.link_url  %}
        <a href="{{ page.link_url }}">{{ page.get_link_text }}</a>
    {% endif %}
    """

    link_page = models.ForeignKey(
        Page,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    link_url = models.URLField(blank=True)
    link_text = models.CharField(blank=True, max_length=255)

    class Meta:
        abstract = True

    def clean(self):
        if not self.link_page and not self.link_url:
            raise ValidationError({
                'link_url': ValidationError("You must specify link page or link url."),
                'link_page': ValidationError("You must specify link page or link url."),
            })

        if self.link_page and self.link_url:
            raise ValidationError({
                'link_url': ValidationError("You must specify link page or link url. You can't use both."),
                'link_page': ValidationError("You must specify link page or link url. You can't use both."),
            })

        if not self.link_page and not self.link_text:
            raise ValidationError({
                'link_text': ValidationError("You must specify link text, if you use the link url field."),
            })

    def get_link_text(self):
        if self.link_text:
            return self.link_text

        if self.link_page:
            return self.link_page.title

        return ''

    def get_link_url(self):
        if self.link_page:
            return self.link_page.url

        return self.link_url

    panels = [
        MultiFieldPanel([
            PageChooserPanel('link_page'),
            FieldPanel('link_url'),
            FieldPanel('link_text'),
        ], 'Link'),
    ]


# Related pages
class RelatedPage(Orderable, models.Model):
    page = models.ForeignKey('wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    class Meta:
        abstract = True
        ordering = ['sort_order']

    panels = [
        PageChooserPanel('page'),
    ]


# Related documents
class RelatedDocument(Orderable, models.Model):
    title = models.CharField(max_length=255, help_text="Document name")
    document = models.ForeignKey('wagtaildocs.Document', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text="Please upload related documents")

    class Meta:
        abstract = True
        ordering = ['sort_order']

    panels = [
        FieldPanel('title'),
        DocumentChooserPanel('document'),
    ]


# Generic social fields abstract class to add social image/text to any new content type easily.
class SocialFields(models.Model):
    social_image = models.ForeignKey('images.CustomImage', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    social_text = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True

    promote_panels = [
        MultiFieldPanel([
            ImageChooserPanel('social_image'),
            FieldPanel('social_text'),
        ], 'Social networks'),
    ]


# Generic listing fields abstract class to add listing image/text to any new content type easily.
class ListingFields(models.Model):
    listing_image = models.ForeignKey(
        'images.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Choose the image you wish to be displayed when this page appears in listings"
    )
    listing_title = models.CharField(max_length=255, blank=True, help_text="Override the page title used when this page appears in listings")
    listing_summary = models.CharField(max_length=255, blank=True, help_text="The text summary used when this page appears in listings. It's also used as the description for search engines if the 'Search description' field above is not defined.")

    class Meta:
        abstract = True

    promote_panels = [
        MultiFieldPanel([
            ImageChooserPanel('listing_image'),
            FieldPanel('listing_title'),
            FieldPanel('listing_summary'),
        ], 'Listing information'),
    ]


@register_snippet
class CallToActionSnippet(LinkFields):
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True, max_length=255)
    image = models.ForeignKey('images.CustomImage', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    panels = [
        FieldPanel('title'),
        FieldPanel('summary'),
    ] + LinkFields.panels + [
        ImageChooserPanel('image'),
    ]

    def __str__(self):
        return self.title


@register_setting
class SocialMediaSettings(BaseSetting):
    twitter_handle = models.CharField(
        max_length=255,
        blank=True,
        default='hra_latest',
        help_text='Your Twitter username without the @, e.g. katyperry',
    )
    facebook_app_id = models.CharField(
        max_length=255,
        blank=True,
        help_text='Your Facebook app ID.',
    )
    linkedin_company_id = models.CharField(
        max_length=255,
        blank=True,
        default='health-research-authority',
        help_text='The bit after http://linkedin.com/company/ in your LinkedIn page URL',
    )
    youtube_channel_id = models.CharField(
        max_length=255,
        blank=True,
        default='UCdRaMooWKtc3YM5gkpB2FaA',
        help_text='The bit after https://www.youtube.com/channel/ in your YouTube channel URL',
    )
    default_sharing_text = models.CharField(
        max_length=255,
        blank=True,
        help_text='Default sharing text to use if social text has not been set on a page.',
    )
    site_name = models.CharField(
        max_length=255,
        blank=True,
        default='Health Research Authority',
        help_text='Site name, used by Open Graph.',
    )


def get_adjacent_pages(paginator, page_number):
    adjacent_pages = 2
    if paginator.num_pages <= 2 * adjacent_pages + 3:
        page_numbers = range(1, paginator.num_pages + 1)
    else:
        page_numbers = [
            n for n in
            range(int(page_number) - adjacent_pages,
                  int(page_number) + adjacent_pages + 1)
            if n > 0 and n <= paginator.num_pages
        ]
    show_first = 1 not in page_numbers
    show_last = paginator.num_pages not in page_numbers

    return {
        'page_numbers': page_numbers,
        'show_first': show_first,
        'show_first_hellip': show_first and 2 not in page_numbers,
        'show_last': show_last,
        'show_last_hellip': show_last and (paginator.num_pages - 1) not in page_numbers,
    }
