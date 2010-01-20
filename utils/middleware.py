import json
import re

from utils.exceptions import PermissionDeniedException
from utils import settings
from utils.models import PostLog
from django.http import HttpResponseRedirect

class PermissionDeniedMiddleware(object):
    """
        Catches PermissionDeniedException exceptions
        and redirects to login page
    """
    def process_exception(self, request, exception):
        
        #Ignore everything that's not a PermissionDeniedException
        if not isinstance(exception, PermissionDeniedException):
            return None
            
        return HttpResponseRedirect('%s?next=%s' % (settings.PERMISSION_DENIED_URL, request.path))
        
        
        
class PostLogMiddleware(object):
    """
        Catches specified urls post data
    """
    
    def process_request(self, request):
        if request.method == "POST":
            for url in settings.POSTLOG_URLS:    
                if re.match(url, request.path):
                    user = None
                    if request.user and request.user.is_authenticated():
                        user = request.user
                
                    PostLog.objects.create(
                        path=request.path,
                        user=user,
                        ipaddress=request.META['REMOTE_ADDR'],
                        data=json.dumps(request.POST, sort_keys=True, indent=2)
                    )
            
        return None