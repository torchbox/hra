from wagtail.api.v2.serializers import BaseSerializer

from hra.api.serializers import RenderedRichTextField


class GlossaryTermSerializer(BaseSerializer):
    description = RenderedRichTextField()
