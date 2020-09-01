from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.decorators.cache import cache_control
from django.views.generic import TemplateView

from wagtail.utils.urlpatterns import decorate_urlpatterns
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from hra.api import urls as api_urls
from hra.esi import views as esi_views
from hra.search import views as search_views


urlpatterns = [
    url(r'^django-admin/', admin.site.urls),
    url(r'^admin/', include(wagtailadmin_urls)),

    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^search/$', search_views.search, name='search'),
    url(r'^esi/(.*)/$', esi_views.esi, name='esi'),
    url(r'^', include(api_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        # Add views for testing 404 and 500 templates
        url(r'^test404/$', TemplateView.as_view(template_name='404.html')),
        url(r'^test500/$', TemplateView.as_view(template_name='500.html')),
    ]

urlpatterns += [
    url(r'', include(wagtail_urls)),
]


# Cache-control
cache_length = getattr(settings, 'CACHE_CONTROL_MAX_AGE', None)

if cache_length:
    urlpatterns = decorate_urlpatterns(
        urlpatterns,
        cache_control(max_age=cache_length)
    )
