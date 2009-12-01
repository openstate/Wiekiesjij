from django import template

register = template.Library()


class InsertStyleGroupNode(template.Node):
    
    def __init__(self, stylegroup):
        self.stylegroup = template.Variable(stylegroup)
        
    def render(self, context):
        stylegroup = self.stylegroup.resolve(context)
        try:
            email_classes = context['email_classes']
            return email_classes[stylegroup]
        except KeyError:
            pass
        return ''
        
        
    @classmethod
    def tag(cls, parser, token):
        try:
            tag, stylegroup = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError, "%r tag requires exactly one arguments" % token.contents.split()[0]
        return cls(stylegroup)
        
register.tag('use_stylegroup', InsertStyleGroupNode.tag)


class StyleGroupNode(template.Node):
    
    def __init__(self, name, nodelist):
        self.name = template.Variable(name)
        self.nodelist = nodelist
        
    def render(self, context):
        try:
            email_classes = context['email_classes']
        except KeyError:
            email_classes = {}
            
        name = self.name.resolve(context)
        email_classes.update({
            name: self.nodelist.render(context)
        })
        context['email_classes'] = email_classes
        return ''
        
    @classmethod
    def tag(cls, parser, token):
        try:
            tag, stylegroup = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError, "%r tag requires exactly one argument" % token.contents.split()[0]
            
        nodelist = parser.parse(('end_stylegroup', ))
        parser.delete_first_token()
        return cls(stylegroup, nodelist)
        
register.tag('stylegroup', StyleGroupNode.tag)