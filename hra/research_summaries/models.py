from collections import OrderedDict

from dateutil.parser import parse as parse_date
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from django.utils.functional import cached_property
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch import index

from hra.utils.models import SocialFields, ListingFields, get_adjacent_pages


class ResearchType(models.Model):
    NON_ALIASED_STUDY_TYPE_IDS = (8, 20)
    ALIAS_NAME = "Research Study"

    name = models.CharField(max_length=255)

    # Research type (study type) ID from the HARP API.
    # Use it to check if an entry already exists in url local DB
    harp_study_type_id = models.PositiveIntegerField(editable=False, unique=True)

    @cached_property
    def display_name(self):
        """
        Only "Research Database" and "Research Tissue Bank"
        research types must be displayed as is.
        All other types should be displayed as "Research Study".
        """

        if self.harp_study_type_id in self.NON_ALIASED_STUDY_TYPE_IDS:
            return self.name

        return self.ALIAS_NAME

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'research type'
        verbose_name_plural = 'research types'


REC_OPINION_CHOICES = OrderedDict((
    ('unfavourable', 'Unfavourable Opinion'),
    ('favourable', 'Favourable Opinion'),
    ('further_unfavourable', 'Further Information Unfavourable Opinion'),
    ('further_favourable', 'Further Information Favourable Opinion'),
))


