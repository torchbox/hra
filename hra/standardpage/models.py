import logging

from django.conf import settings
from django.core.handlers.base import BaseHandler
from django.core.handlers.wsgi import WSGIRequest
from django.db import models
from django.utils.functional import cached_property
from django.utils.six import StringIO
from django.utils.six.moves.urllib.parse import urlparse

from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, StreamFieldPanel,
    InlinePanel,
    MultiFieldPanel
)

from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel

from hra.utils.blocks import StoryBlock
from hra.utils.models import ListingFields, SocialFields, RelatedPage, CallToActionSnippet


logger = logging.getLogger(__name__)


class StandardPagePageType(models.Model):
    page = ParentalKey(
        'standardpage.StandardPage',
        related_name='page_type_relationships'
    )
    page_type = models.ForeignKey(
        'categories.PageType',
        related_name='+',
        on_delete=models.CASCADE
    )

    panels = [
        SnippetChooserPanel('page_type')
    ]


class StandardPageRelatedPage(RelatedPage):
    source_page = ParentalKey('standardpage.StandardPage', related_name='related_pages')


class StandardPage(Page, SocialFields, ListingFields):
    hero_image = models.ForeignKey('images.CustomImage', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='+')
    introduction = RichTextField(blank=True)
    body = StreamField(StoryBlock())

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('hero_image'),
        FieldPanel('introduction'),
        StreamFieldPanel('body'),
        InlinePanel('related_pages', label="Related pages"),
    ]

    promote_panels = (
        Page.promote_panels +
        SocialFields.promote_panels +
        ListingFields.promote_panels + [
            InlinePanel('page_type_relationships', label='Page types')
        ]
    )

    @cached_property
    def page_types(self):
        page_types = [
            n.page_type for n in self.page_type_relationships.all()
        ]
        return page_types

    def dummy_request(self, original_request=None, **meta):
        logger.info('ORIGINAL REQUEST: {}'.format(original_request.__dict__))

        # build dummy request - copied from superclass

        url = self.full_url
        if url:
            url_info = urlparse(url)
            hostname = url_info.hostname
            path = url_info.path
            port = url_info.port or 80
            scheme = url_info.scheme
        else:
            # Cannot determine a URL to this page - cobble one together based on
            # whatever we find in ALLOWED_HOSTS
            try:
                hostname = settings.ALLOWED_HOSTS[0]
                if hostname == '*':
                    # '*' is a valid value to find in ALLOWED_HOSTS[0], but it's not a valid domain name.
                    # So we pretend it isn't there.
                    raise IndexError
            except IndexError:
                hostname = 'localhost'
            path = '/'
            port = 80
            scheme = 'http'

        dummy_values = {
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': path,
            'SERVER_NAME': hostname,
            'SERVER_PORT': port,
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'HTTP_HOST': hostname,
            'wsgi.version': (1, 0),
            'wsgi.input': StringIO(),
            'wsgi.errors': StringIO(),
            'wsgi.url_scheme': scheme,
            'wsgi.multithread': True,
            'wsgi.multiprocess': True,
            'wsgi.run_once': False,
        }

        # Add important values from the original request object, if it was provided.
        HEADERS_FROM_ORIGINAL_REQUEST = [
            'REMOTE_ADDR', 'HTTP_X_FORWARDED_FOR', 'HTTP_COOKIE', 'HTTP_USER_AGENT',
            'wsgi.version', 'wsgi.multithread', 'wsgi.multiprocess', 'wsgi.run_once',
        ]
        if settings.SECURE_PROXY_SSL_HEADER:
            HEADERS_FROM_ORIGINAL_REQUEST.append(settings.SECURE_PROXY_SSL_HEADER[0])
        if original_request:
            for header in HEADERS_FROM_ORIGINAL_REQUEST:
                if header in original_request.META:
                    dummy_values[header] = original_request.META[header]

        # Add additional custom metadata sent by the caller.
        dummy_values.update(**meta)

        request = WSGIRequest(dummy_values)

        logger.info('PRE-MIDDLEWARE: {}'.format(request.__dict__))

        # Apply middleware to the request
        # Note that Django makes sure only one of the middleware settings are
        # used in a project
        if hasattr(settings, 'MIDDLEWARE'):
            logger.info('MIDDLEWARE processing')
            handler = BaseHandler()
            handler.load_middleware()
            response = handler._middleware_chain(request)
            logger.info('MIDDLEWARE RESPONSE: {}'.format(response.__dict__))
        elif hasattr(settings, 'MIDDLEWARE_CLASSES'):
            logger.info('MIDDLEWARE_CLASSES processing')
            # Pre Django 1.10 style - see http://www.mellowmorning.com/2011/04/18/mock-django-request-for-testing/
            handler = BaseHandler()
            handler.load_middleware()
            # call each middleware in turn and throw away any responses that they might return
            for middleware_method in handler._request_middleware:
                response = middleware_method(request)
                logger.info('MIDDLEWARE RESPONSE (brief): {}'.format(response))

        logger.info('POST-MIDDLEWARE: {}'.format(request.__dict__))

        return request


class StandardIndexSectionPage(RelatedPage):
    source_page = ParentalKey('standardpage.StandardIndex', related_name='section_pages')


class StandardIndex(Page, SocialFields, ListingFields):
    hero_image = models.ForeignKey('images.CustomImage', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='+')
    hero_introduction = models.CharField(blank=True, max_length=120,
                                         help_text='Short text to appear under page title')
    introduction = RichTextField(blank=True)
    call_to_action = models.ForeignKey(CallToActionSnippet, blank=True, null=True, on_delete=models.SET_NULL,
                                       related_name='+')

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('hero_image'),
            FieldPanel('hero_introduction'),
        ], heading="Hero block"),
        FieldPanel('introduction'),
        SnippetChooserPanel('call_to_action'),
        InlinePanel('section_pages', label='Section pages'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
    ]

    promote_panels = (
        Page.promote_panels +
        SocialFields.promote_panels +
        ListingFields.promote_panels
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context['sidebar_pages'] = self.get_children().live().public()

        return context
