from django import template
from django.template.loader import render_to_string
from django.utils.encoding import smart_str
from django.template.loader import get_template, TemplateDoesNotExist
from django.conf import settings
from django.utils.safestring import mark_safe
import os # Thumbnails
import Image # Thumbnails
from django.template import Library
from django.http import QueryDict # For parsing parameters

register = Library()

SCALE_WIDTH = 'w'
SCALE_HEIGHT = 'h'
SCALE_BOTH = 'both'

def scale(max_x, pair):
    ''' scales an image to the desired size '''
    x, y = pair
    new_y = (float(max_x) / x) * y
    return (int(max_x), int(new_y))


@register.filter
def thumbnail2(file, size='200w'):
    ''' creates a thumbnail of the picture supplied '''
    # defining the size
    if (size.lower().endswith('h')):
        mode = 'h'
        size = size[:-1]
        max_size = int(size.strip())
    elif (size.lower().endswith('w')):
        mode = 'w'
        size = size[:-1]
        max_size = int(size.strip())
    else:
        mode = 'both'

    # defining the filename and the miniature filename
    filehead, filetail = os.path.split(file.path)
    basename, format = os.path.splitext(filetail)
    miniature = basename + '_' + size + format
    filename = file.path
    miniature_filename = os.path.join(filehead, miniature)
    filehead, filetail = os.path.split(file.url)
    miniature_url = filehead + '/' + miniature
    if os.path.exists(miniature_filename) and os.path.getmtime(filename)>os.path.getmtime(miniature_filename):
        os.unlink(miniature_filename)
    # if the image wasn't already resized, resize it
    if not os.path.exists(miniature_filename):
        image = Image.open(filename)
        image_x, image_y = image.size

        if mode == SCALE_HEIGHT:
            image_y, image_x = scale(max_size, (image_y, image_x))
        elif mode == SCALE_WIDTH:
            image_x, image_y = scale(max_size, (image_x, image_y))
        elif mode == SCALE_BOTH:
            image_x, image_y = [int(x) for x in size.split('x')]
        else:
            raise Exception("Thumbnail size must be in ##w, ##h, or ##x## format.")

        image.thumbnail([image_x, image_y], Image.ANTIALIAS)
        try:
            image.save(miniature_filename, image.format, quality=90, optimize=1)
        except:
            image.save(miniature_filename, image.format, quality=90)

    return miniature_url


'''
Usage example: From HTML template <img src="{{ image.image_file|thumbnail:'size=50x50&greyscale=True&repeat=V' }}" />
Parameters example: size=104x104&repeat=False&greyscale=False
Parameters in detail:
    - size: Is widthxheight
    - greyscale: Possible values (True, False). If set to True image is greyscaled. If other value given - ignored.
    - repeat: Possible values (H, V). If other value given - ignored. If specified, image is repeated horizontally
              or vertically. If greyscale is specified, repeated image is made black and white.
'''
@register.filter("thumbnail")
def thumbnail(file, args='size=104x104'):
    ''' creates a thumbnail of the picture supplied '''

    # defining the size
    params = QueryDict(args) # Getting params as a query dictionary

    # Default values
    repeat = None
    greyscale = None

    # Getting the size
    if params.has_key('size'):
        size = params['size']
        x, y = [int(x) for x in params['size'].split('x')]
    else:
        size = '100x100'
        x, y = [int(x) for x in size.split('x')]

    # Checking if shall be made greyscale
    if params.has_key('greyscale') and params['greyscale'] in ('True', 'False'):
        greyscale = bool(params['greyscale'])

    # Checking if shall be repeated (H = horizontal, V = vertical)
    if params.has_key('repeat') and params['repeat'] in ('V', 'H'):
        repeat = params['repeat']
    
    # defining the filename and the miniature filename
    filehead, filetail = os.path.split(file.path)
    basename, format = os.path.splitext(filetail)
    miniature = basename + '_' + args.replace('&', ' ') + format
    filename = file.path
    miniature_filename = os.path.join(filehead, miniature)
    filehead, filetail = os.path.split(file.url)
    miniature_url = filehead + '/' + miniature
    if os.path.exists(miniature_filename) and os.path.getmtime(filename)>os.path.getmtime(miniature_filename):
        os.unlink(miniature_filename)
    # if the image wasn't already resized, resize it
    if not os.path.exists(miniature_filename):
        image = Image.open(filename)

        if repeat:
            original = image
            original.thumbnail([x, y], Image.ANTIALIAS)

            bw = image
            if greyscale == True:
                bw = bw.convert('L')

            bw.thumbnail([x, y], Image.ANTIALIAS)

            if repeat == 'V': # Vertical
                combi = Image.new('RGB', (original.size[0], original.size[1] * 2))
                combi.paste(original, (0, 0))
                combi.paste(bw, (0, original.size[1]))
            else: # Horizontal
                combi = Image.new('RGB', (original.size[0] * 2, original.size[1]))
                combi.paste(original, (0, 0))
                combi.paste(bw, (original.size[0], 0))

            try:
                combi.save(miniature_filename, image.format, quality=90, optimize=1)
            except:
                combi.save(miniature_filename, image.format, quality=90)

        else:
            image.thumbnail([x, y], Image.ANTIALIAS)

            if greyscale == True:
                image = image.convert('L')

            try:
                image.save(miniature_filename, image.format, quality=90, optimize=1)
            except:
                image.save(miniature_filename, image.format, quality=90)

    return miniature_url


