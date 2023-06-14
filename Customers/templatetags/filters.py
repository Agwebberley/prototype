from django import template

register = template.Library()

@register.filter
def get_field_value(item, field_name):
    return getattr(item, field_name)

@register.filter
def replace(value, arg):
    # arg should be in the format of 'old,new'
    old, new = arg.split(',')
    return value.replace(old, new)