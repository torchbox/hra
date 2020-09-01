from django.db import models
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.core.fields import RichTextField

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
    title = models.CharField(max_length=100)
    text = RichTextField(max_length=150, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel('type'),
        FieldPanel('title'),
        FieldPanel('text', classname='full'),
    ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        purge_esi()


@register_setting(icon='cog')
class CookieBannerSettings(BaseSetting):

    is_active = models.BooleanField("Active", default=False)
    title = models.CharField(blank=True, max_length=100)
    text = RichTextField(blank=True)
    policy_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        on_delete=models.SET_NULL,
    )

    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel('is_active'),
        FieldPanel('title'),
        FieldPanel('text', classname='full'),
        PageChooserPanel('policy_page'),
    ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        purge_esi()
