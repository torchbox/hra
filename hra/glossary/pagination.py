from collections import OrderedDict

from django.core.cache import cache
from django.db.models import Count
from django.db.models.functions import Substr, Lower
from rest_framework.pagination import BasePagination
from rest_framework.response import Response


class GlossaryTermsPagination(BasePagination):
    query_parameter = 'term_startswith'

    def __init__(self):
        self.count_per_letter = None

    def paginate_queryset(self, queryset, request, view=None):
        """
        We do not need pagination, but need some additional information
        after filtering like total count.
        """

        self.view = view
        self.total_count = queryset.count()

        # Get count by first letter
        if view:
            model = view.model
            count_per_letter_cache_key = 'glossary_pagination_count_per_letter-{}'.format(model._meta.label)

            count_per_letter = cache.get(count_per_letter_cache_key)
            if not count_per_letter:
                count_queryset = model.objects.annotate(letter=Lower(Substr('name', 1, 1))).values('letter')
                count_queryset = count_queryset.order_by('letter').annotate(count=Count('letter'))

                count_per_letter = dict(count_queryset.values_list('letter', 'count'))

                # Set cache for 5 minutes
                cache.set(count_per_letter_cache_key, count_per_letter, 60 * 5)

            self.count_per_letter = count_per_letter

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
