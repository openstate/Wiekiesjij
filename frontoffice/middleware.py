from django.conf import settings
from django.template.defaultfilters import slugify
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from elections.models import ElectionInstance

class SubdomainMiddleware:
    """ Make the subdomain publicly available to classes """
    
    def process_request(self, request):
        ei_id = None
        domain_parts = request.get_host().split('.')
        if (len(domain_parts) > 2):
            subdomain = domain_parts[0]
            if (subdomain.lower() == 'www'):
                subdomain = ''
            domain = '.'.join(domain_parts[1:])
        else:
            subdomain = ''
            domain = request.get_host()
        
        if subdomain and not subdomain.isdigit():
            result = cache.get('%s-%s' % ('sdmid', subdomain))
            #If not found we update the cache for all of them
            if result is None:
                for (id, name) in ElectionInstance.objects.values_list('id', 'name'):
                    subd = slugify(name)
                    cache.set('%s-%s' % ('sdmid', subd), (id, name))
                    if subd == subdomain:
                        ei_id = id
                        ei_name = name
                        
            else:
                (ei_id, ei_name) = result
            
            #might still be None
            if ei_id:
                request.session['ElectionInstance'] = {'id': ei_id, 'name': ei_name}
                url = reverse('fo.match_welcome', kwargs={'election_instance_id': ei_id})
                return HttpResponseRedirect('http://%s%s' % (domain, url))