from django.db import models
from django.utils import timezone
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

from hra.utils.datetime import range_month
from hra.utils.models import SocialFields, ListingFields


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

    def __str__(self):
        return self.name


class CommitteePagePhone(Orderable):
    source_page = ParentalKey('rec.CommitteePage', related_name='phone_numbers')
    phone = models.CharField(max_length=255)

    def __str__(self):
        return self.phone


class CommitteePageEmail(Orderable):
    source_page = ParentalKey('rec.CommitteePage', related_name='email_addresses')
    email = models.EmailField(max_length=255)

    def __str__(self):
        return self.email


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


class CommitteePage(Page, SocialFields, ListingFields):
    """REC - Research Ethics Committee"""
    REGION_CHOICES = (
        ('east_midlands', 'East Midlands'),
        ('east_of_england', 'East of England'),
        ('london', 'London'),
        ('north_east', 'North East'),
        ('north_west', 'North West'),
        ('northern_ireland', 'Northern Ireland'),
        ('scotland', 'Scotland'),
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
    approvals_officer = models.CharField("Approvals Officer", max_length=255, blank=True)
    approvals_administrator = models.CharField("Approvals Administrator", max_length=255, blank=True)
    region = models.CharField("Region/Nation", max_length=64, choices=REGION_CHOICES)
    usual_meeting_venue = models.CharField(max_length=255, blank=True)
    usual_meeting_time = models.TimeField(blank=True, null=True)

    search_fields = Page.search_fields + [
        index.SearchField('chair'),
        index.SearchField('rec_manager'),
        index.SearchField('rec_assistant'),
        index.SearchField('approvals_officer'),
        index.SearchField('approvals_administrator'),
        index.FilterField('region'),
        index.SearchField('usual_meeting_venue'),
    ]

    content_panels = Page.content_panels + [
        InlinePanel('previous_names', label="Previous name of REC"),
        FieldPanel('chair'),
        MultiFieldPanel([
            FieldPanel('rec_manager'),
            FieldPanel('rec_assistant'),
        ], heading='REC'),
        MultiFieldPanel([
            FieldPanel('approvals_officer'),
            FieldPanel('approvals_administrator'),
        ], heading='Approvals'),
        InlinePanel('phone_numbers', label="Phone numbers"),
        InlinePanel('email_addresses', label="Email addresses"),
        FieldPanel('region'),
        FieldPanel('usual_meeting_venue'),
        FieldPanel('usual_meeting_time'),
        InlinePanel('meeting_dates', label="Meeting dates"),
        InlinePanel('committee_types', label="Committee Types"),
        InlinePanel('committee_flags', label="Committee Flags"),
    ]

    promote_panels = (
        Page.promote_panels +
        SocialFields.promote_panels +
        ListingFields.promote_panels
    )

    parent_page_types = ['rec.CommitteeIndexPage']
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        meeting_dates = self.meeting_dates.all()
        # We have to do that instead of just meeting_dates.filter(date__gte=timezone.now().date())
        # Because it will not work on preview in the Wagtail admin
        today = timezone.now().date()
        meeting_dates = [meeting_date for meeting_date in meeting_dates if meeting_date.date >= today]

        context.update({
            'upcoming_meeting_dates': meeting_dates
        })

        return context


class CommitteeIndexPage(Page, SocialFields, ListingFields):

    introduction = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname='full'),
    ]

    promote_panels = (
        Page.promote_panels +
        SocialFields.promote_panels +
        ListingFields.promote_panels
    )

    subpage_types = ['rec.CommitteePage']

    def get_context(self, request, *args, **kwargs):
        # Get all filtering values from a request
        selected_committee_flag_pks = request.GET.getlist('committee_flag', None)
        selected_committee_type_pk = request.GET.get('committee_type', None)
        selected_committee_region = request.GET.get('committee_region', None)
        search_query = request.GET.get('query', None)

        # Get all initial objects values
        # Prefetch meeting dates to avoid repeatedly hitting the database when generating matrix
        committee_pages = CommitteePage.objects.live().public().descendant_of(self).prefetch_related('meeting_dates')
        committee_flags = CommitteeFlag.objects.all()
        committee_types = CommitteeType.objects.all()
        committee_region_choices = CommitteePage.REGION_CHOICES

        # Perform full text search, if a search query is present in the request
        if search_query:
            search_results = committee_pages.search(search_query, operator='and')

            # At the moment, we use the ElasticSearch search backend,
            # so the `search` method returns an ElasticsearchSearchResults object
            # We can't do the further processing (filtering, start and end dates) on this object,
            # so we should convert it back into QuerySet.
            # Note: we don't care about search ordering here.
            committee_pages = committee_pages.filter(pk__in=[page.pk for page in search_results])

        # Filter by committee flags, if present in the request
        if selected_committee_flag_pks:
            try:
                selected_committee_flag_pks = \
                    set(int(pk) for pk in selected_committee_flag_pks) & \
                    set(obj.pk for obj in committee_flags)
                if selected_committee_flag_pks:
                    committee_pages = committee_pages.filter(
                        committee_flags__committee_flag__pk__in=selected_committee_flag_pks
                    )
            except ValueError:
                pass

        # Filter by committee types, if present in the request
        if selected_committee_type_pk:
            try:
                selected_committee_type_pk = int(selected_committee_type_pk)
                if selected_committee_type_pk in (obj.pk for obj in committee_types):
                    committee_pages = committee_pages.filter(
                        committee_types__committee_type__pk=selected_committee_type_pk
                    )
            except ValueError:
                pass

        # Filter by committee region, if present in the request
        if selected_committee_region in (key for key, _ in committee_region_choices):
            committee_pages = committee_pages.filter(region=selected_committee_region)

        # Exclude duplicates after filtering
        committee_pages = committee_pages.distinct()

        # Get the first and last dates to show
        start_date = timezone.now().date()
        end_date_qs = committee_pages.aggregate(end_date=models.Max('meeting_dates__date'))
        # Start and end with this month if no meetings or last meeting is before this month
        end_date = max(start_date, end_date_qs['end_date'] or start_date)

        # Build a matrix for front-end
        calendar_matrix = []
        if committee_pages:
            for meeting_month in range_month(start_date, end_date):
                all_meetings = []

                for committee in committee_pages:
                    # Rather inefficient to sweep through these for every month in range
                    # But a lot easier to comprehend
                    committee_meetings = [
                        meeting.date
                        for meeting in committee.meeting_dates.all()
                        if meeting.date.year == meeting_month.year and
                        meeting.date.month == meeting_month.month
                    ]

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
            'committee_types': committee_types,
            'selected_committee_type_pk': selected_committee_type_pk,
            'committee_region_choices': committee_region_choices,
            'selected_committee_region': selected_committee_region,
            'search_query': search_query,
        })

        return context
