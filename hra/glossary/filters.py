from rest_framework.filters import BaseFilterBackend


class GlossaryTermsStartsWithFilter(BaseFilterBackend):
    query_parameter = 'term_startswith'

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
