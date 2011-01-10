from django import template

register = template.Library()

@register.filter
def dict_to_querystring(query_dict):
    #query_dict = data.get(index, {})
    return '?' + '&'.join([u'%s=%s' % (k, v) for k, v in query_dict.iteritems()]).replace(' ', '%20') 
    
@register.inclusion_tag('statistics/_chart.html')
def draw_chart(dataset, eip, description=''):
    return {
        'dataset': dataset.get(eip.pk),
        'eip': eip,
        'description': description,
    }