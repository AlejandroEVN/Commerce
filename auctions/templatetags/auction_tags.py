from django import template

register = template.Library()

@register.filter
def sub(value, arg):
    return value - arg

@register.filter
def usd(value):
    return f"${value}"

@register.filter
def count(value):
    return len(value)

@register.filter
def capitalize(value):
    return value.capitalize()