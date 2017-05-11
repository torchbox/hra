from modelcluster.models import ClusterableModel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailcore.blocks import (ListBlock, PageChooserBlock,
                                        StructBlock, TextBlock)
from wagtail.wagtailcore.fields import StreamField

from hra.esi import purge_esi


class OverrideablePageChooserBlock(StructBlock):
    page = PageChooserBlock()
    title = TextBlock(help_text="Leave blank to use the page's own title", required=False)


@register_setting(icon='list-ul')
class NavigationSettings(BaseSetting, ClusterableModel):
    header_links = StreamField(
        [
            ('item', OverrideablePageChooserBlock()),
        ],
        blank=True
    )
    footer_links = StreamField(
        [
            ('column', StructBlock([
                ('column_heading', TextBlock()),
                ('subitems', ListBlock(OverrideablePageChooserBlock(label="Sub-item"))),
            ])),
        ],
        blank=True
    )
    footer_secondary_links = StreamField(
        [
            ('item', OverrideablePageChooserBlock()),
        ],
        blank=True
    )

    panels = [
        StreamFieldPanel('header_links'),
        StreamFieldPanel('footer_links'),
        StreamFieldPanel('footer_secondary_links'),
    ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        purge_esi()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        purge_esi()
