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
    
    
def get_profile_forms(for_function, form_type):
    return get_profile_app().get_profile_forms(for_function, form_type)
    
    
def create_profile(for_function, data):
    """
        Creates a profile for the given for_function using the data
    """
    return get_profile_app().create_profile(for_function, data)
    
    
def profile_invite_email_templates(for_function):
    """
        Get the templates to use for sending an invitation
        
        Returns a dict with a plain and a hhtml key pointing to the template files to use
    """
    return get_profile_app().profile_invite_email_templates(for_function)
    
    
def replace_user(original_user, new_user, delete_original=True):
    """
        Function to replace the original_user with the new_user
        Handles all the related profile stuff too
    """
    return get_profile_app().replace_user(original_user, new_user, delete_original)
    
    
def get_profile_template(for_function, type):
    """
        Get the template to use to display a certain profile
        Returns False if not found
    """
    return get_profile_app().get_profile_template(for_function, type)