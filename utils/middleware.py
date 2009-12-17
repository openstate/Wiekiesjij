from utils.exceptions import PermissionDeniedException
from utils import settings
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