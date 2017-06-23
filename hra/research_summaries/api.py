import logging
from urllib import parse

import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError

from hra.research_summaries.importers import ResearchSummaryPageImporter
from hra.utils.datetime import iter_between_dates

logger = logging.getLogger(__name__)


class APIError(Exception):
    pass


def fetch_chunks_for_dates(parent_page, start_date, end_date):
    """
    Fetches research summaries for a given period
    in chunks no longer than settings.HARP_API_MAX_PERIOD_DAYS.

    The API doesn't allow to fetch data for a period longer than 365 days,
    but we can do that using multiple requests.
    """

    api_max_period_days = settings.HARP_API_MAX_PERIOD_DAYS
    for current_start_date, current_end_date in iter_between_dates(start_date, end_date, api_max_period_days):
        fetch_for_dates(parent_page, current_start_date, current_end_date)


def fetch_for_dates(parent_page, start_date, end_date):
    """
    Fetches research summaries for a given period.

    Doesn't allow to fetch for a period longer than settings.HARP_API_MAX_PERIOD_DAYS,
    because the API doesn't allow to fetch data for a period longer than 365 days.
    """

    api_url = getattr(settings, 'HARP_API_URL', None)
    api_username = getattr(settings, 'HARP_API_USERNAME', None)
    api_password = getattr(settings, 'HARP_API_PASSWORD', None)
    api_max_period_days = getattr(settings, 'HARP_API_MAX_PERIOD_DAYS', None)
    api_date_format = '%Y-%m-%d'

    if not all([api_url, api_username, api_password, api_max_period_days]):
        raise ImproperlyConfigured(
            "HARP API settings are incorrect. "
            "You must specify the following settings: "
            "HARP_API_URL, HARP_API_USERNAME, HARP_API_PASSWORD, "
            "HARP_API_MAX_PERIOD_DAYS"
        )

    if abs((start_date - end_date).days) > api_max_period_days:
        raise APIError(
            "You can not request period longer than {} days".format(
                api_max_period_days
            )
        )

    query_params = parse.urlencode({
        # Explicitly convert date into a string of required format
        'datePublishedFrom': start_date.strftime(api_date_format),
        'datePublishedTo': end_date.strftime(api_date_format),
    })

    request_url = '{}?{}'.format(api_url, query_params)
    response = requests.get(request_url, auth=(api_username, api_password))

    if response.status_code != 200:
        raise APIError(
            "Failed to fetch research summary data from '{}' (received '{} {}' response)".format(
                request_url,
                response.status_code,
                response.reason,
            )
        )

    data = response.json()

    if not isinstance(data, list):
        raise APIError(
            "API has returned {}. Expected type: {}".format(type(data), list)
        )

    for item in data:
        importer = ResearchSummaryPageImporter(item)

        logger.info(
            "Processing research summary {}={}".format(
                importer.id_mapping.source,
                importer.id_mapping.get_field_data(item),
            )
        )

        try:
            importer.create_or_update_page(parent_page)
        except ValidationError:
            logger.exception(
                "Unable to create or update a page "
                "due to validation errors. {}={}".format(
                    importer.id_mapping.source,
                    importer.id_mapping.get_field_data(item),
                )
            )
        except ValueError:
            logger.info(
                "Unable to create or update a page "
                "due to ValueError exception. {}={}".format(
                    importer.id_mapping.source,
                    importer.id_mapping.get_field_data(item),
                ),
                exc_info=True
            )
