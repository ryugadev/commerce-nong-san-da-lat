from django import template

register = template.Library()

@register.filter
def comma_to_period(value):
    """
    Chuyển đổi dấu phẩy thành dấu chấm trong chuỗi.
    Ví dụ: "1,234,567" → "1.234.567"
    """
    try:
        return value.replace(",", ".")
    except AttributeError:
        return value


@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''
