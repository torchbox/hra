from django import template

from hra.esi import register_inclusion_tag
from hra.navigation.models import NavigationSettings

register = template.Library()

esi_inclusion_tag = register_inclusion_tag(register)


# Primary nav
@esi_inclusion_tag('navigation/headernav.html')
def headernav(context):
    context = {
        'headernav': NavigationSettings.for_site(context['request'].site).header_links,
        'request': context['request'],
        'current_page': context.get('page'),
        'current_page_ancestors_pks': []
    }

    if context['current_page']:
        context['current_page_ancestors_pks'] = context['current_page'] \
            .get_ancestors(inclusive=True).values_list('pk', flat=True)

    return context


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
