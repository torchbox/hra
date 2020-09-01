from wagtail.core import blocks

from hra.utils.blocks import HighlightBlock


class ListingBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, max_length=128)
    display_meta_info = blocks.BooleanBlock(required=False)
    featured_pages = blocks.ListBlock(blocks.PageChooserBlock())
    pages = blocks.ListBlock(blocks.PageChooserBlock())

    class Meta:
        icon = 'list-ul'
        template = "home/blocks/listing_block.html"


class HomePageBodyBlock(blocks.StreamBlock):
    listing = ListingBlock()
    highlight = HighlightBlock(template='home/blocks/highlight_block.html')
