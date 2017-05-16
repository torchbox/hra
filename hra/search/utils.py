from django.shortcuts import get_object_or_404
from wagtail.wagtailcore.models import PageViewRestriction, Page

from hra.categories.models import PageType
from hra.standardpage.models import StandardPage


def exclude_invisible_pages(request, pages):
    # Get list of pages that are restricted to this user
    restricted_pages = [
        restriction.page
        for restriction in PageViewRestriction.objects.all().select_related('page')
        if not restriction.accept_request(request)
    ]

    # Exclude the restricted pages and their descendants from the queryset
    for restricted_page in restricted_pages:
        pages = pages.not_descendant_of(restricted_page, inclusive=True)

    return pages


def get_search_queryset(request):
    """
    Returns a QuerySet for further search.
    We need to keep in mind, that we must not perform any
    ORM operations that Wagtail's QuerySet search API doesn't support.
    """
    # Allow to search only among live pages
    queryset = Page.objects.live()

    # Exclude pages that the user doesn't have permission to see
    queryset = exclude_invisible_pages(request, queryset)

    # Allow to filter search results using a page type, if specified
    page_type_pk = request.GET.get('type', None)
    page_type = get_object_or_404(PageType.objects.all(), pk=page_type_pk) if page_type_pk else None

    # We need to search among pages with specified page type.
    #
    # Unfortunately, it's not possible (at the moment)
    # to filter search results in ElasticSearch using queryset API,
    # so we need to get PKs of linked pages from category page
    # and pass them into queryset for further search.
    if page_type:
        standard_pages = StandardPage.objects.filter(page_type_relationships__page_type=page_type)

        queryset = queryset.filter(pk__in=standard_pages.values_list('pk', flat=True))

    return queryset
