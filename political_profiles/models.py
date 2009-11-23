from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class Profile(models.Model):
    """
    A abstract profile, put general shared profile information in here
    """
    user = models.OneToOneField(User, related_name="%(class)s", unique=True, verbose_name=_('User'))
    first_name = models.CharField(_('First name'), blank=True, max_length=80)
    middle_name = models.CharField(_('Middle name'), blank=True, max_length=80)
    last_name = models.CharField(_('Last name'), blank=True, max_length=80)
    
    class Meta:
        abstract = True
        verbose_name, verbose_name_plural = _('Profile'), _('Profiles')
    
class VisitorProfile(Profile):
    """
        A profile for visitors of the website when they "register"
    """
    class Meta:
        verbose_name, verbose_name_plural = _('Visitor Profile'), _('Visitor Profiles')
    
class PoliticianProfile(Profile):
    """
        A profile for a politician
    """
    class Meta:
        verbose_name, verbose_name_plural = _('Politician Profile'), _('Politicians Profiles')
    
class ChanceryProfile(Profile):
    """
        A profile for a chancery
    """
    class Meta:
        verbose_name, verbose_name_plural = _('Chancery Profile'), _('Chancery Profiles')
    
    
class ContactProfile(Profile):
    """
        A profile for a contact (for a party)
    """
    class Meta:
        verbose_name, verbose_name_plural = _('Contact Profile'), _('Contact Profiles')

def user_profile(u):
    """
        Function to always get the users profile as a profile property
        Returns None if no profile is found
    """
    if not hasattr(u, '_cached_profile'):
        try:
            u._cached_profile = u.visitorprofile
            return u._cached_profile
        except ObjectDoesNotExist:
            pass
        try:
            u._cached_profile = u.politicianprofile
            return u._cached_profile
        except ObjectDoesNotExist:
            pass
        try:
            u._cached_profile = u.chanceryprofile
            return u._cached_profile
        except ObjectDoesNotExist:
            pass
        try:
            u._cached_profile = u.contactprofile
            return u._cached_profile
        except ObjectDoesNotExist:
            pass
        u._cached_profile = None
            
    return u._cached_profile
# Python power, add the function as a property to the user
User.profile = property(user_profile)