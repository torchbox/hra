from django.db import models
from django.utils import timezone
from django.utils.datetime_safe import date
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

from hra.utils.datetime import range_month


@register_snippet
class CommitteeType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'committee type'
        verbose_name_plural = 'committee types'


@register_snippet
class CommitteeFlag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'committee flag'
        verbose_name_plural = 'committee flags'


class CommitteePagePreviousName(Orderable):
    source_page = ParentalKey('rec.CommitteePage', related_name='previous_names')
    name = models.CharField(max_length=255)


class CommitteePagePhone(Orderable):
    source_page = ParentalKey('rec.CommitteePage', related_name='phone_numbers')
    phone = models.CharField(max_length=255)


class CommitteePageEmail(Orderable):
    source_page = ParentalKey('rec.CommitteePage', related_name='email_addresses')
    email = models.EmailField(max_length=255)


class CommitteePageMeetingDate(models.Model):
    source_page = ParentalKey('rec.CommitteePage', related_name='meeting_dates')
    date = models.DateField()

    class Meta:
        ordering = ['date']


class CommitteePageType(Orderable):
    source_page = ParentalKey('rec.CommitteePage', related_name='committee_types')
    committee_type = models.ForeignKey('rec.CommitteeType', related_name='+')

    panels = [
        SnippetChooserPanel('committee_type')
    ]


class CommitteePageFlag(Orderable):
    source_page = ParentalKey('rec.CommitteePage', related_name='committee_flags')
    committee_flag = models.ForeignKey('rec.CommitteeFlag', related_name='+')

    panels = [
        SnippetChooserPanel('committee_flag')
    ]


class CommitteePage(Page):
    """REC - Research Ethics Committee"""
    REGION_CHOICES = (
        ('east_midlands', 'East Midlands'),
        ('east_of_england', 'East of England'),
        ('england', 'England'),
        ('london', 'London'),
        ('north_east', 'North East'),
        ('north_west', 'North West'),
        ('northern_ireland', 'Northern Ireland'),
        ('scotland', 'Scotland'),
        ('social_care_institute_for_excellence', 'Social Care Institute for Excellence'),
        ('south_central', 'South Central'),
        ('south_east_coast', 'South East Coast'),
        ('south_west', 'South West'),
        ('wales', 'Wales'),
        ('west_midlands', 'West Midlands'),
        ('yorkshire_and_the_humber', 'Yorkshire & the Humber'),
    )

    chair = models.CharField(max_length=255, blank=True)
    rec_manager = models.CharField("REC Manager", max_length=255, blank=True)
    rec_assistant = models.CharField("REC Assistant", max_length=255, blank=True)
    hra_office_name = models.CharField("HRA Office name", max_length=255, blank=True)
    region = models.CharField("Region/Nation", max_length=64, choices=REGION_CHOICES)
    usual_meeting_venue = models.CharField(max_length=255, blank=True)
    usual_meeting_time = models.TimeField(blank=True, null=True)

    content_panels = Page.content_panels + [
        InlinePanel('previous_names', label="Previous name of REC"),
        FieldPanel('chair'),
        FieldPanel('rec_manager'),
        FieldPanel('rec_assistant'),
        InlinePanel('phone_numbers', label="Phone numbers"),
        InlinePanel('email_addresses', label="Email addresses"),
        FieldPanel('hra_office_name'),
        FieldPanel('region'),
        FieldPanel('usual_meeting_venue'),
        FieldPanel('usual_meeting_time'),
        InlinePanel('meeting_dates', label="Meeting dates"),
        InlinePanel('committee_types', label="Committee Types"),
        InlinePanel('committee_flags', label="Committee Flags"),
    ]

    parent_page_types = ['rec.CommitteeIndexPage']
    subpage_types = []


class CommitteeIndexPage(Page):

    introduction = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname='full'),
    ]

    subpage_types = ['rec.CommitteePage']

    def get_context(self, request, *args, **kwargs):
        selected_committee_flag_pks = request.GET.getlist('committee_flag', None)

        committee_pages = CommitteePage.objects.live().public().descendant_of(self)
        committee_flags = CommitteeFlag.objects.all()

        # Allow to filter by committee flags
        selected_committee_flags = committee_flags.filter(pk__in=selected_committee_flag_pks)
        selected_committee_flag_pks = [flag.pk for flag in selected_committee_flags]
        if selected_committee_flag_pks:
            committee_pages = committee_pages.filter(committee_flags__pk__in=selected_committee_flag_pks)

        # Exclude duplicates
        committee_pages = committee_pages.distinct()

        start_and_end_dates = committee_pages.filter(
            meeting_dates__date__gte=timezone.now().date()
        ).aggregate(
            start_date=models.Min('meeting_dates__date'),
            end_date=models.Max('meeting_dates__date'),
        )

        calendar_matrix = []

        dates_range = range_month(start_and_end_dates['start_date'], start_and_end_dates['end_date'])

        if dates_range and committee_pages:
            for meeting_month in dates_range:
                all_meetings = []

                for committee in committee_pages:
                    committee_meetings = committee.meeting_dates.filter(
                        date__year=meeting_month.year,
                        date__month=meeting_month.month,
                    ).values_list('date', flat=True)

                    all_meetings.append(committee_meetings)

                calendar_matrix.append(
                    (meeting_month, all_meetings)
                )

        context = super().get_context(request, *args, **kwargs)
        context.update({
            'committee_pages': committee_pages,
            'calendar_matrix': calendar_matrix,
            'committee_flags': committee_flags,
            'selected_committee_flag_pks': selected_committee_flag_pks,
        })

        return context
