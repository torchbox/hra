from collections import defaultdict

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel,
    PageChooserPanel)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from hra.utils.blocks import StoryBlock
from hra.utils.models import ListingFields, RelatedPage, SocialFields, get_adjacent_pages


@register_snippet
class EventType(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextField(help_text="This isn't currently shown "
                                "publicly, but could be in the future")

    def __str__(self):
        return self.title


class EventPageRelatedPage(RelatedPage):
    source_page = ParentalKey('events.EventPage', related_name='related_pages', on_delete=models.CASCADE)


class EventPageEventType(models.Model):
    event_type = models.ForeignKey(
        'events.EventType',
        on_delete=models.CASCADE
    )
    page = ParentalKey('events.EventPage', related_name='event_types', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('event_type'),
    ]


class EventPage(Page, SocialFields, ListingFields):
    start_date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    # Permit null=True on end_date, as we use Coalesce to query 'end_date or start_date'
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    street_address_1 = models.CharField(_('Street Address 1'), blank=True, max_length=255)
    street_address_2 = models.CharField(_('Street Address 2'), blank=True, max_length=255)
    city = models.CharField(_('City'), blank=True, max_length=255)
    region = models.CharField(_('State or county'), blank=True, max_length=255)
    postcode = models.CharField(_('Zip or postal code'), blank=True, max_length=255)
    country = models.CharField(_('Country'), blank=True, max_length=255)
    phone = models.CharField(_('Phone'), blank=True, max_length=255)

    introduction = RichTextField(blank=True)
    body = StreamField(StoryBlock())

    subpage_types = []
    parent_page_types = ['events.EventIndexPage']

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [FieldRowPanel([
                FieldPanel('start_date'),
                FieldPanel('start_time'),
            ])],
            heading='Start'
        ),
        MultiFieldPanel(
            [FieldRowPanel([
                FieldPanel('end_date'),
                FieldPanel('end_time'),
            ])],
            heading='End'
        ),
        InlinePanel('event_types', label="Event types"),

        MultiFieldPanel([
            FieldPanel('street_address_1'),
            FieldPanel('street_address_2'),
            FieldPanel('city'),
            FieldPanel('region'),
            FieldPanel('postcode'),
            FieldPanel('country'),
            FieldPanel('phone'),
        ], _('Location')),

        FieldPanel('introduction'),
        StreamFieldPanel('body'),

        InlinePanel('related_pages', label="Related pages"),
    ]

    promote_panels = (
        Page.promote_panels +
        SocialFields.promote_panels +
        ListingFields.promote_panels
    )

    def clean_fields(self, exclude=None):
        errors = defaultdict(list)
        try:
            super().clean_fields(exclude)
        except ValidationError as e:
            errors.update(e.message_dict)

        # Require start time if there's an end time
        if self.end_time and not self.start_time:
            errors["start_time"].append(_("If you enter an end time, you must also enter a start time"))

        if self.end_date and self.end_date < self.start_date:
            errors["end_date"].append(_("Events involving time travel are not supported"))
        elif self.end_date == self.start_date and self.end_time and self.end_time < self.start_time:
            errors["end_time"].append(_("Events involving time travel are not supported"))

        if errors:
            raise ValidationError(errors)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Access siblings like this to get the same order as on the index page
        context['sidebar_pages'] = self.get_parent().specific.upcoming_events

        return context


class EventIndexPageFeaturedPage(RelatedPage):
    source_page = ParentalKey('events.EventIndexPage', related_name='featured_pages', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('page', page_type='events.EventPage'),
    ]


class EventIndexPage(Page, SocialFields, ListingFields):
    subpage_types = ['events.EventPage']

    content_panels = Page.content_panels + [
        InlinePanel('featured_pages', label='Featured pages'),
    ]

    promote_panels = (
        Page.promote_panels +
        SocialFields.promote_panels +
        ListingFields.promote_panels
    )

    def _annotated_descendant_events(self):
        return (
            EventPage.objects
            .live().public().descendant_of(self)
            .annotate(latest_date=Coalesce('end_date', 'start_date'))
        )

    @cached_property
    def upcoming_events(self):
        return (
            self._annotated_descendant_events()
            .filter(latest_date__gte=timezone.now().date())
            .order_by('start_date')
        )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Get all events to display on an event index page.
        # Apply ascending order by start_date to upcoming events,
        # but for past events apply descending ordering by start_date.
        date_now = timezone.now().date()
        events = self._annotated_descendant_events()
        events = events.annotate(
            upcoming_order=models.Case(
                models.When(latest_date__gte=date_now, then='start_date'),
                default=models.Value(None),
                output_field=models.DateField()
            )
        )
        events = events.annotate(
            past_order=models.Case(
                models.When(latest_date__lt=date_now, then='start_date'),
                default=models.Value(None),
                output_field=models.DateField()
            )
        )
        events = events.order_by('upcoming_order', '-past_order')

        paginator = Paginator(events, settings.DEFAULT_PER_PAGE)
        try:
            events = paginator.page(request.GET.get('page'))
        except PageNotAnInteger:
            events = paginator.page(1)
        except EmptyPage:
            events = paginator.page(paginator.num_pages)

        context.update({
            'events': events,
            'sidebar_pages': self.get_siblings().live().public(),
        })
        context.update(get_adjacent_pages(paginator, events.number))

        return context
