from django.utils.html import format_html
from django.core import validators

from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.snippets.blocks import SnippetChooserBlock

from .models import CallToActionSnippet


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(required=False)
    longdesc = blocks.PageChooserBlock(
        label='Long description',
        required=False,
        target_model='standardpage.StandardPage',
        help_text='If this image conveys infomation not given in the page text, provide a page with an full description for non-sighted users.'
    )

    class Meta:
        icon = "image"
        template = "blocks/image_block.html"


class QuoteBlock(blocks.StructBlock):
    quote = blocks.RichTextBlock()
    quotee = blocks.CharBlock(required=False)
    image = ImageChooserBlock(required=False)

    class Meta:
        icon = "openquote"
        template = "blocks/quote_block.html"


class CallToActionWithTextBlock(blocks.StructBlock):
    call_to_action = SnippetChooserBlock(CallToActionSnippet)
    side_text = blocks.RichTextBlock()

    class Meta:
        icon = "redirect"
        template = "blocks/call_to_action_with_text_block.html"


class HighlightBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    text = blocks.RichTextBlock()
    image = ImageChooserBlock(required=False)

    class Meta:
        icon = "pick"
        template = "blocks/highlight_block.html"


class LMSLoginBlock(blocks.StaticBlock):

    class Meta:
        icon = "password"
        label = 'LMS Login'
        template = 'blocks/lms_login_block.html'


class CookieOptionsBlock(blocks.StructBlock):
    measurement_desc = blocks.RichTextBlock(
        label='Measurement cookies description',
        help_text='Use this to describe how measurement cookies are used on the site. This section is shown only if the relevant cookies are actually in use.'
    )
    necessary_desc = blocks.RichTextBlock(
        label='Necessary cookies description',
        help_text='Use this to describe how necessary cookies are used on the site.'
    )

    class Meta:
        icon = "cog"
        label = 'Cookie Options'
        template = 'blocks/cookie_options.html'


class AnchorBlock(blocks.CharBlock):
    """
    In-page anchor
    """
    def render_basic(self, value, context=None):
        if value:
            return format_html('<a id="{0}"></a>', value)
        else:
            return ''

    def clean(self, value):
        clean_value = super().clean(value)
        validators.validate_slug(clean_value)
        return clean_value

    class Meta:
        icon = "link"
        label = "Anchor"


class StoryBlock(blocks.StreamBlock):
    """
    Main streamfield block to be inherited by Pages
    """

    heading = blocks.CharBlock(classname="full title", icon='title')
    paragraph = blocks.RichTextBlock()
    image = ImageBlock()
    quote = QuoteBlock()
    embed = EmbedBlock()
    call_to_action = CallToActionWithTextBlock()
    highlight = HighlightBlock()
    table = TableBlock(template='blocks/table_block.html')
    lms_login = LMSLoginBlock()
    cookie_options = CookieOptionsBlock()
    anchor = AnchorBlock(help_text='Value to append to URL after # character')

    class Meta:
        template = "blocks/stream_block.html"


# Monkeypatch TableBlock to avoid killing search indexing when empty
# Note it will be still rendered on page as 'None'

_tableblock_get_searchable_content = TableBlock.get_searchable_content

def _safe_tableblock_get_searchable_content(self, value):  # noqa:E302
    if value is not None:
        return _tableblock_get_searchable_content(self, value)
    else:
        return []

TableBlock.get_searchable_content = _safe_tableblock_get_searchable_content  # noqa:E305
