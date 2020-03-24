from django import template


register = template.Library()


@register.filter
def index(iterable, i: int):
    return iterable[i]
