from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from tagging.fields import TagField

GENDERS = (
        ('Male',_('Male')),
        ('Female', _('Female')),
        )



class ConnectionType(models.Model):
    """
            Type of connection.
    """
    type      = models.CharField(_('Type'), max_length=255)

    def __unicode__(self):
        return self.type

class WorkExperienceSector(models.Model):
    """
            Different Sectors that people could have worked in.
    """
    sector      = models.CharField(_('Sector'), max_length=255)

    def __unicode__(self):
        return self.sector

class PoliticalExperienceType(models.Model):
    """
            Different Types of Political Experience Areas.
    """
    type      = models.CharField(_('Type'), max_length=255)

    def __unicode__(self):
        return self.type

class EducationLevel(models.Model):
    """
            Different Levels that people could have been educated at.
    """

    level      = models.CharField(_('Level'), max_length=255)
    def __unicode__(self):
        return self.level
    
# Profiles
class Profile(models.Model):
    """
    A abstract profile, put general shared profile information in here
    """
    user = models.OneToOneField(User, related_name="%(class)s", unique=True, verbose_name=_('User'))
    first_name = models.CharField(_('First name'), blank=True, max_length=80)
    middle_name = models.CharField(_('Middle name'), null=True, blank=True, max_length=80)
    last_name = models.CharField(_('Last name'), blank=True, max_length=80)

    class Meta:
        abstract = True
        verbose_name, verbose_name_plural = _('Profile'), _('Profiles')
    
    def full_name(self):
        return ' '.join(filter(lambda x: x, (self.first_name, self.middle_name, self.last_name)))
        
        
    def save(self, *args, **kwargs):
        """
            Update the user's first_name and last_name as needed.
        """
        super(Profile, self).save(*args, **kwargs)
        if self.user.get_full_name() != self.full_name():
            self.user.first_name = self.first_name
            self.user.last_name = ' '.join(filter(lambda x: x, (self.middle_name, self.last_name)))
            self.user.save()
    
class VisitorProfile(Profile):
    """
        A profile for visitors of the website when they "register"
    """
    type = 'visitor'
    
    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name, verbose_name_plural = _('Visitor Profile'), _('Visitor Profiles')
            
    
class PoliticianProfile(Profile):
    """
        A profile for a politician
    """
    type = 'candidate'
    
    initials        = models.CharField(_('Initials'), max_length=15, blank=True, null=True)
    gender          = models.CharField(_('Gender'), max_length=25,choices=GENDERS, default='Male',
                                       help_text=_("Please choose your gender."))
    dateofbirth     = models.DateField(_('Date Of Birth'), null=True, blank=True)
    picture         = models.ImageField(_('Picture'), upload_to='media/politician', null=True, blank=True)
    movie           = models.URLField(_('Movie'), max_length=255, verify_exists=True, blank=True, null=True,
                                      help_text=_('Link to YouTube video'))
                                      
    introduction    = models.TextField(_('Introduction'), blank=True, null=True)
    motivation    = models.TextField(_('Motivation'), blank=True, null=True)
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
    type = 'council_admin'
    
    gender      = models.CharField(_('Gender'), max_length=25, choices=GENDERS, default='Male')
    telephone	= models.CharField(_('Phone Number'), max_length=255, null=True, blank=True)
    workingdays = models.CharField(_('Working Days'), max_length=255, null=True, blank=True)
    street      = models.CharField(_('Street'), max_length=40, null=True, blank=True)
    house_num   = models.CharField(_('House Number'), max_length=5, null=True, blank=True)
    postcode  	= models.CharField(_('Postcode'), max_length=7, null=True, blank=True,
                                   help_text=_("Postcode (e.g. 9725 EK or 9211BV)"))
    town        = models.CharField(_('Town/City'), max_length=30, null=True, blank=True)
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
    type = 'party_admin'
    
    gender = models.CharField(_('Gender'), max_length=25, choices=GENDERS, default='Male')
    telephone	= models.CharField(_('Phone Number'), max_length=255, null=True, blank=True)
    workingdays = models.CharField(_('Working Days'), max_length=255, null=True, blank=True)
    street      = models.CharField(_('Street'), max_length=40, null=True, blank=True)
    house_num   = models.CharField(_('House Number'), max_length=5, null=True, blank=True)
    postcode  	= models.CharField(_('Postcode'), max_length=7, null=True, blank=True,
                                   help_text=_("Postcode (e.g. 9725 EK or 9211BV)"))
    town        = models.CharField(_('Town/City'), max_length=30, null=True, blank=True)
    website     = models.URLField(_('Councils Website'), max_length=255, verify_exists=True, null=True, blank=True)
    picture     = models.ImageField(_('Picture'), upload_to='media/contact', null=True, blank=True)
    description = models.CharField(_('Description'), max_length=255, null=True, blank=True,
                                   help_text=_("A short description of yourself"))

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name, verbose_name_plural = _('Contact Profile'), _('Contact Profiles')
    #Expenses	Reference


