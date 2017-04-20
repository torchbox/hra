from django.conf.urls import include, url
from rest_framework.renderers import DocumentationRenderer, CoreJSONRenderer, SchemaJSRenderer

from rest_framework.schemas import SchemaGenerator, SchemaView


def include_docs_urls(title=None, description=None, patterns=None):
    generator = SchemaGenerator(title=title, description=description, patterns=patterns)

    docs_view = SchemaView.as_view(
        renderer_classes=[DocumentationRenderer, CoreJSONRenderer],
        schema_generator=generator,
        public=True,
    )
    schema_js_view = SchemaView.as_view(
        renderer_classes=[SchemaJSRenderer],
        schema_generator=generator,
        public=True,
    )

    urls = [
        url(r'^$', docs_view, name='docs-index'),
        url(r'^schema.js$', schema_js_view, name='schema-js')
    ]
    return include(urls, namespace='api-docs')
