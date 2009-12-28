import re

from django import template
from django.template.loader import render_to_string
from django.utils.encoding import smart_str
from django.template.defaultfilters import stringfilter


register = template.Library()

class BlockwrapNode(template.Node):
    """
        Wraps the nodelist using the given template and kwargs
    """
    def __init__(self, nodelist, template_name=None, extra_args={}):
        self.nodelist = nodelist
        self.kwargs = extra_args
        self.template_name = template_name

    def render(self, context):
        kwargs = dict([(smart_str(k,'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])

        if self.template_name is None:
            template_name = 'default'
        else:
            template_name = self.template_name.resolve(context)

        # if someone added a content variable to the kwargs, tough luck
        kwargs['content'] = self.nodelist.render(context)

        template_search_list = [
            "utils/blockwrap/_{0}.html".format(template_name),
        ]
        context.push()
        result = render_to_string(template_search_list, kwargs, context)
        context.pop()
        return result


@register.tag
def blockwrap(parser, token):
    """
         Wraps the content using a template

        Example usage::

            {% blockwrap %}
                Somecontent
            {% endblockwrap %}

        This example would render the default template 'utils/blockwrap/_default.html'
        passing the wrapped content as a content variable to the template

        Another example::
            {% blockwrap template='myown' title='Some title'}
                Some content
            {% endblockwrap %}

        This example would render 'utils/blockwrap/_myown.html' with in the context the title and content variables

    """
    tokens = token.split_contents()
    kwargs = {}
    template_name = None
    if len(tokens) >= 2:
        bits = iter(tokens[1:])
        for bit in bits:
            if '=' in bit:
                k, v = bit.split('=', 1)
                k = k.strip()
                if k == 'template':
                    template_name = parser.compile_filter(v)
                else:
                    kwargs[k] = parser.compile_filter(v)
            else:
                 raise template.TemplateSyntaxError('{0} tag only accepts keyword arguments !'.format(tokens[0]))

    nodelist = parser.parse(('endblockwrap', ))
    parser.delete_first_token()
    return BlockwrapNode(nodelist, template_name, kwargs)
    
    
@register.filter
@stringfilter
def youtube(url):
    """
        Changes an youtube url to an embeded video
    """
    regex = re.compile(r"^(http://)?(www\.)?(youtube\.com/watch\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})")
    match = regex.match(url)
    if not match: return ""
    video_id = match.group('id')
    return """
    <object width="425" height="344">
    <param name="movie" value="http://www.youtube.com/watch/v/%(video_id)s"></param>
    <param name="allowFullScreen" value="true"></param>
    <embed src="http://www.youtube.com/watch/v/%(video_id)s" type="application/x-shockwave-flash" allowfullscreen="true" width="425" height="344"></embed>
    </object>
    """ % {'video_id': video_id}
youtube.is_safe = True # Don't escape HTML
