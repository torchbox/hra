from wagtail.api.v2.router import WagtailAPIRouter

from hra.glossary.endpoints import GlossaryTermsAPIEndpoint

api_router = WagtailAPIRouter('wagtailapi')

api_router.register_endpoint('glossary_terms', GlossaryTermsAPIEndpoint)
