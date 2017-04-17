from rest_framework.fields import Field
from wagtail.api.v2.serializers import BaseSerializer
from wagtail.wagtailcore.rich_text import expand_db_html


class RenderedRichTextField(Field):
    def to_representation(self, value):
        return expand_db_html(value)


class GlossaryTermSerializer(BaseSerializer):
    description = RenderedRichTextField()
