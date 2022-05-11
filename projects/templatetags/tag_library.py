from django import template

register = template.Library()

@register.filter()
def to_int(value):
    return int(value)

@register.filter
def sub( value, arg ):
    '''
    Divides the value; argument is the divisor.
    Returns empty string on any error.
    '''
    try:
        value = int( value )
        arg = int( arg )
        if arg: return  arg-value
    except: pass
    return ''