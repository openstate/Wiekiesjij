from django import template
 
register = template.Library()

# Used for "converting the widgets class name to the one for css"
field_class_converter = {
    'integerfield': 'small',
}

class_converter = {
    'colorpicker': 'textinput',
    'autocompleter': 'textinput',
}

@register.filter
def get_class(field):
    """
        returns the class for the given field
    """
    result = []
    
    field_class = field.field.__class__.__name__.lower()
    result.append(field_class_converter.get(field_class, ''))
        
    class_name = field.field.widget.__class__.__name__.lower()
    result.append(class_converter.get(class_name, class_name))
    return ' '.join(filter(lambda x: x, result))
    
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
    
    
class IfMultiFieldNode(template.Node):
    """
        If Node to check if the field has multiple inputs in it's output
        Used to change how the label for the field is shown
    """
    
    MULTIFIELD_CLASSES = (
        'AddressWidget',
        'NameWidget',
        'RadioSelect',
		'CheckboxSelectMultiple',
		'ClearableFileInput',
    )
    
    def __init__(self, field, nodelist_true, nodelist_false):
        self.field = template.Variable(field)
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
        
    def render(self, context):
        field = self.field.resolve(context)
        
        if field.field.widget.__class__.__name__ in self.MULTIFIELD_CLASSES:
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)
        
    @classmethod
    def tag(cls, parser, token):
        tokens = token.split_contents()
        
        if len(tokens) < 2:
            raise template.TemplateSyntaxError('{0} tag requires one field as arguments'.format(tokens[0]))
    
        
        nodelist_true = parser.parse(('else', 'endifmultifield'))    
        token = parser.next_token()
        if token.contents == 'else':
            nodelist_false = parser.parse(('endifmultifield'))
            parser.delete_first_token()
        else:
            nodelist_false = template.NodeList()
        
        return cls(tokens[1], nodelist_true, nodelist_false)
            
register.tag('ifmultifield', IfMultiFieldNode.tag)