from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from utils import settings



def visitors_only(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
        Decorator for views that checks that the user is a visitor, redirecting
        to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: (u.is_authenticated() and u.profile is not None and 'visitor' == u.profile.type),
        login_url=settings.PERMISSION_DENIED_URL,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def politicians_only(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
        Decorator for views that checks that the user is a politician, redirecting
        to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: (u.is_authenticated() and u.profile is not None and 'candidate' == u.profile.type),
        login_url=settings.PERMISSION_DENIED_URL,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator