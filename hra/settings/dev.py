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

# Read URLs set in docker-compose.yml
DATABASES = {'default': dj_database_url.config()}
CACHES = {'default': django_cache_url.config()}

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch5',
        'INDEX': 'hra',
        'HOSTS': [{
            'host': 'search',
        }],
    },
}

# For Database performance debugging...
MIDDLEWARE_CLASSES = [
    'hra.rec.middleware.QueryCountDebugMiddleware', ] + MIDDLEWARE_CLASSES
LOGGING['loggers']['hra.rec.middleware'] = {
    'level': 'DEBUG', 'handlers': ['console']}
# LOGGING['loggers']['django.db.backends'] = {'level': 'DEBUG', 'handlers': ['console']}
LOGGING['handlers']['console']['level'] = 'DEBUG'

AWS_ACCESS_KEY_ID = 'fake_key'
AWS_SECRET_ACCESS_KEY = 'fake_secret_key'
AWS_STORAGE_BUCKET_NAME = 'hra'
AWS_AUTO_CREATE_BUCKET = True
AWS_S3_ENDPOINT_URL = 'http://localstack:4572'
AWS_S3_CUSTOM_DOMAIN = 'localhost:4572/hra'
AWS_S3_USE_SSL = False
AWS_S3_SECURE_URLS = False
AWS_DEFAULT_ACL = 'public-read'
AWS_LOCATION = 'media/'
MEDIA_URL = 'http://localhost:4572/hra/media/'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

try:
    from .local import *  # noqa
except ImportError:
    pass