class ResearchSummaryPage(Page, SocialFields, ListingFields):
    is_creatable = False

    REC_OPINION_CHOICES_REVERSE = OrderedDict((
        (value, key) for key, value in REC_OPINION_CHOICES.items()
    ))

    # Research summary ID from the HARP API.
    # Use it to check if an entry already exists in url local DB
    harp_application_id = models.PositiveIntegerField(editable=True, unique=True)

    research_type = models.ForeignKey('research_summaries.ResearchType', null=True, blank=True,
                                      on_delete=models.SET_NULL, related_name='+')
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
    date_of_rec_opinion = models.DateField(blank=True, null=True, editable=True, db_index=True)
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

    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    # Can't use `auto_now=True`, because we don't want to update this field,
    # when an editor changes something in the admin UI.
    # We should update this field only on import from the API.
    updated_at = models.DateTimeField(db_index=True, editable=True)

    search_fields = Page.search_fields + [
        index.SearchField('full_title', partial_match=True),
        index.SearchField('research_summary_text', partial_match=True),
        index.SearchField('iras_id'),
        index.SearchField('eudract_number'),
        index.SearchField('isrctn_number'),
        index.SearchField('clinicaltrials_number'),
        index.SearchField('additional_reference_number_fields'),
        index.FilterField('research_type'),
        index.FilterField('date_of_rec_opinion'),
        index.FilterField('updated_at'),

        index.FilterField('rec_opinion'),

        index.SearchField('harp_application_id'),
        index.SearchField('contact_name'),
        index.SearchField('contact_email'),
        index.SearchField('sponsor_organisation'),
        index.SearchField('rec_name'),
        index.SearchField('rec_reference'),
        index.SearchField('data_collection_arrangements', partial_match=True),
        index.SearchField('research_programme', partial_match=True),
        index.SearchField('rtb_title', partial_match=True),
        index.SearchField('research_database_title'),
        index.SearchField('establishment_organisation', partial_match=True),
        index.SearchField('establishment_organisation_address_1'),
        index.SearchField('establishment_organisation_address_2'),
        index.SearchField('establishment_organisation_address_3'),
        index.SearchField('establishment_organisation_address_postcode'),
    ]

    promote_panels = (
        Page.promote_panels +
        SocialFields.promote_panels +
        ListingFields.promote_panels
    )

    parent_page_types = ['research_summaries.ResearchSummariesIndexPage']
    subpage_types = []

    def __init__(self, *args, **kwargs):
        super(ResearchSummaryPage, self).__init__(*args, **kwargs)

        # Some of the fields have one or more spaces in them, need to trim them
        # so we can evaluate whether they are empty with not operator.
        for field in self._meta.get_fields():
            # Skip non-textual fields
            if not isinstance(field, (models.CharField, models.TextField)):
                continue

            if isinstance(getattr(self, field.name), str):
                stripped_value = getattr(self, field.name).strip()
                setattr(self, field.name, stripped_value)

    @cached_property
    def display_date(self):
        return self.decision_date

    @cached_property
    def display_research_type(self):
        if not self.research_type:
            return None

        return self.research_type.display_name


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

    @cached_property
    def _children_research_summary(self):
        return ResearchSummaryPage.objects.live().public().descendant_of(self)

    @cached_property
    def updated_at(self):
        latest_page = self._children_research_summary.order_by('-updated_at').first()

        latest_date = None
        if latest_page:
            latest_date = latest_page.updated_at

        return latest_date

    def get_context(self, request, *args, **kwargs):
        search_date_from = request.GET.get('date_from', None)
        search_date_to = request.GET.get('date_to', None)
        search_research_type = request.GET.get('research_type', None)
        search_rec_opinion = request.GET.get('rec_opinion', None)
        search_query = request.GET.get('query', None)
        page_number = request.GET.get('page', 1)

        search_results = self._children_research_summary

        # Convert dates to the Python format
        if search_date_from:
            try:
                # Can return None or raise ValueError in case of bad format
                search_date_from = parse_date(search_date_from, dayfirst=True).date()
            except ValueError:
                search_date_from = None

        if search_date_to:
            try:
                # Can return None or raise ValueError in case of bad format
                search_date_to = parse_date(search_date_to, dayfirst=True).date()
            except ValueError:
                search_date_to = None

        # Swap dates around if "date from" happens after "date to".
        if search_date_from and search_date_to:
            if search_date_from > search_date_to:
                    search_date_to, search_date_from = search_date_from, search_date_to

        # Search queryset
        if search_date_to:
            search_results = search_results.filter(date_of_rec_opinion__lte=search_date_to)

        if search_date_from:
            search_results = search_results.filter(date_of_rec_opinion__gte=search_date_from)

        # Research types to be displayed as is
        non_aliased_research_types = dict(
            ResearchType.objects.filter(
                harp_study_type_id__in=ResearchType.NON_ALIASED_STUDY_TYPE_IDS
            ).values_list('pk', 'name')
        )
        # Add the alias for rest research types
        alias_fake_id = 0
        display_research_types = non_aliased_research_types.copy()
        display_research_types.update({
            alias_fake_id: ResearchType.ALIAS_NAME,
        })

        try:
            search_research_type = int(search_research_type)

            if search_research_type == alias_fake_id:
                search_results = search_results.exclude(research_type__in=non_aliased_research_types.keys())
            elif search_research_type in non_aliased_research_types.keys():
                search_results = search_results.filter(research_type=search_research_type)
        except (TypeError, ValueError):
            pass

        # rec opinion filter
        if search_rec_opinion:
            search_results = search_results.filter(rec_opinion=search_rec_opinion)

        if search_query:
            search_results = search_results.search(search_query, operator='and')

        # Pagination
        paginator = Paginator(search_results, settings.DEFAULT_PER_PAGE)
        try:
            search_results = paginator.page(page_number)
        except PageNotAnInteger:
            search_results = paginator.page(1)
        except EmptyPage:
            search_results = paginator.page(paginator.num_pages)

        context = super().get_context(request, *args, **kwargs)
        context.update({
            'search_research_type': search_research_type,
            'search_rec_opinion': search_rec_opinion,
            'search_query': search_query,
            'search_results': search_results,
            'display_research_types': display_research_types,
            'search_date_from': search_date_from,
            'search_date_to': search_date_to,
            'rec_opinions': REC_OPINION_CHOICES,
        })
        context.update(get_adjacent_pages(paginator, page_number))

        return context
