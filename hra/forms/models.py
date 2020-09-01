from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import (
    FieldPanel, FieldRowPanel,
    MultiFieldPanel, InlinePanel
)
from wagtail.contrib.forms.models import AbstractFormField
from wagtail.search import index

from wagtailcaptcha.models import WagtailCaptchaEmailForm

from hra.utils.models import (
    ListingFields,
    SocialFields,
)


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields', on_delete=models.CASCADE)


class FormPage(WagtailCaptchaEmailForm, SocialFields, ListingFields):
    introduction = RichTextField(blank=True)
    body = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True, help_text="Text displayed to the user on successful submission of the form")
    action_text = models.CharField(max_length=32, blank=True, help_text="Form action text. Defaults to \"Submit\"")

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        FieldPanel('body'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('action_text'),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    promote_panels = (
        Page.promote_panels +
        SocialFields.promote_panels +
        ListingFields.promote_panels
    )
