from django.conf.urls import include, url

from hra.api.documentation import include_docs_urls
from hra.api.routers import api_router


urlpatterns = [
    url(r'^api/v2/', include(api_router.urls)),
]

urlpatterns += [
    url(r'^api_docs/', include_docs_urls(title='HRA API docs', patterns=urlpatterns)),
]
