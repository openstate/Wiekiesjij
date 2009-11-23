"""
    Intermediary module for validating and simplifying settings
"""
from django.conf import settings
from django.db import models
    

CONTACT_LIMITATION = {}
if hasattr(settings, 'ELECTIONS_CONTACT_LIMITATION'):
    CONTACT_LIMITATION = settings.ELECTIONS_CONTACT_LIMITATION
    
CHANCERY_LIMITATION = {}
if hasattr(settings, 'ELECTIONS_CHANCERY_LIMITATION'):
    CHANCERY_LIMITATION = settings.ELECTIONS_CHANCERY_LIMITATION
    
POLITICIAN_LIMITATION = {}
if hasattr(settings, 'ELECTIONS_POLITICIAN_LIMITATION'):
    POLITICIAN_LIMITATION = settings.ELECTIONS_POLITICIAN_LIMITATION