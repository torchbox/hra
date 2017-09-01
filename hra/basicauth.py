import logging

from django.conf import settings
from django.http import HttpResponse

# from django.contrib.sites.models import Site
from ten_self_service.core.models import SiteScheme

logger = logging.getLogger(__name__)


class BasicAuth(object):

    """
    We can't do firewalls with CloudFront. So basic auth is a must.

    Pre-production instances must set the BASIC_AUTH_USER and BASIC_AUTH_PASS
    environment variables. They can optionally set BASIC_AUTH_REALM (which
    defaults to 'Development')
    """

    def render_401(self, site_scheme):
        response = HttpResponse(
            "<html><title>401 Unauthorized</title><body><h1>401 Unauthorized</h1></body></html>",
            content_type="text/html",
        )
        realm = site_scheme.basic_auth_realm
        response['WWW-Authenticate'] = "Basic realm=\"%s\"" % realm
        response.status_code = 401
        return response

    def is_authenticated(self, request, site_scheme):
        if 'HTTP_AUTHORIZATION' not in request.META:
            logger.debug('basicauth: no HTTP_AUTHORIZATION - {}'.format(request.path))
            return False

        method, auth = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
        if method.lower() != 'basic':
            logger.debug('basicauth: HTTP_AUTHORIZATION not basic - {}'.format(request.path))
            return False

        username, password = auth.strip().decode('base64').split(':', 1)
        if site_scheme.basic_auth_user != username or site_scheme.basic_auth_pass != password:
            logger.debug('basicauth: password mismatch {}/{} != {}/{}'.format(username,
                                                                              password,
                                                                              site_scheme.basic_auth_user,
                                                                              site_scheme.basic_auth_pass))
            return False

        return True

    def process_request(self, request):
        site_scheme = SiteScheme.objects.only(
            'basic_auth_enabled',
            'basic_auth_user',
            'basic_auth_pass'
        ).get(site=settings.SITE_ID)  # get without caching
        required_fields = (
            site_scheme.basic_auth_enabled,
            site_scheme.basic_auth_user,
            site_scheme.basic_auth_pass
        )
        if all(required_fields):
            if request.path.startswith("/static/"):
                return
            if request.path in getattr(settings, "BASIC_AUTH_DISABLED", []):
                return
            if not self.is_authenticated(request, site_scheme):
                return self.render_401(site_scheme)
