import re, urllib, os, time, datetime, feedparser
from django import template
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import smart_str
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe


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
    return mark_safe("""
    <object width="425" height="344">
    <param name="movie" value="http://www.youtube.com/watch/v/%(video_id)s&rel=0"></param>
    <param name="allowFullScreen" value="true"></param>
    <embed src="http://www.youtube.com/watch/v/%(video_id)s&rel=0" type="application/x-shockwave-flash" allowfullscreen="true" width="425" height="344"></embed>
    </object>
    """ % {'video_id': video_id})


@register.filter
@stringfilter
def possessive(name):
    """
        Adds "s" "'s" or "'" to a name
        Customized for Dutch
    """
    vowels = set(['a','e','i','o','u','y']) #'y' is a vowel in most names
    esses = set(['s','x','z']) #characters with an 's'-sound
    last_char = name[-1]

    if last_char in vowels:
        return name+"'s"
    elif last_char in esses:
        return name+"'"
    else:
        return name+"s"


@register.inclusion_tag('utils_tags/_tweets.html')
def pull_feed(feed_url, posts_to_show=5, cache_expires=60):
    """
        Reads, parses and caches RSS feed.
        http://www.djangosnippets.org/snippets/384/
        Addapted version for Twitter messages.
    """

    CACHE_FOLDER = settings.TMP_ROOT + '/'
    CACHE_FILE = ''.join([CACHE_FOLDER, template.defaultfilters.slugify(feed_url), '.cache'])
    try:
        cache_age = os.stat(CACHE_FILE)[8]
    except: #if file doesn't exist, make sure it gets created
        cache_age = 0
    #is cache expired? default 60 minutes (60*60)
    if (cache_age + cache_expires*60 < time.time()):
        try: #refresh cache
            urllib.urlretrieve(feed_url,CACHE_FILE)
        except IOError: #if downloading fails, proceed using cached file
            pass
    #load feed from cache
    feed = feedparser.parse(open(CACHE_FILE))
    #set regex shizzle for actually parsing the messages
    url_regex = re.compile(r"([A-Za-z]+://[A-Za-z0-9-_]+\.[A-Za-z0-9-_:%&?/.=]+)") #url
    usn_regex = re.compile(r"[@]([A-Za-z0-9-_]+)") #username
    htg_regex = re.compile(r"[#]([A-Za-z0-9-_]+)") #hashtag
    pos_regex = re.compile(r"^([A-Za-z0-9-_]+:)") #remove poster name
    
    posts = []
    for i in range(posts_to_show):
        pub_date = feed['entries'][i].updated_parsed
        #TODO: Twitter delivers time in GMT (probably). We don't live in Greenwich.
        published = datetime.datetime(*pub_date[:6])

        #make links out of URLs, @usernames and #hashtags and remove username of politician
        summary = url_regex.sub(r'<a href="\g<1>">\g<1></a>', feed['entries'][i].summary)
        summary = usn_regex.sub(r'@<a href="http://twitter.com/\g<1>">\g<1></a>', summary)
        summary = htg_regex.sub(r'#<a href="http://search.twitter.com/search?q=%23\g<1>">\g<1></a>', summary)
        summary = pos_regex.sub('', summary)

        posts.append({
            'title': mark_safe(feed['entries'][i].title),
            'summary': mark_safe(summary),
            'link': mark_safe(feed['entries'][i].link),
            'published': published,
        })
    return {'posts': posts}


@register.filter
def age(bday, d=None):
    if bday is None:
        return ''
    if d is None:
        d = datetime.date.today()
    return (d.year - bday.year) - int((d.month, d.day) < (bday.month, bday.day))



class CompareBlockNode(template.Node):
    """
        Complex comparison tags.
        
        Compares two values and returns the normal bit it they are equal,
        the smaller bit if the first is smaller then the second one
        and the bigger bit if it's bigger
        Smaller and bigger are optional and will result in the equal block being rendered if left out
    """
    
    
    def __init__(self, value1, value2, nodelist_equal, nodelist_bigger, nodelist_smaller):
        self.value1 = template.Variable(value1)
        self.value2 = template.Variable(value2)
        
        self.nodelist_equal = nodelist_equal
        self.nodelist_bigger = nodelist_bigger
        self.nodelist_smaller = nodelist_smaller
        

    def render(self, context):
        value1 = self.value1.resolve(context)
        value2 = self.value2.resolve(context)
        
        if value1 < value2:
            if self.nodelist_smaller:
                return self.nodelist_smaller.render(context)
        elif value1 > value2:
            if self.nodelist_bigger:
                return self.nodelist_bigger.render(context)
        return self.nodelist_equal.render(context)
        
    @classmethod
    def tag(cls, parser, token):
        tokens = token.split_contents()

        if len(tokens) != 3:
            raise template.TemplateSyntaxError('{0} tag requires two values to compare'.format(tokens[0]))


        nodelist_equal = parser.parse(('smaller', 'bigger', 'endifcompare'))    
        token = parser.next_token()
        
        nodelist_smaller = None
        nodelist_bigger = None
        
        if token.contents == 'smaller':
            nodelist_smaller = parser.parse(('bigger', 'endifcompare'))
            token2 = parser.next_token()
        elif token.contents == 'bigger':
            nodelist_bigger = parser.parse(('smaller', 'endifcompare'))
            token2 = parser.next_token()
        
        if token2.contents == 'smaller':
            nodelist_smaller = parser.parse(('endifcompare'))
            token2 = parser.delete_first_token()
        elif token2.contents == 'bigger':
            nodelist_bigger = parser.parse(('endifcompare'))
            token2 = parser.delete_first_token()

        return cls(tokens[1], tokens[2], nodelist_equal, nodelist_bigger, nodelist_smaller)

register.tag('ifcompare', CompareBlockNode.tag)
