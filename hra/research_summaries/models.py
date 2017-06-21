from django.db import models
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch import index

from hra.utils.models import SocialFields, ListingFields


# TODO: Move into importer module
mapping = {
    'title': 'ApplicationTitle',
    'full_title': 'ApplicationFullTitle',
    'iras_id': 'IrasProjectID',
    'contact_name': 'ContactName',
    'contact_email': 'ContactEmail',
    'sponsor_organisation': 'SponsorOrganisation',
    'eudract_number': 'EudraCT',
    'isrctn_number': 'ISRCTN',
    'clinicaltrials_number': 'NCT',
    'additional_reference_number_fields': 'AdditionalReferenceNumbers',
    'duration_of_study_in_uk': 'DurationOfStudyInUK',
    'research_summary_text': 'ResearchSummary',
    'rec_name': 'CommitteeName',
    'rec_reference': 'CommitteeReferenceNumber',
    'date_of_rec_opinion': 'DecisionDate',
    'rec_opinion': 'Decision',
    'decision_date': 'DecisionDate',
    'data_collection_arrangements': 'DataCollectionArrangements',
    'research_programme': 'ResearchProgramme',
    'storage_license': 'HumanTissueAuthorityStorageLicence',
    'rtb_title': 'RTBTitle',
    'research_database_title': 'ResearchDatabaseTitle',
    'establishment_organisation': 'EstablishmentOrganisation',
    'establishment_organisation_address_1': 'EstablishmentOrganisationAddress1',
    'establishment_organisation_address_2': 'EstablishmentOrganisationAddress2',
    'establishment_organisation_address_3': 'EstablishmentOrganisationAddress3',
    'establishment_organisation_address_postcode': 'EstablishmentOrganisationPostcode',
}


class ResearchType(models.Model):
    name = models.CharField(max_length=255)

    # Research type (study type) ID from the HARP API.
    # Use it to check if an entry already exists in url local DB
    harp_study_type_id = models.PositiveIntegerField(editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'research type'
        verbose_name_plural = 'research types'


class ResearchSummaryPage(Page, SocialFields, ListingFields):
    REC_OPINION_CHOICES = (
        ('unfavourable_opinion', 'Unfavourable Opinion'),
        ('favourable_opinion', 'Favourable Opinion'),
        ('further_information_favourable_opinion', 'Further Information Favourable Opinion'),
        ('further_information_unfavourable_opinion', 'Further Information Unfavourable Opinion')
    )

    # Research summary ID from the HARP API.
    # Use it to check if an entry already exists in url local DB
    harp_application_id = models.PositiveIntegerField(editable=True)
    research_types = ParentalManyToManyField('research_summaries.ResearchType')

    full_title = models.CharField(max_length=255, blank=True, editable=False)
    iras_id = models.CharField("IRAS ID", blank=True, max_length=255, editable=True)
    contact_name = models.CharField(max_length=255, blank=True, editable=True)
    contact_email = models.EmailField(max_length=255, blank=True, editable=True)
    sponsor_organisation = models.CharField(max_length=255, blank=True, editable=True)
    eudract_number = models.CharField(max_length=255, blank=True, editable=True)
    isrctn_number = models.CharField("ISRCTN Number", max_length=255, blank=True, editable=True)
    clinicaltrials_number = models.CharField("Clinicaltrials.gov Identifier", max_length=255, blank=True, editable=True)
    additional_reference_number_fields = models.CharField(max_length=255, blank=True, editable=True)
    duration_of_study_in_uk = models.CharField("Duration of Study in UK", max_length=255, blank=True, editable=True)
    research_summary_text = models.TextField(blank=True, editable=True)
    rec_name = models.CharField(max_length=255, blank=True, editable=True)
    rec_reference = models.CharField(max_length=255, blank=True, editable=True)
    date_of_rec_opinion = models.DateField(blank=True, null=True, editable=True)
    rec_opinion = models.CharField(choices=REC_OPINION_CHOICES, max_length=64, blank=True, editable=True)
    decision_date = models.DateField(blank=True, null=True, editable=True)

    data_collection_arrangements = models.CharField(max_length=512, blank=True, editable=True)
    research_programme = models.CharField(max_length=512, blank=True, editable=True)
    storage_license = models.CharField(max_length=512, blank=True, editable=True)
    rtb_title = models.CharField("RTBTitle", max_length=512, blank=True, editable=True)
    research_database_title = models.CharField(max_length=255, blank=True, editable=True)
    establishment_organisation = models.CharField(max_length=255, blank=True, editable=True)
    establishment_organisation_address_1 = models.CharField(max_length=255, blank=True, editable=True)
    establishment_organisation_address_2 = models.CharField(max_length=255, blank=True, editable=True)
    establishment_organisation_address_3 = models.CharField(max_length=255, blank=True, editable=True)
    establishment_organisation_address_postcode = models.CharField(max_length=32, blank=True, editable=True)

    search_fields = Page.search_fields + [
        index.SearchField('full_title', partial_match=True),
        index.SearchField('research_summary_text', partial_match=True),
        index.SearchField('iras_id'),
        index.SearchField('eudract_number'),
        index.SearchField('isrctn_number'),
        index.SearchField('clinicaltrials_number'),
        index.SearchField('additional_reference_number_fields'),
        index.FilterField('rec_opinion'),
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

    promote_panels = (
        Page.promote_panels +
        SocialFields.promote_panels +
        ListingFields.promote_panels
    )

    subpage_types = ['research_summaries.ResearchSummaryPage']
