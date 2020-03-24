from django import template

from hra.esi import register_inclusion_tag
from hra.notifications.models import NotificationBarSettings, CookieBannerSettings


register = template.Library()

esi_inclusion_tag = register_inclusion_tag(register)


@esi_inclusion_tag('notifications/notification_bar.html')
def notification_bar(context):
    return {
        'notification_settings': NotificationBarSettings.for_site(context['request'].site),
        'request': context['request'],
    }


@esi_inclusion_tag('notifications/cookie_banner.html')
def cookie_banner(context):
    return {
        'cookiebanner_settings': CookieBannerSettings.for_site(context['request'].site),
        'request': context['request'],
    }


@register.filter(is_safe=True)
def lose_br(value):
    return value.replace('<br/>', '')
