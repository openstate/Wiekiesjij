from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from elections.functions import get_profile_model


def staff_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user is staff, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_staff,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
    
    
def council_admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user is staff or has the council_admin profile, redirecting
    to the log-in page if necessary.
    """
    ProfileClass = get_profile_model('council_admin')
    actual_decorator = user_passes_test(
        lambda u: (u.is_staff or (u.profile is not None and isinstance(u.profile, ProfileClass))),
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
    
def party_admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user is staff or has a party_admin profile, redirecting
    to the log-in page if necessary.
    """
    ProfileClass = get_profile_model('party_admin')
    actual_decorator = user_passes_test(
        lambda u: (u.is_staff and (u.profile is not None and isinstance(u.profile, ProfileClass))),
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def candidate_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user is a candidate, redirecting
    to the log-in page if necessary.
    """

    ProfileClass = get_profile_model('candidate')
    actual_decorator = user_passes_test(
        lambda u: (u.is_staff or (u.profile is not None and isinstance(u.profile, ProfileClass))),
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator