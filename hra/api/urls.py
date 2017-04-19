from django.conf.urls import include, url
from django.views.decorators.cache import never_cache
from wagtail.utils.urlpatterns import decorate_urlpatterns

from hra.api.documentation import include_docs_urls
from hra.api.routers import api_router


urlpatterns = [
    url(r'^api/v2/', include(api_router.urls)),
]

urlpatterns = decorate_urlpatterns(urlpatterns, never_cache)

urlpatterns += [
    url(r'^api_docs/', include_docs_urls(title='HRA API docs', patterns=urlpatterns)),
]
