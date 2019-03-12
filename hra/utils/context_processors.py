from django.conf import settings


def global_vars(request):
    return {
        'APP_VERSION': getattr(settings, 'APP_VERSION', None),
        'GOOGLE_TAG_MANAGER_ID': getattr(settings, 'GOOGLE_TAG_MANAGER_ID', None),
        'TITLE_SUFFIX': getattr(settings, 'TITLE_SUFFIX', None),
    }
