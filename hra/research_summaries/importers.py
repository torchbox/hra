from dateutil.parser import parse as parse_date
from django.utils import timezone

from hra.research_summaries.mappings import FieldMapping, ForeignKeyMapping
from hra.research_summaries.models import ResearchSummaryPage, ResearchType


DEFERRED = 'Publication of this data is currently deferred.'
NOT_APPLICABLE = 'N/A'


class PageImporter:
    model = None
    id_mapping = None
    mappings = []

    def __init__(self, data):
        self.data = data

    def _set_fields(self, page):
        mappings = [self.id_mapping] + self.mappings

        for mapping in mappings:
            mapping.set_field(page, self.data)

    def get_page(self, parent):
        qs = self.model.objects.child_of(parent)
        qs = qs.filter(**{
            self.id_mapping.dest: self.id_mapping.get_field_data(self.data)
        })

        return qs.first()

    def create_or_update_page(self, parent):
        page = self.get_page(parent)

        if page:
            # Update existing page
            self._set_fields(page)
            page.save_revision().publish()
        else:
            # Create a new page
            page = self.model()
            self._set_fields(page)
            page = parent.add_child(instance=page)
            page.save_revision(changed=False)

        return page


def get_decision_date(data):
    # Ignore decision date if publication deferred
    if data['DecisionDate'] and data['DecisionDate'] not in (DEFERRED, NOT_APPLICABLE,):
        return parse_date(data['DecisionDate'])
    return None


def get_study_type(data):
    # Ignore study type if id or name are publication deferred
    if data['StudyTypeID'] and data['StudyTypeID'] != DEFERRED and data['StudyType'] != DEFERRED:
        return {
            'StudyTypeID': data['StudyTypeID'],
            'StudyType': data['StudyType'] or '',
        }
    return None


class ResearchSummaryPageImporter(PageImporter):
    model = ResearchSummaryPage
    id_mapping = FieldMapping('harp_application_id', source='ApplicationID')
    mappings = PageImporter.mappings + [
        FieldMapping('title', source=lambda data: data['ApplicationTitle'].strip() or data['ApplicationID']),
        FieldMapping('full_title', source=lambda data: data['ApplicationFullTitle'] or ''),
        FieldMapping('iras_id', source=lambda data: data['IrasProjectID'] or ''),
        FieldMapping('contact_name', source=lambda data: data['ContactName'] or ''),
        FieldMapping('contact_email', source=lambda data: data['ContactEmail'] or ''),
        FieldMapping('sponsor_organisation', source=lambda data: data['SponsorOrganisation'] or ''),
        FieldMapping('eudract_number', source=lambda data: data['EudraCT'] or ''),
        FieldMapping('isrctn_number', source=lambda data: data['ISRCTN'] or ''),
        FieldMapping('clinicaltrials_number', source=lambda data: data['NCT'] or ''),
        FieldMapping(
            'additional_reference_number_fields',
            source=lambda data: data['AdditionalReferenceNumbers'] or ''
        ),
        FieldMapping('duration_of_study_in_uk', source=lambda data: data['DurationOfStudyInUK'] or ''),
        FieldMapping('research_summary_text', source=lambda data: data['ResearchSummary'] or ''),
        FieldMapping('rec_name', source=lambda data: data['CommitteeName'] or ''),
        FieldMapping('rec_reference', source=lambda data: data['CommitteeReferenceNumber'] or ''),
        FieldMapping('date_of_rec_opinion', source=get_decision_date),
        FieldMapping(
            'rec_opinion',
            source=lambda data: ResearchSummaryPage.REC_OPINION_CHOICES_REVERSE.get(data['Decision'], '')
        ),
        FieldMapping('data_collection_arrangements', source=lambda data: data['DataCollectionArrangements'] or ''),
        FieldMapping('research_programme', source=lambda data: data['ResearchProgramme'] or ''),
        FieldMapping('storage_license', source=lambda data: data['HumanTissueAuthorityStorageLicence'] or ''),
        FieldMapping('rtb_title', source=lambda data: data['RTBTitle'] or ''),
        FieldMapping('research_database_title', source=lambda data: data['ResearchDatabaseTitle'] or ''),
        FieldMapping('establishment_organisation', source=lambda data: data['EstablishmentOrganisation'] or ''),
        FieldMapping(
            'establishment_organisation_address_1',
            source=lambda data: data['EstablishmentOrganisationAddress1'] or ''
        ),
        FieldMapping(
            'establishment_organisation_address_2',
            source=lambda data: data['EstablishmentOrganisationAddress2'] or ''
        ),
        FieldMapping(
            'establishment_organisation_address_3',
            source=lambda data: data['EstablishmentOrganisationAddress3'] or ''
        ),
        FieldMapping(
            'establishment_organisation_address_postcode',
            source=lambda data: data['EstablishmentOrganisationPostcode'] or ''
        ),
        ForeignKeyMapping(
            'research_type',
            id_mapping=FieldMapping('harp_study_type_id', source='StudyTypeID'),
            mappings=[
                FieldMapping('name', source='StudyType')
            ],
            cls=ResearchType,
            source=get_study_type,
        ),
        FieldMapping(
            'updated_at',
            source=lambda data: timezone.now()
        ),
    ]
