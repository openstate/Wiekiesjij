from django import template
from django.template.loader import get_template, TemplateDoesNotExist
from django.template import loader, Context
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

class RenderNode(template.Node):
    def __init__(self, width=None, height=None, allow_full_screen='true', allow_script_access='always'):
        self.width                  = template.Variable(width)
        self.height                 = template.Variable(height)
        self.allow_full_screen      = allow_full_screen
        self.allow_script_access    = allow_script_access

    def render(self, context):
        t = loader.get_template('core/youtube/video.html')

        context['yt_video']                 = context['video']
        context['yt_width']                 = self.width.resolve(context)
        context['yt_height']                = self.height.resolve(context)
        context['yt_allow_full_screen']     = self.allow_full_screen
        context['yt_allow_script_access']   = self.allow_script_access

        return t.render(context)

@register.tag
def yt_render(parser, token):
    '''
    Render you tube video with params.
    Syntax::
        <width> <height> <allow_full_screen> <allow_script_access>
    Example::
        advanced - {% yt_render 230 150 true always %}
        simple - {% yt_render %}
    '''
    tokens = token.split_contents()

    # TODO. Doesn't work with params yet.
    if 1 == len(tokens): # <width> <height> <allow_full_screen> <allow_script_access>
        return RenderNode()
    elif 3 == len(tokens): # <width> <height> <allow_full_screen> <allow_script_access>
        return RenderNode(tokens[1], tokens[2])