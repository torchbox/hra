import logging

from dateutil.parser import parse as parse_date
from django.core.management import BaseCommand, CommandError
from django.db import models
from django.utils.datetime_safe import date

from hra.research_summaries.api import fetch_chunks_for_dates
from hra.research_summaries.models import ResearchSummariesIndexPage, ResearchSummaryPage

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "The command that imports reports since the last import. If date range is "
        "specified, imports summaries for a given period."
    )

    def add_arguments(self, parser):
        parser.add_argument('--date-from', type=str, dest='start_date', default=None)
        parser.add_argument('--date-to', type=str, dest='end_date', default=None)

    def handle(self, *args, **options):
        start_date = options['start_date']
        end_date = options['end_date']

        if not (start_date and end_date) and (start_date or end_date):
            raise CommandError(
                "You must specify both --date-from and --date-to "
                "to import research summaries for a given period."
            )

        if start_date:
            start_date = parse_date(start_date).date()

        if end_date:
            if end_date == 'today':
                end_date = date.today()
            else:
                end_date = parse_date(end_date).date()

        if not (start_date and end_date):
            # If there is no dates in arguments,
            # use the date of the last import as a start date,
            # and the current date as an end date
            end_date = date.today()
            last_updated_at = ResearchSummaryPage.objects.aggregate(last_updated_at=models.Max('updated_at'))
            last_updated_at = last_updated_at.get('last_updated_at')

            if not last_updated_at:
                raise CommandError(
                    "No research summaries were imported before. "
                    "You have to run import and specify date range manually."
                )

            start_date = last_updated_at.date()

        parent_page = ResearchSummariesIndexPage.objects.first()
        logger.info('Importing research summaries %s - %s', start_date, end_date)

        if not parent_page:
            raise CommandError(
                "There is no ResearchSummariesIndexPage pages. "
                "You have to create one to be able to import research summaries."
            )

        fetch_chunks_for_dates(parent_page, start_date, end_date)
