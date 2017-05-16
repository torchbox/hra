from wagtail.wagtailcore.models import PageViewRestriction


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