# Profile Attribute Classes

class Link(models.Model):
    """
        A class to hold links the politician has
    """
    name        = models.CharField(_('Name'), max_length=255)
    url         = models.URLField(_('URL'), verify_exists=True)
    description	= models.TextField(_('Description'), blank=True, null=True)
    politician  = models.ForeignKey(PoliticianProfile, related_name='links', verbose_name=_('Politician') )

    class Meta:
        verbose_name, verbose_name_plural = _('Link'), _('Links')


class Connection(models.Model):
    """
        A class to hold links the politician has
    """
    type        = models.ForeignKey(ConnectionType, verbose_name=_('Type'), null=True, blank=True)
    url         = models.URLField(_('URL'), verify_exists=True)
    description	= models.TextField(_('Description'), null=True, blank=True)
    politician  = models.ForeignKey(PoliticianProfile, related_name='connections', verbose_name=_('Politician') )

    class Meta:
        verbose_name, verbose_name_plural = _('Connection'), _('Connections')

class Interest(models.Model):
    """
        A class to hold an interest of the politician
    """
    organization    = models.CharField(_('Organisation Name'), max_length=255)
    url             = models.URLField(_('URL'), verify_exists=True)
    description     = models.TextField(_('Description'), null=True, blank=True)
    politician  = models.ForeignKey(PoliticianProfile, verbose_name=_('Politician'), related_name='interests')

    class Meta:
        verbose_name, verbose_name_plural = _('Intrest'), _('Intrests')

class Appearance(models.Model):
    """
        A class to hold an appearance (where they attended somthing) of the politician
    """
    name        = models.CharField(_('Affiliated Organisation Name'), max_length=255)
    location	= models.CharField(_('Location'), max_length=255)
    url         = models.URLField(_('URL'), verify_exists=True, null=True, blank=True)
    description = models.TextField(_('Description'), null=True, blank=True)
    datetime    = models.DateTimeField(_('Date and Time of Appearance'), null=True, blank=True)
    politician  = models.ForeignKey(PoliticianProfile, verbose_name=_('Politician'), related_name='appearances')

    class Meta:
        verbose_name, verbose_name_plural = _('Politician Appearance'), _('Politician Appearances')

class WorkExperience(models.Model):
    """
        A class to hold work experience
    """
    company_name 	= models.CharField(_('Company Name'), max_length=255)
    sector          = models.ForeignKey(WorkExperienceSector, verbose_name=_('sector'), null=True, blank=True)
    position        = models.CharField(_('Position'), max_length=255)
    startdate       = models.DateField(_('Start Date'), null=True, blank=True)
    enddate         = models.DateField(_('End Date'), null=True, blank=True)
    current         = models.BooleanField(_('Currently Employed'), default=False)
    description     = models.TextField(_('Description'), blank=True, null=True)
    politician  = models.ForeignKey(PoliticianProfile, verbose_name=_('Politician'), related_name='work')

    class Meta:
        verbose_name, verbose_name_plural = _('Work experience'), _('Work experience')

class Education(models.Model):
    """
        A period of education
    """
    institute   = models.CharField(_('Institute Name'), max_length=255)
    level       = models.ForeignKey(EducationLevel, verbose_name=_('level'), null=True, blank=True)
    field       = models.CharField(_('Field'), max_length=255)
    startdate   = models.DateField(_('Start Date'), null=True, blank=True)
    enddate     = models.DateField(_('End Date'), null=True, blank=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    politician  = models.ForeignKey(PoliticianProfile, verbose_name=_('Politician'), related_name='education')

    class Meta:
        verbose_name, verbose_name_plural = _('Education'), _('Education')

class PoliticalExperience(models.Model):
    """
        Experience in the political world
    """
    organisation    = models.CharField(_('Organisation'), max_length=255)
    type  = models.ForeignKey(PoliticalExperienceType, verbose_name=_('type'), null=True, blank=True)
    position        = models.CharField(_('Position'), max_length=255)
    startdate       = models.DateField(_('Start Date'), null=True, blank=True)
    enddate         = models.DateField(_('End Date'), null=True, blank=True)
    description     = models.TextField(_('Description'), blank=True, null=True)
    politician      = models.ForeignKey(PoliticianProfile, verbose_name=_('Politician'), related_name='political')
    #tags            = TagField()
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


