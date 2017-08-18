from django.http import HttpResponse

class ELBHealthCheck(object):
    def process_request(self, request):
        if request.path == "/__ping__":
            return HttpResponse("OK", content_type="text/plain")
