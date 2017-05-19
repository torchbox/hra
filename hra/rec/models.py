from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet


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
