from collections import OrderedDict

from django.db.models import Count
from django.db.models.functions import Substr, Lower
from rest_framework.pagination import BasePagination
from rest_framework.response import Response


class GlossaryTermsPagination(BasePagination):
    query_parameter = 'term_startswith'

    def paginate_queryset(self, queryset, request, view=None):
        """
        We do not need pagination, but need some additional information
        after filtering like total count.
        """

        self.view = view
        self.total_count = queryset.count()

        self.count_per_letter = None
        if not request.GET:
            # Get count by first letter
            count_queryset = queryset.annotate(letter=Lower(Substr('name', 1, 1))).values('letter')
            count_queryset = count_queryset.order_by('letter').annotate(count=Count('letter'))

            print(count_queryset.query)

            self.count_per_letter = dict(count_queryset.values_list('letter', 'count'))

        return queryset

    def get_paginated_response(self, data):
        data = OrderedDict([
            ('meta', OrderedDict([
                ('total_count', self.total_count),
                ('count_per_letter', self.count_per_letter),
            ])),
            ('items', data),
        ])
        return Response(data)
