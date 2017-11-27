from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from wagtail.wagtailsearch.models import Query

from hra.categories.models import PageType
from hra.research_summaries.models import ResearchSummaryPage
from hra.search.utils import get_search_queryset


def search(request):
    search_query = request.GET.get('query', None)
    page = request.GET.get('page', 1)

    # Allow to filter search results using a page types, if specified
    page_types = PageType.objects.all()
    selected_page_type_pks = request.GET.getlist('type', None)
    # Use really existing pks
    try:
        selected_page_type_pks = \
            set(int(pk) for pk in selected_page_type_pks) & \
            set(obj.pk for obj in page_types)
    except ValueError:
        selected_page_type_pks = []

    search_results = get_search_queryset(request, selected_page_type_pks)

    # Do not display ResearchSummaryPage pages in the main search
    search_results = search_results.not_type(ResearchSummaryPage)

    # Search
    if search_query:
        search_results = search_results.search(search_query, operator='and')

        query = Query.get(search_query)

        # Record hit
        query.add_hit()

    # Pagination
    paginator = Paginator(search_results, settings.DEFAULT_PER_PAGE)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return render(request, 'search/search.html', {
        'search_query': search_query,
        'search_results': search_results,
        'page_types': page_types,
        'selected_page_type_pks': selected_page_type_pks,
    })
