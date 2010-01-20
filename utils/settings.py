from django.conf import settings

PERMISSION_DENIED_URL = getattr(settings, 'UTILS_PERMISSION_DENIED_URL', None)
if PERMISSION_DENIED_URL is None:
    PERMISSION_DENIED_URL = '/permission_denied/'
    
    
POSTLOG_URLS = getattr(settings, 'UTILS_POSTLOG_URLS', None)
if POSTLOG_URLS is None:
    POSTLOG_URLS = []