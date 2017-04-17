from wagtail.api.v2.endpoints import BaseAPIEndpoint
from wagtail.api.v2.filters import FieldsFilter, OrderingFilter, SearchFilter

from .models import GlossaryTerm
from .serializers import GlossaryTermSerializer


class GlossaryTermsAPIEndpoint(BaseAPIEndpoint):
    base_serializer_class = GlossaryTermSerializer
    filter_backends = [FieldsFilter, OrderingFilter, SearchFilter]
    body_fields = BaseAPIEndpoint.body_fields + ['name', 'description', 'is_noun']
    listing_default_fields = BaseAPIEndpoint.listing_default_fields + ['name', 'description', 'is_noun']
    nested_default_fields = BaseAPIEndpoint.nested_default_fields + ['name']
    name = 'glossary_terms'
    model = GlossaryTerm
