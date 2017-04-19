import coreapi
import coreschema
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from rest_framework.filters import BaseFilterBackend


class GlossaryTermsStartsWithFilter(BaseFilterBackend):
    query_parameter = 'term_startswith'
    query_title = _('First letters')
    query_description = _('One or more first letter of a glossary term')

    def filter_queryset(self, request, queryset, view):
        """
        This performs case-insensitive starts-with filtering on the queryset of GlossaryTerms
        using a value from query `self.query_parameter` query parameter

        Eg: ?term_startswith=abc
        """

        if self.query_parameter in request.GET:
            value = request.GET[self.query_parameter]

            if len(value) > 0:
                queryset = queryset.filter(name__istartswith=value)

        return queryset

    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name=self.query_parameter,
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_text(self.query_title),
                    description=force_text(self.query_description)
                )
            )
        ]
