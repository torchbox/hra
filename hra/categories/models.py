from django.db import models

from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import FieldPanel


@register_snippet
class Category(models.Model):
    name = models.CharField(max_length=255)

    panels = [
        FieldPanel('name', classname="full"),
    ]

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


@register_snippet
class PageType(models.Model):
    name = models.CharField(max_length=255)

    panels = [
        FieldPanel('name', classname="full"),
    ]

    def __str__(self):
        return self.name
