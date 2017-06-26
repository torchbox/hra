from collections import OrderedDict

from django.db import models
from modelcluster.fields import ParentalManyToManyField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch import index

from hra.utils.models import SocialFields, ListingFields


class ResearchType(models.Model):
    name = models.CharField(max_length=255)

    # Research type (study type) ID from the HARP API.
    # Use it to check if an entry already exists in url local DB
    harp_study_type_id = models.PositiveIntegerField(editable=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'research type'
        verbose_name_plural = 'research types'


# TODO: Add indexes (dates, type, etc)
# TODO: Add ES filters
class ResearchSummaryPage(Page, SocialFields, ListingFields):
    is_creatable = False

    REC_OPINION_CHOICES = OrderedDict((
        ('unfavourable', 'Unfavourable Opinion'),
        ('favourable', 'Favourable Opinion'),
        ('further_unfavourable', 'Further Information Unfavourable Opinion'),
        ('further_favourable', 'Further Information Favourable Opinion'),
    ))
    REC_OPINION_CHOICES_REVERSE = OrderedDict((
        (value, key) for key, value in REC_OPINION_CHOICES.items()
    ))

    # Research summary ID from the HARP API.
    # Use it to check if an entry already exists in url local DB
    harp_application_id = models.PositiveIntegerField(editable=True, unique=True)

    research_types = ParentalManyToManyField('research_summaries.ResearchType')
    full_title = models.TextField(blank=True, editable=False)
    iras_id = models.CharField("IRAS ID", blank=True, max_length=255, editable=True)
    contact_name = models.CharField(max_length=255, blank=True, editable=True)
    contact_email = models.CharField(max_length=255, blank=True, editable=True)
    sponsor_organisation = models.CharField(max_length=255, blank=True, editable=True)
    eudract_number = models.CharField(max_length=255, blank=True, editable=True)
    isrctn_number = models.CharField("ISRCTN Number", max_length=255, blank=True, editable=True)
    clinicaltrials_number = models.CharField("Clinicaltrials.gov Identifier", max_length=255, blank=True, editable=True)
    additional_reference_number_fields = models.TextField(blank=True, editable=True)
    duration_of_study_in_uk = models.CharField("Duration of Study in UK", max_length=255, blank=True, editable=True)
    research_summary_text = models.TextField(blank=True, editable=True)
    rec_name = models.CharField(max_length=255, blank=True, editable=True)
    rec_reference = models.CharField(max_length=255, blank=True, editable=True)
    date_of_rec_opinion = models.DateField(blank=True, null=True, editable=True)
    rec_opinion = models.CharField(choices=REC_OPINION_CHOICES.items(), max_length=64, blank=True, editable=True)
    decision_date = models.DateField(blank=True, null=True, editable=True)

    data_collection_arrangements = models.TextField(blank=True, editable=True)
    research_programme = models.TextField(blank=True, editable=True)
    storage_license = models.CharField(max_length=512, blank=True, editable=True)
    rtb_title = models.CharField("RTBTitle", max_length=512, blank=True, editable=True)
    research_database_title = models.CharField(max_length=255, blank=True, editable=True)
    establishment_organisation = models.CharField(max_length=255, blank=True, editable=True)
    establishment_organisation_address_1 = models.CharField(max_length=255, blank=True, editable=True)
    establishment_organisation_address_2 = models.CharField(max_length=255, blank=True, editable=True)
    establishment_organisation_address_3 = models.CharField(max_length=255, blank=True, editable=True)
    establishment_organisation_address_postcode = models.CharField(max_length=32, blank=True, editable=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    search_fields = Page.search_fields + [
        index.SearchField('full_title', partial_match=True),
        index.SearchField('research_summary_text', partial_match=True),
        index.SearchField('iras_id'),
        index.SearchField('eudract_number'),
        index.SearchField('isrctn_number'),
        index.SearchField('clinicaltrials_number'),
        index.SearchField('additional_reference_number_fields'),
        index.FilterField('date_of_rec_opinion'),
        index.FilterField('updated_at'),
    ]

    promote_panels = (
        Page.promote_panels +
        SocialFields.promote_panels +
        ListingFields.promote_panels
    )

    parent_page_types = ['research_summaries.ResearchSummariesIndexPage']
    subpage_types = []


class ResearchSummariesIndexPage(Page, SocialFields, ListingFields):
    introduction = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
    ]

    promote_panels = (
        Page.promote_panels +
        SocialFields.promote_panels +
        ListingFields.promote_panels
    )

    subpage_types = ['research_summaries.ResearchSummaryPage']

    @classmethod
    def can_create_at(cls, parent):
        """Do not allow to create more than one instance of this page"""
        return super().can_create_at(parent) and not cls.objects.count()
