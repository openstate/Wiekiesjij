import json
import re
import sys
import base64
from functools import wraps

from django.views.debug import technical_500_response
from django.conf import settings as django_settings

from utils.exceptions import PermissionDeniedException
from utils.netutils import getip
from utils import settings
from utils.models import PostLog
from django.http import HttpResponseRedirect

from django.http import HttpResponse
from django.contrib.auth import authenticate

class HttpAuthMiddleware(object):
    """
    Some middleware to authenticate all requests at this site.
    """
    def process_request(self, request):
        return _http_auth_helper(request)

def http_auth(func):
    """
    A decorator, that can be used to authenticate some requests at the site.
    """
    @wraps(func)
    def inner(request, *args, **kwargs):
        result = _http_auth_helper(request)
        if result is not None:
            return result
        return func(request, *args, **kwargs)
    return inner


def _http_auth_helper(request):
    "This is the part that does all of the work"
    try:
        if not django_settings.FORCE_HTTP_AUTH:
            # If we don't mind if django's session auth is used, see if the
            # user is already logged in, and use that user.
            if request.user:
                return None
    except AttributeError:
        pass
        
    # At this point, the user is either not logged in, or must log in using
    # http auth.  If they have a header that indicates a login attempt, then
    # use this to try to login.
    if request.META.has_key('HTTP_AUTHORIZATION'):
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            if auth[0].lower() == 'basic':
                # Currently, only basic http auth is used.
                uname, passwd = base64.b64decode(auth[1]).split(':')
                user = authenticate(username=uname, password=passwd)
                if user:
                    # If the user successfully logged in, then add/overwrite
                    # the user object of this request.
                    request.user = user
                    return None
    
    # The username/password combo was incorrect, or not provided.
    # Challenge the user for a username/password.
    resp = HttpResponse()
    resp.status_code = 401
    try:
        # If we have a realm in our settings, use this for the challenge.
        realm = django_settings.HTTP_AUTH_REALM
    except AttributeError:
        realm = ""
    
    resp['WWW-Authenticate'] = 'Basic realm="%s"' % realm
    return resp





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
                        ipaddress=getip(request),
                        data=json.dumps(request.POST, sort_keys=True, indent=2)
                    )
            
        return None
        
        
class UserBasedExceptionMiddleware(object):
    """
        User based exception middleware
        Shows the technical exception when logged in as superuser or 
        when accessing from one of the internal ips
        
        @see http://ericholscher.com/blog/2008/nov/15/debugging-django-production-environments/
    """
    def process_exception(self, request, exception):
        if request.user.is_superuser or getip(request) in django_settings.INTERNAL_IPS:
            return technical_500_response(request, *sys.exc_info())