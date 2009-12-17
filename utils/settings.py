from django.conf import settings

PERMISSION_DENIED_URL = getattr(settings, 'UTILS_PERMISSION_DENIED_URL', None)
if PERMISSION_DENIED_URL is None:
    PERMISSION_DENIED_URL = '/permission_denied/'