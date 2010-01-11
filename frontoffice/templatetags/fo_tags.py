from django import template

register = template.Library()



class IsProfileNode(template.Node):
    """
        Checks if current user is of a specific profile type (exactly).

        Example:

            {% isprofile 'visitor' %}
                Link to something for visitors only.
            {% else %}
                No link
            {% endisprofile %}
    """
    def __init__(self, profile_type, nodelist_true, nodelist_false):
        self.profile_type = template.Variable(profile_type)
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false

    def render(self, context):
        profile_type = self.profile_type.resolve(context)
        user = context['user']

        if not user.is_authenticated():
            return self.nodelist_false.render(context)
        elif user.profile is not None and user.profile.type == profile_type:
            return self.nodelist_true.render(context)

        return self.nodelist_false.render(context)

    @classmethod
    def tag(cls, parser, token):
        tokens = token.split_contents()

        if len(tokens) < 2:
            raise template.TemplateSyntaxError('{0} tag requires one profile.type as arguments'.format(tokens[0]))

        nodelist_true = parser.parse(('else', 'endisprofile'))
        token = parser.next_token()
        if token.contents == 'else':
            nodelist_false = parser.parse(('endisprofile'))
            parser.delete_first_token()
        else:
            nodelist_false = template.NodeList()

        return cls(tokens[1], nodelist_true, nodelist_false)


register.tag('isprofile', IsProfileNode.tag)



def incont(value, cont):
    return value in cont

register.filter('in', incont)
