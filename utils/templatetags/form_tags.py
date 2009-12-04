from django import template
 
register = template.Library()

# Used for "converting the widgets class name to the one for css"
class_converter = {
    'colorpicker': 'textinput',
}

@register.filter
def get_class(field):
    """
        returns the class for the given field
    """
    class_name = field.field.widget.__class__.__name__.lower()
    return class_converter.get(class_name, class_name)
    
@register.filter
def get_required_class(field):
    """
        returns 'required' if the field is required, 'optional' otherwise
    """
    if field.field.required:
        return 'required'
    return 'optional'

@register.filter
def with_class(field):
    """
        Adds the widget's name as a css class
    """
    class_name = get_class(field)
    class_name += " %s" % get_required_class(field)
    if "class" in field.field.widget.attrs:
        field.field.widget.attrs['class'] += " %s" % class_name
    else:
        field.field.widget.attrs['class'] = class_name
    return field