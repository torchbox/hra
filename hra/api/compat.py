from django.conf.urls import url
from wagtail.api.v2.endpoints import BaseAPIEndpoint
from wagtail.api.v2.utils import parse_fields_parameter, BadRequestError


class CoreAPICompatibilityMixin(BaseAPIEndpoint):
    """
    Temporary mixin to bring CoreAPI support to te project.

    TODO: Remove once Wagtail provide support for the WagtailAPI.
    """

    def list(self, request):
        return self.listing_view(request)

    def retrieve(self, request, pk):
        return self.detail_view(request, pk)

    @classmethod
    def get_urlpatterns(cls):
        return [
            url(r'^$', cls.as_view({'get': 'list'}), name='listing'),
            url(r'^(?P<pk>\d+)/$', cls.as_view({'get': 'retrieve'}), name='detail'),
        ]

    def get_serializer_class(self):
        request = self.request

        # Get model
        if self.action == 'list':
            model = self.get_queryset().model
        else:
            model = type(self.get_object())

        # Fields
        if 'fields' in request.GET:
            try:
                fields_config = parse_fields_parameter(request.GET['fields'])
            except ValueError as e:
                raise BadRequestError("fields error: %s" % str(e))
        else:
            # Use default fields
            fields_config = []

        # Allow "detail_only" (eg parent) fields on detail view
        if self.action == 'list':
            show_details = False
        else:
            show_details = True

        return self._get_serializer_class(self.request.wagtailapi_router, model, fields_config, show_details=show_details)
