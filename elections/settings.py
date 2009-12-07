"""
    Intermediary module for validating and simplifying settings
"""
from django.conf import settings
from django.db import models
from django.core.exceptions import ImproperlyConfigured
    

CONTACT_LIMITATION = getattr(settings, 'ELECTIONS_CONTACT_LIMITATION', {})
CHANCERY_LIMITATION = getattr(settings, 'ELECTIONS_CHANCERY_LIMITATION', {})
POLITICIAN_LIMITATION = getattr(settings, 'ELECTIONS_POLITICIAN_LIMITATION', {})

PROFILE_APP = getattr(settings, 'ELECTIONS_PROFILE_APP', None)
if PROFILE_APP is None or PROFILE_APP not in settings.INSTALLED_APPS:
    raise ImproperlyConfigured('ELECTIONS_PROFILE_APP incorrect or invalid, could not find the app "%(app)s" in the INSTALLED_APPS' % {'app': PROFILE_APP})

ELECTION_EVENT_ID = getattr(settings, 'ELECTIONS_ELECTION_EVENT_ID', None)
if ELECTION_EVENT_ID is None:
    raise ImproperlyConfigured('ELECTIONS_ELECTION_EVENT_ID is missing from the settings')