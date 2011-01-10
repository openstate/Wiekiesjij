from django import template

register = template.Library()

class IfProfileNode(template.Node):
    """
        If Node to check if the user has the correct profiletype
        
        Example:
        
            {% ifprofile 'council_admin' %}
                Link to something you need to be council_admin for
            {% else %}
                No link
            {% endifprofile %}
    """
    PROFILE_TYPE = ['council_admin', 'party_admin', 'candidate']
    
    def __init__(self, profile_type, nodelist_true, nodelist_false):
        self.profile_type = template.Variable(profile_type)
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
        
    def render(self, context):
        profile_type = self.profile_type.resolve(context)
        user = context['user']
        
        type_index = self.PROFILE_TYPE.index(profile_type)
        if not user.is_authenticated():
            return self.nodelist_false.render(context)
        elif user.is_staff:
            return self.nodelist_true.render(context)
        elif user.profile is not None and self.PROFILE_TYPE.index(user.profile.type) <= type_index:
            return self.nodelist_true.render(context)
            
        return self.nodelist_false.render(context)
        
    @classmethod
    def tag(cls, parser, token):
        tokens = token.split_contents()
        
        if len(tokens) < 2:
            raise template.TemplateSyntaxError('{0} tag requires one profile.type as arguments'.format(tokens[0]))
    
        nodelist_true = parser.parse(('else', 'endifprofile'))    
        token = parser.next_token()
        if token.contents == 'else':
            nodelist_false = parser.parse(('endifprofile'))
            parser.delete_first_token()
        else:
            nodelist_false = template.NodeList()
        
        return cls(tokens[1], nodelist_true, nodelist_false)
            
register.tag('ifprofile', IfProfileNode.tag)