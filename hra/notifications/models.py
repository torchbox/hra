from django.db import models
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField

from hra.esi import purge_esi


@register_setting(icon='warning')
class NotificationBarSettings(BaseSetting):
    NOTIFICATION_TYPES = (
        ('default', 'Notification'),
        ('error', 'Error'),
        ('success', 'Success'),
    )

    type = models.CharField(max_length=32, choices=NOTIFICATION_TYPES, blank=True,
                            help_text='Set empty type to hide the notification')
    title = models.CharField(max_length=128)
    text = RichTextField(max_length=128, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel('type'),
        FieldPanel('title'),
        FieldPanel('text', classname='full'),
    ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        purge_esi()
