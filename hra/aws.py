from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class ELBHealthCheck(MiddlewareMixin):
    def process_request(self, request):
        if request.path == "/__ping__":
            return HttpResponse("OK", content_type="text/plain")
