from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from utils import settings

from elections.functions import get_profile_model


def superuser_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user is a superuser, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_superuser,
        login_url=settings.PERMISSION_DENIED_URL,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
    
def staff_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user is staff, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_staff,
        login_url=settings.PERMISSION_DENIED_URL,
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
    actual_decorator = user_passes_test(
        lambda u: (u.is_authenticated() and (u.is_staff or (u.profile is not None and 'council_admin' == u.profile.type))),
        login_url=settings.PERMISSION_DENIED_URL,
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
    actual_decorator = user_passes_test(
        lambda u: (u.is_authenticated() and (u.is_staff or (u.profile is not None and u.profile.type in ('party_admin', 'council_admin')))),
        login_url=settings.PERMISSION_DENIED_URL,
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
    actual_decorator = user_passes_test(
        lambda u: (u.is_authenticated() and (u.is_staff or (u.profile is not None and u.profile.type in ('candidate', 'party_admin', 'council_admin')))),
        login_url=settings.PERMISSION_DENIED_URL,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def log_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user is a contact, redirecting
    to the log-in page if necessary.
    """

    actual_decorator = user_passes_test(
        lambda u: (u.is_authenticated()),
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator