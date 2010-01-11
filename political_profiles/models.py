# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from tagging.fields import TagField
from functions import cal_work_experience_days, cal_political_experience_days
from datetime import date

GENDERS = [
        ('Male',_('Male')),
        ('Female', _('Female')),
        ]
PETS = [
        ('Dog',_('Dog')),
        ('Cat', _('Cat')),
        ('Rabbit', _('Rabbit')),
        ('Horse', _('Horse')),
        ('Other', _('Other')),
        ]
HOBBIES = [
        ('Footabll',_('Football')),
        ('Golf', _('Golf')),
        ('Computer Games', _('Computer Games')),
        ('Other', _('Other')),
        ]
CLUBS  = [
        ('1',_('1')),
        ('2', _('2')),
        ('Other', _('Other')),
        ]
SPORT  = [
        ('Golf',_('Golf')),
        ('Football', _('Football')),
        ('Darts', _('Darts')),
        ('Horse Racing', _('Horse Racing')),
        ('Other', _('Other')),
        ]
MEDIA  = [
        ('NOS1',_('NOS1')),
        ('NOS2', _('NOS2')),
        ('NOS3',_('NOS3')),
        ('CNN', _('CNN')),
        ('BBC',_('BBC')),
        ('VERONICA', _('VERONICA')),
        ('NOS1',_('NOS1')),
        ('NOS1', _('NOS1')),
        ('Other', _('Other')),
        ]
CHARITY = [
        ('Serious Request',_('Serious Request')),
        ('Red Cross', _('Red Cross')),
        ('Red Cross', _('Red Cross')),
        ('Red Cross', _('Red Cross')),
        ('Red Cross', _('Red Cross')),
        ('Red Cross', _('Red Cross')),
        ('Other', _('Other')),
        ]
TRANSPORT  = [
        ('Train',_('Train')),
        ('Tram',_('Tram')),
        ('Bicycle',_('Bicycle')),
        ('Motorbike',_('Motorbike')),
        ('Car',_('Car')),
        ('Other', _('Other')),
        ]
NEWSPAPER  = [
        ('News1',_('News1')),
        ('News1',_('News1')),
        ('News1',_('News1')),
        ('News1',_('News1')),
        ('News1',_('News1')),
        ('News1',_('News1')),
        ('Other', _('Other')),
        ]
DIET  = [
        ('Omnivore',_('Nee')),
        ('vegetarian', _(u'Ja, ik ben vegetariër')),
        ('Vegan', _('Ja, ik ben veganist')),
        ('Other', _('Other')),
        ]
CHURCH = [
        ('Roman Catholic',_('Rooms Katholiek')),
        ('PKN',_('PKN')),
        ('Other Protestant',_('Anders Protestant')),
        ('Muslim',_('Moslim')),
        ('Jew',_('Joods')),
        ('Eastern Religion',_(u'Oosterse godsdienst (Boeddhisme,Hindoeïsme)')),
        ('Other',_('Anders')),
        ('No religion', _('Geen geloofsgemeenschap')),
        ]
LIFE_STANCE  = [
        ('Religious',_('Aanhanger van een religie')),
        ('There is something there but I do not know what', _('Er bestaat wel iets, maar ik weet niet wat')),
        ('Atheist', _('Atheist')),
        ('Humanist', _('Humanist')),
        ]
        
MARITAL_STATUS = [
        ('Married',_('Married')),
		('Civil Partnership', _('Geregistreerd partnerschap')),
		('Committed relationship', _('Vaste relatie / samenwonend')),
        ('Single', _('Single')),
        ('Other', _('Other')),
        ]
MOTIVATION = [
        ('A Better World',_('A Better World')),
        ('A stronger and better Netherlands', _('A stronger and better Netherlands')),
        ('A stronger and better Europe', _('A stronger and better Europe')),
        ('A powerful party', _('A powerful party')),
        ('Personal development', _('Personal development')),
        ('No motivation', _('No motivation')),

        ]

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
    motivation      = models.CharField(_('Motivation'), max_length=45, choices=MOTIVATION, blank=True, null=True)

    marital_status  = models.CharField(_('Marital Status'), max_length=25, choices=MARITAL_STATUS, blank=True, null=True)
    num_children    = models.PositiveIntegerField(_('Number of Children'), max_length=3, null=True, blank=True)
    life_stance     = models.CharField(_('Life Stance'), max_length=25, choices=LIFE_STANCE, blank=True, null=True)
    church          = models.CharField(_('Church'), max_length=25, choices=CHURCH, blank=True, null=True)
    smoker          = models.BooleanField(_('Smoker'), default=False)
    diet            = models.CharField(_('Diet'), max_length=25, choices=DIET, blank=True, null=True)
    fav_news        = models.CharField(_('Favourite Newspaper'), max_length=25, choices=NEWSPAPER, blank=True, null=True)
    transport       = models.CharField(_('What is your regular method of transport'), max_length=25, choices=TRANSPORT, blank=True, null=True)
    charity         = models.CharField(_('What charity do you care for most?'), max_length=35, choices=CHARITY, blank=True, null=True)
    fav_media       = models.CharField(_('What is your favourite media chanel?'), max_length=25, choices=MEDIA, blank=True, null=True)
    fav_sport       = models.CharField(_('What is your favourite sport?'), max_length=25, choices=SPORT, blank=True, null=True)
    hobby           = models.CharField(_('What is your hobby'), max_length=25, choices=HOBBIES, blank=True, null=True)
    fav_club        = models.CharField(_('What is your favourite club'), max_length=25, choices=CLUBS, blank=True, null=True)
    fav_pet         = models.CharField(_('What is your favourite pet'), max_length=25, choices=PETS, blank=True, null=True)
    political_experience_days      = models.PositiveIntegerField(_('Days of political experience'), max_length=10, null=True, blank=True, editable=False)
    work_experience_days           = models.PositiveIntegerField(_('Days of work experience'), max_length=10, null=True, blank=True, editable=False)

    def profile_incomplete(self):
        return not self.education.all() or not self.work.all() or not self.political.all() or \
            not (self.goals.all() or self.profile.appearances.all() or self.links.all())

    def election_party_instances(self):
        "Returns the election_party_instance objects of the candidate"
        # Currently there is only one but this needs to be modified at a later
        # date for when there are past elections
        candidicies = self.user.elections.all()
        election_party_instances = []
        for candidacy in candidicies:
            election_party_instances.append(candidacy.election_party_instance)

        return election_party_instances

    def region(self):
        "returns the region the politician is currently in"
        candidacy = self.user.elections.all()
        return candidacy[0].election_party_instance.election_instance.council.region

    def party(self):
        "Returns the party  of the candidate"
        # Currently there is only one but this needs to be modified at a later
        # date for when there are past elections and so more partys
        candidacy = self.user.elections.all()
        return candidacy[0].election_party_instance.party

    def position(self):
        "Returns the position of the candidate on the party's list"
        candidacy = self.user.elections.all()
        return candidacy[0].position

    def age(self):
        if self.dateofbirth:
            d = date.today()
            bday = self.dateofbirth
            return (d.year - bday.year) - int((d.month, d.day) < (bday.month, bday.day))
        return

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
    organisation    = models.CharField(_('Organisation Name'), max_length=255)
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
        ordering = ('datetime',)

class WorkExperience(models.Model):
    """
        A class to hold work experience
    """
    company_name    = models.CharField(_('Company Name'), max_length=255)
    sector          = models.ForeignKey(WorkExperienceSector, verbose_name=_('Sector'), null=True, blank=True)
    position        = models.CharField(_('Position'), max_length=255)
    startdate       = models.DateField(_('Start Date'), null=True, blank=True)
    enddate         = models.DateField(_('End Date'), null=True, blank=True)
    description     = models.TextField(_('Description'), blank=True, null=True)
    politician  = models.ForeignKey(PoliticianProfile, verbose_name=_('Politician'), related_name='work')

    class Meta:
        verbose_name, verbose_name_plural = _('Work experience'), _('Work experience')
        ordering = ('startdate', 'enddate')

class Education(models.Model):
    """
        A period of education
    """
    institute   = models.CharField(_('Institute Name'), max_length=255)
    level       = models.ForeignKey(EducationLevel, verbose_name=_('Level'), null=True, blank=True)
    field       = models.CharField(_('Field'), max_length=255)
    startdate   = models.DateField(_('Start Date'), null=True, blank=True)
    enddate     = models.DateField(_('End Date'), null=True, blank=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    politician  = models.ForeignKey(PoliticianProfile, verbose_name=_('Politician'), related_name='education')

    class Meta:
        verbose_name, verbose_name_plural = _('Education'), _('Education')
        ordering = ('startdate', 'enddate')

class PoliticalExperience(models.Model):
    """
        Experience in the political world
    """
    organisation    = models.CharField(_('Organisation'), max_length=255)
    type  = models.ForeignKey(PoliticalExperienceType, verbose_name=_('Type'), null=True, blank=True)
    position        = models.CharField(_('Position'), max_length=255)
    startdate       = models.DateField(_('Start Date'), null=True, blank=True)
    enddate         = models.DateField(_('End Date'), null=True, blank=True)
    description     = models.TextField(_('Description'), blank=True, null=True)
    politician      = models.ForeignKey(PoliticianProfile, verbose_name=_('Politician'), related_name='political')
    #tags            = TagField()
    class Meta:
        verbose_name, verbose_name_plural = _('Politicial Experience'), _('Politicial Experience')
        ordering = ('startdate', 'enddate')

class PoliticalGoal(models.Model):
    """
        A goal of a politician
    """
    goal            = models.CharField(_('Goal'), max_length=100, help_text=_('A short statement defining your goal'))
    politician      = models.ForeignKey(PoliticianProfile, verbose_name=_('Politician'), related_name='goals')
    
    class Meta:
        verbose_name, verbose_name_plural = _('Goal'), _('Goals')
        ordering = ('goal', )
    
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


post_save.connect(cal_political_experience_days, sender=PoliticalExperience)
post_delete.connect(cal_political_experience_days, sender=PoliticalExperience)
post_save.connect(cal_work_experience_days, sender=WorkExperience)
post_delete.connect(cal_work_experience_days, sender=WorkExperience)