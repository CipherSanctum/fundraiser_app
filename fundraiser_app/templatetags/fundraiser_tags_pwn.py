from django import template
from django.utils.safestring import mark_safe
import markdown


register = template.Library()  # necessary to be a valid tag library


@register.filter  # can put (name='my_tag') next to filter for a diff name in template
def markdown_format_fundraiser(text):
    return mark_safe(markdown.markdown(text))


@register.filter
def unslugify_and_capitalize(category_slug):
    return category_slug.replace('-', ' ').title()
