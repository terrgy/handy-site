from django import template


def lol_filter(value, arg=None):
    return 'lol'


register = template.Library()
register.filter('lol', lol_filter)