@register.filter
def render_search_result(result):
    """
    Renders a search result.

    {% if page.object_list %}
        {% for result in page.object_list %}
            <div>{{ result|render_search_result }}</div>
        {% endfor %}
    {% else %}
        <p>No results found.</p>
    {% endif %}
    """

    app_label = result.content_type().split('.')[0]
    model_label = result.content_type().split('.')[1]

    try:
        t = get_template("search/result/%s/%s.html" % (app_label, model_label))
    except TemplateDoesNotExist:
        t = get_template("search/result/default.html")

    return t.render(template.Context({
        'object': result.object,
    }))


@register.filter("truncate_chars")
def truncate_chars(value, max_length):
    '''
    Truncates characters.
    Example of usage: {{ product.name|truncate_chars:25 }}
    '''
    if len(value) > max_length:
        truncd_val = value[:max_length]
        return  truncd_val + "..."
    return value

@register.filter
def math_minus(value, minus):
    '''
    Math minus operation. Decreases the given variable by given value
    Example of usage: {{ forloop.counter|math_minus:2 }}
    '''
    value = float(value)
    return value - minus

@register.filter
def math_plus(value, plus):
    '''
    Math plus operation. Increases the given variable by given value
    Example of usage: {{ forloop.counter|math_plus:3 }}
    '''
    value = float(value)
    plus = float(plus)
    return value + plus

@register.filter
def str_replace (value, args):
    ''' Search and replace functionality'''
    params = args.split(':')
    search = params[0]
    replace = params[1]
    return value.replace(search, replace)


@register.simple_tag
def js_comment(string):
    ''' Set TEMPLATE_COMMENTS as true if you want to comment out javascript - useful for debugging - Artur'''
    if settings.TEMPLATE_COMMENTS:
        return '<!--' + string + '-->'

@register.filter
def in_list(value, args):
    '''
    Finds out if an item is in list
    Example of usage:
    {% if item|in_list:list %}
        in list
    {% else %}
        not in list
    {% endif %}

    '''
    return value in args

@register.filter
def to_string(value):
    return str(value)

@register.filter
def greater_than(value, args):
    '''
    Finds out if a value is greater than a given value
    Example of usage:
    {% if item|greater_than:3 %}
        is greater
    {% else %}
        is not greater
    {% endif %}

    '''
    value = float(value)
    args = float(args)
    return value > args

@register.filter
def less_than(value, args):
    '''
    Finds out if an value is less than than a given value
    Example of usage:
    {% if item|less_than:3 %}
        is less
    {% else %}
        is not less
    {% endif %}

    '''
    value = (value)
    args = (args)
    return value < args

class AssignNode(template.Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def render(self, context):
        context[self.name] = self.value.resolve(context, True)
        return ''

@register.tag
def assign(parser, token):
    """
    Assign an expression to a variable in the current context.

    Syntax::
        {% assign [name] [value] %}
    Example::
        {% assign list entry.get_related %}

    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    value = parser.compile_filter(bits[2])
    return AssignNode(bits[1], value)

@register.filter
def cat(value, args):
    """
    add two strings together.

    Syntax::
        <value>|cat:extra string
    Example::
        {% 'lorem ipsum'|cat:'dolor sit amet' %}

    """
    args = str(args)
    value = str(value)

    full_string = value + args
    return full_string

@register.filter
def str_repeat(value, args):
    '''
    Repeats the given string number of times.

    Syntax::
        <value>|str_repeat:<number_of_times>
    Example::
        {% 'lorem'|str_repeat:3 %}
    '''
    args = int(args)
    value = str(value)

    if args > 0:
        return value * args
    else:
        return value

@register.filter
def trim(value):
    return mark_safe(value).strip()


class BlockwrapNode(template.Node):
    """
        Wraps the nodelist using the given template and kwargs
    """
    def __init__(self, nodelist, template_name, extra_args):
        self.nodelist = nodelist
        self.kwargs = extra_args
        self.template_name = template_name

    def render(self, context):
        kwargs = dict([(smart_str(k,'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])

        template_name = self.template_name.resolve(context)
        # if someone added a content variable to the kwargs, tough luck
        kwargs['content'] = self.nodelist.render(context)

        template_search_list = [
            "templateblocks/{0}.html".format(template_name),
        ]
        context.push()
        formstr = render_to_string(template_search_list, kwargs, context)
        context.pop()
        return formstr

register = template.Library()

@register.tag
def blockwrap(parser, token):
    """
         Wraps the content using a template

        Example usage::

            {% blockwrap %}
                Somecontent
            {% endblockwrap %}

        This example would render the default template 'templateblocks/default.html'
        passing the wrapped content as a content variable to the template

        Another example::
            {% blockwrap template='myown' title='Some title'}
                Some content
            {% endblockwrap %}

        This example would render 'templateblocks/myown.html' with in the context the title and content variables

    """
    tokens = token.split_contents()
    kwargs = {}
    template_name = 'default'

    if len(tokens) > 2:
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
