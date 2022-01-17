from datetime import datetime

from django import template

register = template.Library()


@register.simple_tag(name='time_until_now')
def time_until_now(dt):
    now = datetime(2021, 11, 2, 16, 12, 17)
    return (dt - now).days
