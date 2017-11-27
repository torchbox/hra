import dj_database_url
import django_cache_url

from .base import *  # noqa


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'CHANGEME!!!'

INTERNAL_IPS = ('127.0.0.1', '10.0.2.2')

BASE_URL = 'http://localhost:8000'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AUTH_PASSWORD_VALIDATORS = []

DATABASES = {'default': dj_database_url.config()}

CACHES = {'default': django_cache_url.config()}

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch5',
        'INDEX': 'hra',
    },
}

try:
    from .local import *  # noqa
except ImportError:
    pass
