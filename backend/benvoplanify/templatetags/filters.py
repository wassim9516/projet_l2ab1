from django import template

register = template.Library()

@register.filter
def dict_get(liste, key):
    for k, v in liste:
        if k == key:
            return v
    return ''
