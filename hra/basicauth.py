import logging
import os
from base64 import standard_b64decode

from django.conf import settings
from django.http import HttpResponse

logger = logging.getLogger(__name__)


class BasicAuth(object):

    """
    We can't do firewalls with CloudFront. So basic auth is a must.

    Pre-production instances must set the BASIC_AUTH_USER and BASIC_AUTH_PASS
    environment variables. They can optionally set BASIC_AUTH_REALM (which
    defaults to 'Development')
    """

    def render_401(self):
        response = HttpResponse(
            "<html><title>401 Unauthorized</title><body><h1>401 Unauthorized</h1></body></html>",
            content_type="text/html",
        )
        response['WWW-Authenticate'] = "Basic realm=\"%s\"" % os.environ['BASIC_AUTH_REALM']
        response.status_code = 401
        return response

    def is_authenticated(self, request):
        if 'HTTP_AUTHORIZATION' not in request.META:
            logger.debug('basicauth: no HTTP_AUTHORIZATION - {}'.format(request.path))
            return False

        method, auth = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
        if method.lower() != 'basic':
            logger.debug('basicauth: HTTP_AUTHORIZATION not basic - {}'.format(request.path))
            return False

        username, password = standard_b64decode(auth.strip().encode()).decode().split(':', 1)
        basic_auth_user, basic_auth_pass = os.environ['BASIC_AUTH_USER'], os.environ['BASIC_AUTH_PASS']
        if basic_auth_user != username or basic_auth_pass != password:
            logger.debug('basicauth: password mismatch {}/{} != {}/{}'.format(username,
                                                                              password,
                                                                              basic_auth_user,
                                                                              basic_auth_pass))
            return False

        return True

    def process_request(self, request):
        if os.environ.get('BASIC_AUTH_REALM', '') != '':
            if not self.is_authenticated(request):
                return self.render_401()
