from django import template
from django.conf import settings

from wagtail.wagtailcore.utils import camelcase_to_underscore

from hra.events.models import EventPage
from hra.forms.models import FormPage
from hra.news.models import NewsPage
from hra.people.models import PersonPage
from hra.rec.models import CommitteePage
from hra.standardpage.models import StandardPage
from hra.utils.models import SocialMediaSettings


register = template.Library()


# Social text
@register.filter(name='social_text')
def social_text(page, site):
    try:
        return page.social_text
    except AttributeError:
        return SocialMediaSettings.for_site(site).default_sharing_text


# Get widget type of a field
@register.filter(name='widget_type')
def widget_type(bound_field):
    return camelcase_to_underscore(bound_field.field.widget.__class__.__name__)


# Get type of field
@register.filter(name='field_type')
def field_type(bound_field):
    return camelcase_to_underscore(bound_field.field.__class__.__name__)


@register.assignment_tag()
def to_list(*args):
    return args


@register.inclusion_tag('utils/newsletter_signup.html')
def newsletter_signup_form():
    return {
        'newsletter_url': getattr(settings, 'NEWSLETTER_URL', None),
    }


# TODO: Use this on all listings (not only on page) for consistency
@register.assignment_tag(name='page_verbose_names')
def page_verbose_names(page):
    """
    Accepts a page object or page class and
    returns a list (which can be empty) of verbose names for pages
    """

    if isinstance(page, StandardPage) and page.page_types:
        return page.page_types

    mapping = {
        PersonPage: ["Blog post"],
        NewsPage: ["News"],
        EventPage: ["Event"],
        FormPage: ["Form"],
        CommitteePage: ["Committee"],
    }

    key = page
    if isinstance(page, tuple(mapping.keys())):
        key = type(page)

    return mapping.get(key, [])
