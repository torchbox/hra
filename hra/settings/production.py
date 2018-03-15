import os
import raven  # noqa

import django_cache_url
import dj_database_url
from elasticsearch import RequestsHttpConnection
from requests_aws4auth import AWS4Auth

from .base import *  # noqa

# Do not set SECRET_KEY, Postgres or LDAP password or any other sensitive data here.
# Instead, use environment variables or create a local.py file on the server.

# Disable debug mode
DEBUG = False

SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# enable HSTS only once the site is working properly on https with the actual live domain name
# SECURE_HSTS_SECONDS = 31536000  # 1 year


# Cache everything for 10 minutes
# This only applies to pages that do not have a more specific cache-control
# setting. See urls.py
CACHE_CONTROL_MAX_AGE = 600


# Google tag manager

GOOGLE_TAG_MANAGER_ID = 'GTM-K8CGDX6'


# Newsletter

NEWSLETTER_URL = '//nhs.us8.list-manage.com/subscribe?u=04af4dde330becaf38e8eb355&id=1a71ed9a1e'


# Configuration from environment variables
# Alternatively, you can set these in a local.py file on the server

env = os.environ.copy()

# CFG_ prefixed environment variables are made available for use by the application
for key, value in os.environ.items():
    if key.startswith('CFG_'):
        env[key[4:]] = value


# Basic configuration

APP_NAME = env.get('APP_NAME', 'hra')

if 'RECAPTCHA_PUBLIC_KEY' in env:
    RECAPTCHA_PUBLIC_KEY = env['RECAPTCHA_PUBLIC_KEY']
    RECAPTCHA_PRIVATE_KEY = env['RECAPTCHA_PRIVATE_KEY']

if 'SECRET_KEY' in env:
    SECRET_KEY = env['SECRET_KEY']

if 'ALLOWED_HOSTS' in env:
    ALLOWED_HOSTS = env['ALLOWED_HOSTS'].split(',')

if 'PRIMARY_HOST' in env:
    BASE_URL = 'http://%s/' % env['PRIMARY_HOST']

if 'SERVER_EMAIL' in env:
    SERVER_EMAIL = env['SERVER_EMAIL']
    DEFAULT_FROM_EMAIL = env['SERVER_EMAIL']
    EMAIL_USE_TLS = True
    EMAIL_HOST = env['EMAIL_HOST']
    EMAIL_PORT = 587
    EMAIL_HOST_USER = env['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = env['EMAIL_HOST_PASSWORD']

if 'EMAIL_SUBJECT_PREFIX' in env:
    EMAIL_SUBJECT_PREFIX = env['EMAIL_SUBJECT_PREFIX']

if 'CACHE_PURGE_URL' in env:
    INSTALLED_APPS += ('wagtail.contrib.wagtailfrontendcache', )  # noqa
    WAGTAILFRONTENDCACHE = {
        'default': {
            'BACKEND': 'wagtail.contrib.wagtailfrontendcache.backends.HTTPBackend',
            'LOCATION': env['CACHE_PURGE_URL'],
        },
    }

if 'STATIC_URL' in env:
    STATIC_URL = env['STATIC_URL']

if 'STATIC_DIR' in env:
    STATIC_ROOT = env['STATIC_DIR']

if 'MEDIA_URL' in env:
    MEDIA_URL = env['MEDIA_URL']

if 'MEDIA_DIR' in env:
    MEDIA_ROOT = env['MEDIA_DIR']


if 'MEDIA_BUCKET' in env:
    AWS_LOCATION = 'media/'
    AWS_STORAGE_BUCKET_NAME = env['MEDIA_BUCKET']
    AWS_S3_CUSTOM_DOMAIN = env['AWS_S3_CUSTOM_DOMAIN']
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_URL_PROTOCOL = 'https:'
    AWS_S3_SECURE_URLS = True
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# Database

if 'DATABASE_URL' in os.environ:
    DATABASES = {'default': dj_database_url.config()}
elif 'DATABASE_SCHEMA' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env['DATABASE_SCHEMA'],
            'USER': env['DATABASE_USERNAME'],
            'PASSWORD': env['DATABASE_PASSWORD'],
            'HOST': env['DATABASE_HOST'],
            'PORT': env['DATABASE_PORT'],
        },
    }

# Redis

if 'CACHE_URL' in os.environ:
    CACHES = {'default': django_cache_url.config()}
elif 'CACHE_HOST' in os.environ:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': "redis://%s:%s/%s" % (env['CACHE_HOST'], env['CACHE_PORT'], env['CACHE_DB']),
            'KEY_PREFIX': 'hra',
        }
    }


# Celery
# Ask sysadmin to add `CFG_BROKER_URL` env var, if you need celery.

if 'BROKER_URL' in env:
    BROKER_URL = env['BROKER_URL']


if 'ES_HOST' in env:
    WAGTAILSEARCH_BACKENDS = {
        'default': {
            'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch5',
            'INDEX': env['ES_INDEX'],
            'HOSTS': [{
                'host': env['ES_HOST'],
                'port': 443,
                'use_ssl': True,
                'verify_certs': True,
                'http_auth': AWS4Auth(env['ES_ACCESS_KEY_ID'], env['ES_SECRET_ACCESS_KEY'], env['ES_REGION'], 'es'),
            }],
            'OPTIONS': {
                'connection_class': RequestsHttpConnection,
            },
        },
    }


# Raven (sentry) configuration.
if 'RAVEN_DSN' in env:
    RAVEN_CONFIG = {
        'dsn': env['RAVEN_DSN'],
        'release': open("version.txt").read(),
    }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True,
        }
    }
}

if 'HARP_API_USERNAME' in os.environ:
    HARP_API_USERNAME = os.environ['HARP_API_USERNAME']
    HARP_API_PASSWORD = os.environ['HARP_API_PASSWORD']

if 'GOOGLE_TAG_MANAGER_ID' in os.environ:
    GOOGLE_TAG_MANAGER_ID = os.environ['GOOGLE_TAG_MANAGER_ID']
