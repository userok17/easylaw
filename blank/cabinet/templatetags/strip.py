from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='strip')
def strip_value(value):
    return value.strip()