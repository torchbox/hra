from django import template

from hra.esi import register_inclusion_tag
from hra.notifications.models import NotificationBarSettings

register = template.Library()

esi_inclusion_tag = register_inclusion_tag(register)


# Primary nav
@esi_inclusion_tag('notifications/notification_bar.html')
def notification_bar(context):
    return {
        'notification_settings': NotificationBarSettings.for_site(context['request'].site),
        'request': context['request'],
    }
