from django import template
import os, json
register = template.Library()

@register.inclusion_tag('_delayed_next.html')
def delayed_next(wait=2000, label='NEXT'):
    return {
        'wait_time': wait,
        'label': label
    }