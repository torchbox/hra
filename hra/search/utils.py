from wagtail.wagtailcore.models import PageViewRestriction, Page

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


def get_search_queryset(request, page_types=None):
    """
    Returns a QuerySet for further search.
    We need to keep in mind, that we must not perform any
    ORM operations that Wagtail's QuerySet search API doesn't support.
    """
    # Allow to search only among live pages
    queryset = Page.objects.live().descendant_of(request.site.root_page)

    # Exclude pages that the user doesn't have permission to see
    queryset = exclude_invisible_pages(request, queryset)

    # We need to search among pages with specified page type.
    #
    # Unfortunately, it's not possible (at the moment)
    # to filter search results in ElasticSearch using queryset API,
    # so we need to get PKs of linked pages from category page
    # and pass them into queryset for further search.
    if page_types:
        standard_pages = StandardPage.objects.filter(page_type_relationships__page_type__in=page_types)

        queryset = queryset.filter(pk__in=standard_pages.values_list('pk', flat=True))

    return queryset
