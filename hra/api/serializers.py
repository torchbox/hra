from rest_framework.fields import Field
from wagtail.core.rich_text import expand_db_html


class RenderedRichTextField(Field):
    def to_representation(self, value):
        return expand_db_html(value)
