from django import template

from hra.esi import register_inclusion_tag
from hra.navigation.models import NavigationSettings

register = template.Library()

esi_inclusion_tag = register_inclusion_tag(register)


# Primary nav
@esi_inclusion_tag('navigation/headernav.html')
def headernav(context):
    return {
        'headernav': NavigationSettings.for_site(context['request'].site).header_links,
        'request': context['request'],
    }


# Footer nav
@esi_inclusion_tag('navigation/footernav.html')
def footernav(context):
    return {
        'footernav': NavigationSettings.for_site(context['request'].site).footer_links,
        'request': context['request'],
    }

@esi_inclusion_tag('navigation/footersecondarynav.html')
def footersecondarynav(context):
    return {
        'footersecondarynav': NavigationSettings.for_site(context['request'].site).footer_secondary_links,
        'request': context['request'],
    }
