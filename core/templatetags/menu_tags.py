from django import template

register = template.Library()


@register.filter
def intersection(qs1, qs2):
    try:
        return qs1 & qs2
    except TypeError:
        return []