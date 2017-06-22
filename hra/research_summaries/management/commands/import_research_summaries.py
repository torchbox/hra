from urllib import parse

import logging
from django.core.management import BaseCommand, CommandError
from django.utils.datetime_safe import date

from hra.research_summaries.api import fetch_for_dates
from hra.research_summaries.models import ResearchSummariesIndexPage


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        parent_page = ResearchSummariesIndexPage.objects.first()

        if not parent_page:
            raise CommandError(
                "There is no ResearchSummariesIndexPage pages. "
                "You have to create one to be able to import research summaries."
            )

        # TODO: Use arguments
        start_date = date(2015, 12, 1)
        end_date = date(2015, 12, 31)

        fetch_for_dates(parent_page, start_date, end_date)
