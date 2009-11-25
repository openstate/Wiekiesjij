from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured

from elections import settings

def get_profile_app():
    """
        Return the profile app that's set to be used
    """
    try:
        package = import_module(settings.PROFILE_APP)
    except ImportError:
        raise ImproperlyConfigured("The PROFILE_APP setting refers to a non-existing package.")
        
    return package

def get_profile_model(for_function):
    """
        Return the profile model for a specific function
        Possible functions are:
        - 'candidate'
        - 'visitor'
        - 'council_admin'
        - 'party_admin'
    """
    return get_profile_app().get_profile_model(for_function)
    
    
def get_profile_forms(for_function, type):
    return get_profile_app().get_profile_forms(for_function, form_type)