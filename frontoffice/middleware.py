from django.template.defaultfilters import slugify
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from elections.models import ElectionInstance

class SubdomainMiddleware:
    """ Make the subdomain publicly available to classes """
    
    def process_request(self, request):
        domain_parts = request.get_host().split('.')
        if (len(domain_parts) > 2):
            subdomain = domain_parts[0]
            if (subdomain.lower() == 'www'):
                subdomain = ''
            domain = '.'.join(domain_parts[1:])
        else:
            subdomain = ''
            domain = request.get_host()
        
        print subdomain, domain
        if subdomain:
            ei_id = cache.get('%s-%s' % ('sdmid', subdomain))
            #If not found we update the cache for all of them
            if ei_id is None:
                for (id, name) in ElectionInstance.objects.values_list('id', 'name'):
                    subd = slugify(name)
                    cache.set('%s-%s' % ('sdmid', subd), id)
                    if subd == subdomain:
                        ei_id = id
            #might still be None
            if ei_id:
                url = reverse('fo.match_welcome', kwargs={'election_instance_id': ei_id})
                return HttpResponseRedirect('http://%s%s' % (domain, url))