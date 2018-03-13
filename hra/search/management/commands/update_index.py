# TODO: This code matches wagtail versions 1.11 through to 2.0
# Updates beyond that will require checking for compatability
# Also check for https://github.com/wagtail/wagtail/pull/4358 being merged

from wagtail.wagtailsearch.management.commands.update_index import Command as SuperCommand

class Command(SuperCommand):
    def queryset_chunks(self, qs):
        return super().queryset_chunks(qs, 50)

    def handle(self, **options):
        return super().handle(**options)
