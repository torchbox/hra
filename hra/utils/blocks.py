from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock

from .models import CallToActionSnippet


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(required=False)

    class Meta:
        icon = "image"
        template = "blocks/image_block.html"


class QuoteBlock(blocks.StructBlock):
    quote = blocks.CharBlock(classname="title")
    quotee = blocks.CharBlock(required=False)
    image = ImageChooserBlock()

    class Meta:
        icon = "openquote"
        template = "blocks/quote_block.html"


class CallToActionWithTextBlock(blocks.StructBlock):
    call_to_action = SnippetChooserBlock(CallToActionSnippet)
    side_text = blocks.RichTextBlock()

    class Meta:
        icon = "redirect"
        template = "blocks/call_to_action_with_text_block.html"


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

    class Meta:
        template = "blocks/stream_block.html"
