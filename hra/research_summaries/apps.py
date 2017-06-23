from __future__ import absolute_import, division, unicode_literals

from django.apps import AppConfig
from django.core.checks import Error, register


class ResearchSummariesConfig(AppConfig):
    name = 'hra.research_summaries'

    def ready(self):
        @register('research_summaries', deploy=True)
        def check_settings(app_configs, **kwargs):
            from django.conf import settings

            api_url = getattr(settings, 'HARP_API_URL', None)
            api_username = getattr(settings, 'HARP_API_USERNAME', None)
            api_password = getattr(settings, 'HARP_API_PASSWORD', None)
            api_max_period_days = getattr(settings, 'HARP_API_MAX_PERIOD_DAYS', None)

            if not all([api_url, api_username, api_password, api_max_period_days]):
                return [
                    Error(
                        "HARP API settings are incorrect. "
                        "You must specify the following settings: "
                        "HARP_API_URL, HARP_API_USERNAME, HARP_API_PASSWORD, "
                        "HARP_API_MAX_PERIOD_DAYS",
                        id='hra.research_summaries.E001'
                    )
                ]

            return []
