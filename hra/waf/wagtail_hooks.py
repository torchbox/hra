import re

from django.utils.html import format_html, format_html_join
from django.conf import settings

from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.rich_text import DbWhitelister


@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        'waf/purify.1.0.2.min.js',
        'waf/rangy-core.1.3.0.js',
        'waf/rangy-selectionsaverestore.1.3.0.js',
        'waf/hallo-dompurify.js',
    ]
    js_includes = format_html_join('\n', '<script src="{0}{1}"></script>',
                                   ((settings.STATIC_URL, filename) for filename in js_files)
                                   )

    # fake a clean to ensure construct_whitelister_element_rules hooks are hooked
    DbWhitelister.clean('')
    allowed_tags = ['#text'] + [key for key in DbWhitelister.element_rules if re.match('[a-z]+', key)]

    # DOMpurify will be more forgiving than DbWhitelister as it's not filtering attributes
    # but it's not practical to extrapolate from DbWhitelister which ones to retain
    return js_includes + format_html(
        """
            <script>
                (function() {{
                    var config = {{
                        ALLOWED_TAGS: [{allowed_tags}],
                        KEEP_CONTENT: true
                    }};
                    registerHalloPlugin('dompurify', config);
                }})();
            </script>
        """,
        allowed_tags=format_html_join(', ', "'{}'", ((tag, ) for tag in allowed_tags)),
    )
