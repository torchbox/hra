from django.conf.urls import include, url
from django.views.decorators.cache import never_cache
from wagtail.utils.urlpatterns import decorate_urlpatterns

from hra.api.routers import api_router


urlpatterns = [
    url(r'^api/v2/', include(api_router.urls)),
]

urlpatterns = decorate_urlpatterns(urlpatterns, never_cache)
