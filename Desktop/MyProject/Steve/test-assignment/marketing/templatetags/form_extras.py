from django import template
from django.utils.html import conditional_escape

register = template.Library()


@register.filter(is_safe=True)
def add_class(field, css_class):
    """Add a CSS class to a form field widget."""
    if hasattr(field, 'as_widget'):
        widget = field.field.widget
        classes = widget.attrs.get('class', '')
        if css_class not in classes:
            widget.attrs['class'] = f'{classes} {css_class}'.strip() if classes else css_class
    return field


@register.filter(is_safe=True)
def add_attr(field, attribute):
    """Add an attribute to a form field widget.

    Usage: {{ field|add_attr:"placeholder:Enter text" }}
    """
    if hasattr(field, 'as_widget'):
        widget = field.field.widget
        if ':' in attribute:
            key, value = attribute.split(':', 1)
            widget.attrs[key] = value
    return field


@register.filter
def to_json(value):
    """Convert a Python object to JSON for use in JavaScript."""
    import json
    from django.utils.safestring import mark_safe
    return mark_safe(json.dumps(value))
