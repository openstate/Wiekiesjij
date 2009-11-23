"""
    Intermediary module for validating and simplifying settings
"""
from django.conf import settings
from django.db import models

from django.core.exceptions import ImproperlyConfigured

def _check_model_settings(setting, name):
    """
        Checks if the setting is a valid app_label.model_name
    """
    if setting is not None:
        app_label, model_name = setting.split('.')
        m = models.get_model(app_label, model_name)
        if m is None:
            return
    raise ImproperlyConfigured('{0} setting needs to be in the format of `app_label.model_name`'.format(name))
    

CONTACT_LIMITATION = {}
if hasattr(settings, 'ELECTIONS_CONTACT_LIMITATION'):
    CONTACT_LIMITATION = settings.ELECTIONS_CONTACT_LIMITATION
    
CHANCERY_LIMITATION = {}
if hasattr(settings, 'ELECTIONS_CHANCERY_LIMITATION'):
    CHANCERY_LIMITATION = settings.ELECTIONS_CHANCERY_LIMITATION
    
POLITICIAN_LIMITATION = {}
if hasattr(settings, 'ELECTIONS_POLITICIAN_LIMITATION'):
    POLITICIAN_LIMITATION = settings.ELECTIONS_POLITICIAN_LIMITATION
    
    
QUESTION_MODEL = None
if hasattr(settings, 'ELECTIONS_QUESTION_MODEL'):
    QUESTION_MODEL = settings.ELECTIONS_QUESTION_MODEL
_check_model_settings(QUESTION_MODEL, 'ELECTIONS_QUESTION_MODEL')

ANSWER_MODEL = None
if hasattr(settings, 'ELECTIONS_ANSWER_MODEL'):
    ANSWER_MODEL = settings.ELECTIONS_ANSWER_MODEL
_check_model_settings(ANSWER_MODEL, 'ELECTIONS_ANSWER_MODEL')