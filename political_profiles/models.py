from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from tagging.fields import TagField

GENDERS = (('Male',_('Male')),
           ('Female', _('Female')))

# Profiles
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
    
    def full_name(self):
        return ' '.join(filter(lambda x: x, (self.first_name, self.middle_name, self.last_name)))
    
class VisitorProfile(Profile):
    """
        A profile for visitors of the website when they "register"
    """
    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name, verbose_name_plural = _('Visitor Profile'), _('Visitor Profiles')
    
class PoliticianProfile(Profile):
    """
        A profile for a politician
    """
    initials        = models.CharField(_('Level'), max_length=15)
    gender          = models.CharField(_('Gender'), max_length=25,choices=GENDERS , help_text=_("Please choose your gender."), default='Male')
    dateofbirth     = models.DateField(_('Start Date'))
    picture         = models.ImageField(_('Picture'), upload_to='media/politician')
    width           = models.PositiveIntegerField(editable=False, default=0, null=True)
    height          = models.PositiveIntegerField(editable=False, default=0, null=True)
    movie           = models.URLField(_('Movie'), max_length=255, verify_exists=True, help_text=_('Link to YouTube video'))
    introduction    = models.CharField(_('Introduction'), max_length=2550)
    motivation      = models.CharField(_('Motivation'), max_length=2550)
    #hobby = models.CharField(_('Hobbies'), max_length=255)
	#charity = models.CharField(_('Favourite Charities'), max_length=255)
    #pets =  models.CharField(_('Pets'), max_length=255)
    #fanclubs = models.CharField(_('Fan Clubs'), max_length=255)
    #goals		Refrence
    #Votes		Reference
    #Expenses	Reference
    
    def profile_incomplete(self):
        return False

    def __unicode__(self):
        return self.user.username
    
    class Meta:
        verbose_name, verbose_name_plural = _('Politician Profile'), _('Politician Profiles')

class ChanceryProfile(Profile):
    """
        A profile for a chancery
    """
    gender      = models.CharField(_('Gender'), max_length=25,choices=GENDERS)
    telephone	= models.CharField(_('Phone Number'), max_length=255)
    workingdays = models.CharField(_('Working Days'), max_length=255)
    street      = models.CharField(_('Street'), max_length=40)
    house_num   = models.CharField(_('House Number'), max_length=5)
    postcode  	= models.CharField(_('Postcode'), max_length=7, help_text=_("Postcode (e.g. 9725 EK or 9211BV)"))
    town        = models.CharField(_('Town/City'), max_length=30)
    website     = models.URLField(_('Councils Website'), max_length=255, verify_exists=True, null=True, blank=True)

    picture     = models.ImageField(_('Picture'), upload_to='media/chancery')


    description = models.CharField(_('Description'), max_length=255, help_text=_("A short description of the council"),
                null=True, blank=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name, verbose_name_plural = _('Chancery Profile'), _('Chancery Profiles')
    #Expenses	Reference



class ContactProfile(Profile):
    """
        A profile for a contact (for a party)
    """
    gender = models.CharField(_('Gender'), max_length=25, choices=GENDERS, help_text=_("Please choose your gender."))
    telephone	= models.CharField(_('Phone Number'), max_length=255)
    workingdays = models.CharField(_('Working Days'), max_length=255)
    street      = models.CharField(_('Street'), max_length=40)
    house_num   = models.CharField(_('House Number'), max_length=5)
    postcode  	= models.CharField(_('Postcode'), max_length=7, help_text=_("Postcode (e.g. 9725 EK or 9211BV)"))
    town        = models.CharField(_('Town/City'), max_length=30)
    website     = models.URLField(_('Councils Website'), max_length=255, verify_exists=True, null=True, blank=True)
    picture     = models.ImageField(_('Picture'), upload_to='media/contact')
    width       = models.PositiveIntegerField(editable=False, default=0, null=True)
    height      = models.PositiveIntegerField(editable=False, default=0, null=True)
    description = models.CharField(_('Description'), max_length=255, help_text=_("A short description of yourself"),
                                   null=True, blank=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name, verbose_name_plural = _('Contact Profile'), _('Contact Profiles')
    #Expenses	Reference


# Profile Attribute Classes

class Link(models.Model):
    """
        A class to hold a link to the politician
    """
    name        = models.CharField(_('Name'), max_length=255)
    url         = models.CharField(_('URL'), max_length=255)
    description	= models.CharField(_('Description'), max_length=2550)
    politician  = models.ForeignKey(PoliticianProfile, verbose_name=_('Politician'))

    class Meta:
        verbose_name, verbose_name_plural = _('Link'), _('Links')

class Interest(models.Model):
    """
        A class to hold an interest of the politician
    """
    organization    = models.CharField(_('Organisation Name'), max_length=255)
    url             = models.CharField(_('URL'), max_length=255)
    description     = models.CharField(_('Description'), max_length=2550)
    politician  = models.ForeignKey(PoliticianProfile, verbose_name=_('Politician'))

    class Meta:
        verbose_name, verbose_name_plural = _('Intrest'), _('Intrests')

class Appearence(models.Model):
    """
        A class to hold an aperance (where they attended somthing) of the politician
    """
    name        = models.CharField(_('Affiliated Organisation Name'), max_length=255)
    location	= models.CharField(_('Location'), max_length=255)
    url         = models.CharField(_('URL'), max_length=255)
    description = models.CharField(_('Description'), max_length=2550)
    datetime    = models.DateTimeField(_('Date and Time of Appearance'))
    politician  = models.ForeignKey(PoliticianProfile, verbose_name=_('Politician'))

    class Meta:
        verbose_name, verbose_name_plural = _('Politician Appearance'), _('Politician Appeariences')

class WorkExperience(models.Model):
    """
        A class to hold work experience
    """
    company_name 	= models.CharField(_('Company Name'), max_length=255)
    sector          = models.CharField(_('Sector'), max_length=255)
    position        = models.CharField(_('Position'), max_length=255)
    startdate       = models.DateField(_('Start Date'))
    enddate         = models.DateField(_('End Date'))
    current         = models.BooleanField(_('Currently employed'), default=False)
    description     = models.CharField(_('Description'), max_length=2550)
    politician  = models.ForeignKey(PoliticianProfile, verbose_name=_('Politician'))

    class Meta:
        verbose_name, verbose_name_plural = _('Work experience'), _('Work experience')

class Education(models.Model):
    """
        A period of education
    """
    institute   = models.CharField(_('Institute Name'), max_length=255)
    level       = models.CharField(_('Level'), max_length=255)
    field       = models.CharField(_('Field'), max_length=255)
    startdate   = models.DateField(_('Start Date'))
    enddate     = models.DateField(_('End Date'))
    description = models.CharField(_('Description'), max_length=2550)
    politician  = models.ForeignKey(PoliticianProfile, verbose_name=_('Politician'))

    class Meta:
        verbose_name, verbose_name_plural = _('Education'), _('Education')

class PoliticalExperience(models.Model):
    """
        Experience in the political world
    """
    organisation    = models.CharField(_('Organisation'), max_length=255)
    type            = models.CharField(_('Level'), max_length=255)
    position        = models.CharField(_('Level'), max_length=255)
    startdate       = models.DateField(_('Start Date'))
    enddate         = models.DateField(_('End Date'))
    description     = models.CharField(_('Description'), max_length=2550)
    politician  = models.ForeignKey(PoliticianProfile, verbose_name=_('Politician'))
    tags            = TagField()
    class Meta:
        verbose_name, verbose_name_plural = _('Politicial Experience'), _('Politicial Experience')



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


