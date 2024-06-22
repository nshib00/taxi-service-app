from django import template

from datetime import datetime


register = template.Library()


@register.simple_tag
def get_current_time():
    return datetime.now().strftime('%H:%M')
