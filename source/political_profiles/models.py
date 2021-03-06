# -*- coding: utf-8 -*-

import datetime
from datetime import date

from django.db import models
from django.db.models import Sum, Count
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from political_profiles.functions import cal_work_experience_days, cal_political_experience_days
from elections.functions import get_popularity


from utils.netutils import check_unique_visitor


GENDERS = [
        ('Male',_('Male')),
        ('Female', _('Female')),
        ]
PETS = [
        ('DOG','Hond'),
        ('CAT', 'Kat'),
        ('RABBIT', 'Konijn'),
        ('RODENT', 'Knaagdier'),
        ('REPTILE', 'Reptiel'),
        ('BIRD', 'Vogel'),
        ('FISH', 'Vis'),
        ]
MEDIA  = [
        ('NED1', 'Ned 1'),
        ('NED2', 'Ned 2'),
        ('NED3', 'Ned 3'),
        ('RTL4', 'RTL 4'),
        ('RTL5', 'RTL 5'),
        ('RTL7', 'RTL 7'),
        ('SBS6', 'SBS 6'),
        ('NET5', 'Net 5'),
        ('VERONICA', 'Veronica'),
        ('TMF', 'TMF'),
        ('MTV', 'MTV'),
        ('COMEDYCENTRAL', 'Comedycentral'),
        ('DISCOVERYCHANNEL', 'Discovery Channel'),
        ('NATIONALGEOGRAPHIC', 'National Geographic'),
        ('BUITENLANDSEZENDER', 'Buitenlandse zender'),
        # ('RTV_NOORD', 'RTV Noord'),
        #         ('RTV_NOORD_HOLLAND', 'RTV Noord Holland'),
        #         ('RTV_OOST', 'RTV Oost'),
        #         ('RTV_WEST', 'RTV West'),
        #         ('RTV_EEMLAND', 'RTV Eemland'),
        #         ('RTV_UTRECHT', 'RTV Utrecht'),
        #         ('TV_ENSCHEDE', 'TV Enschede'),
        #         ('TV_AMSTERDAM', 'TV Amsterdam'),
        #         ('STADSOMROEP_DENHAAG', 'Stadsomroep Den Haag'),
        #         ('AT5', 'AT5'),
        #         ('OOGTV', 'Oog TV'),
        #         ('OMROEP_AMERSFOORT', 'Omroep Amersfoort'),
        #         ('OMROEP_BRABANT', 'Omroep Brabant'),
        ]
TRANSPORT  = [
        ('WALKING','Lopen'),
        ('BICYCLE','Fiets'),
        ('OV','Openbaar vervoer'),
        ('SCOOTER','Brommer/Scooter'),
        ('MOTORBIKE','Motor'),
        ('CAR','Auto'),
        ('CARPOOL','Carpool'),
        ]
NEWSPAPER  = [
            ('TELEGRAAF', u'De Telegraaf'),
            ('VOLKSKRANT', u'De Volkskrant'),
            ('AD', u'Algemeen Dagblad'),
            ('TROUW', u'Trouw'),
            ('PAROOL', u'Het Parool'),
            ('FINANCIELE_DAGBLAD', u'Het Financiële Dagblad'),
            ('REFORMATISCH_DAGBLAD', u'Reformatisch Dagblad'),
            ('NEDERLANDS_DAGBLAD', u'Nederlands Dagblad'),
            ('NRC', u'NRC Handelsblad'),
            ('PERS', u'De Pers'),
            ('SPITS', u'Sp!ts'),
            ('METRO', u'Metro'),
            ('NRCNEXT', u'nrc.next'),
            # ('AD_DENHAAG', u'AD Den Haag'),
            #             ('TWENTSE_COURANT_TUBANTIA', u'Twentse Courant Tubantia'),
            #             ('NOORDHOLLANDS_DAGBLAD', u'Noordhollands Dagblad'),
            #             ('AD_AMSTERDAM', u'AD Amsterdam'),
            #             ('GRONINGEN_COURANT', u'Groninger Courant'),
            #             ('DAGBLAD_VH_NOORDEN', u'Dagblad van het Noorden'),
            #             ('BRABANTS_DAGBLAD', u'Brabants Dagblad'),
            #             ('GOOI__EN_EEMLANDER', u'Gooi- en Eemlander'),
            #('AD_AMSERSFOORT', u'AD Amersfoortse Courant'),
            ('BUITENLANDSE_KRANT', 'Buitenlandse krant'),
            ('ANDERS', u'Anders'),
        ]
DIET  = [
        ('ALL', u'Vleeseter'),
        ('VEG', u'Vegetariër'),
        ]
SMOKER = [
    ('NO', u'Nee'),
    ('YES', u'Ja'),
]
RELIGION = [
        ('NONE', 'Geen'),
        ('RKK', 'Rooms-Katholieke kerk'),
        ('PROTESTANT', 'Protestants'),
        ('OTHER_CHRISTIAN', 'Overige Christelijke kerken'),
        ('ISLAM', 'Islam'),
        ('JEWISH', 'Jodendom'),
        ('HINDUISM', u'Hindoeïsme'),
        ('BUDDHISM', 'Boeddhisme'),
        ('ATEIST', u'Atheïsme'),
        ('OTHER', 'Anders'),
        ]

CHARITIES = [
        ('AIDS_FONDS','Aids Fonds'),
        ('AMNESTY_INTERNATIONAL','Amnesty International'),
        ('ARTSEN_ZONDER_GRENZEN','Artsen zonder Grenzen'),
        ('ASTMA_FONDS','Astma Fonds'),
        ('BONT_VOOR_DIEREN','Bont voor Dieren'),
        ('CLINICLOWNS','CliniClowns'),
        ('DE_LEPRASTICHTING','De Leprastichting'),
        ('DIABETES_FONDS','Diabetes Fonds'),
        ('DIERENBESCHERMING','Dierenbescherming'),
        ('DOE_EEN_WENS_STICHTING','Doe Een Wens Stichting'),
        ('FAIRFOOD','Fairfood'),
        ('GREENPEACE','Greenpeace'),
        ('HARTSTICHTING','Hartstichting'),
        ('HET_NEDERLANDSE_RODE_KRUIS','Het Nederlandse Rode Kruis'),
        ('HUMANITAS','Humanitas'),
        ('IKV_PAX_CHRISTI','IKV Pax Christi'),
        ('JANTJE_BETON','Jantje Beton'),
        ('KRAJICEK_FOUNDATION','Krajicek Foundation'),
        ('KWF_KANKERBESTRIJDING','KWF Kankerbestrijding'),
        ('MAX_HAVELAAR','Max Havelaar'),
        ('NATUURMONUMENTEN','Natuurmonumenten'),
        ('OXFAM_NOVIB','Oxfam Novib'),
        ('REUMAFONDS','Reumafonds'),
        ('SAVE_THE_CHILDREN','Save the Children'),
        ('STICHTING_AAP','Stichting AAP'),
        ('STICHTING_DOEN','Stichting Doen (postcode loterij)'),
        ('STICHTING_WAR_CHILD','Stichting War Child'),
        ('UNICEF','Unicef'),
        ('WERELD_NATUUR_FONDS','Wereld Natuur Fonds'),
        ]
MARITAL_STATUS = [
        ('Married','Getrouwd'),
        ('Engaged', 'Verloofd'),
        ('Together', 'Samenwonend'),
        ('LAT', 'LAT relatie'),
        ('Single', 'Alleenstaand'),
        ]

PROVINCES = [
    ('Drenthe', 'Drenthe'),
    ('Overijssel', 'Overijssel'),
    ('Flevoland', 'Flevoland'),
    ('Friesland', 'Friesland'),
    ('Gelderland', 'Gelderland'),
    ('Groningen', 'Groningen'),
    ('Limburg', 'Limburg'),
    ('Noord-Brabant', 'Noord-Brabant'),
    ('Noord-Holland', 'Noord-Holland'),
    ('Utrecht', 'Utrecht'),
    ('Zeeland', 'Zeeland'),
    ('Zuid-Holland', 'Zuid-Holland'),
]

PARTIES = [
    ('VVD', 'Volkspartij voor Vrijheid en Democratie (VVD)'),
    ('PVDA', 'Partij van de Arbeid (PvdA)'),
    ('PVV', 'Partij voor de Vrijheid (PVV)'),
    ('CDA', 'Christen Democratisch Appèl (CDA)'),
    ('SP', 'Socialistische Partij (SP)'),
    ('D66', 'Democraten 66 (D66)'),
    ('GL', 'GroenLinks'),
    ('CU', 'ChristenUnie'),
    ('SGP', 'Staatkundig Gereformeerde Partij'),
    ('PVDD', 'Partij voor de Dieren'),
    ('PIRATENPARTIJ', 'Piratenpartij', ''),
    ('MENS', 'Partij voor Mens en Spirit (MenS)'),
    ('NL', 'Nederland Lokaal'),
    ('LB', 'Libertarische Partij'),
    ('DPK', 'Democratisch Politiek Keerpunt (DPK)'),
    ('50Plus','50Plus'),
    ('LIBDEM','Liberaal Democratische Partij (LibDem)'),
    ('AEP','Anti Europa Partij'),
    ('SOPN','Soeverein Onafhankelijke Pioniers Nederland (SOPN)'),
    ('PVDT','Partij van de Toekomst (PvdT)'),
    ('Politieke Partij NXD','Politieke Partij NXD'),
]

EXPERTISE = [
    ('BZK', 'Burger en bestuur'),
    ('FIN', 'Economie en financiën'),
    ('SOC', 'Sociale zaken en werkgelegenheid'),
    ('OW', 'Onderwijs, cultuur en wetenschap'),
    ('IM', 'Integratie, immigratie en inburgering'),
    ('RO', 'Volkshuisvesting en ruimtelijke ordening'),
    ('VERK', 'Verkeer en vervoer'),
    ('LW', 'Landbouw, milieu en natuur'),
    ('VWS', 'Volksgezondheid, welzijn en sport'),
    ('JUS', 'Openbare orde en veiligheid'),
    ('BUIT', 'Buitenlandse zaken, ontwikkelingssamenwerking en defensie'),
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

    terms_and_conditions    = models.BooleanField(_('I agree to the terms and conditions'), blank=True, default=False)

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
    favorites = models.ManyToManyField('PoliticianProfile', verbose_name = _('Favorites'), related_name = 'fans')
    phone = models.CharField(_('Phone number'), max_length=50, blank=True, null=True)
    send_text = models.BooleanField(_('Send me a text'), default=True, help_text=_('Disable this if you don\'t want a textmessage'))

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
    age             = models.PositiveIntegerField(_('Age'), blank=True, null=True)
    picture         = models.ImageField(_('Picture'), upload_to='media/politician', null=True, blank=True)
    movie           = models.URLField(_('Movie'), max_length=255, verify_exists=True, blank=True, null=True,
                                      help_text=_('Link to YouTube video'))

    introduction    = models.TextField(_('Introduction'), blank=True, null=True)

    marital_status  = models.CharField(_('Marital Status'), max_length=25, choices=MARITAL_STATUS, blank=True, null=True)
    num_children    = models.PositiveIntegerField(_('Number of Children'), max_length=3, null=True, blank=True)
    religion        = models.CharField(_('Religion'), max_length=255, choices=RELIGION, blank=True, null=True)
    religious_group = models.CharField(_('Religious group'), max_length=255, blank=True, null=True)
    smoker          = models.CharField(_('Smoker'), choices=SMOKER, max_length=255, blank=True, null=True)
    province        = models.CharField(_('Province'), choices=PROVINCES, max_length=255, blank=True, null=True)
    diet            = models.CharField(_('Diet'), max_length=25, choices=DIET, blank=True, null=True)
    fav_news        = models.CharField(_('Favourite Newspaper'), max_length=25, choices=NEWSPAPER, blank=True, null=True)
    transport       = models.CharField(_('What is your regular method of transport'), max_length=25, choices=TRANSPORT, blank=True, null=True)
    charity         = models.CharField(_('What charity do you care for most?'), max_length=255, blank=True, null=True, choices=CHARITIES)
    fav_media       = models.CharField(_('What is your favourite media chanel?'), max_length=25, choices=MEDIA, blank=True, null=True)
    fav_sport       = models.CharField(_('What is your favourite sport?'), max_length=255, blank=True, null=True)
    hobby           = models.CharField(_('What is your hobby'), max_length=255, blank=True, null=True)
    fav_club        = models.CharField(_('What is your favourite sport club'), max_length=255, blank=True, null=True)
    fav_pet         = models.CharField(_('What is your favourite pet'), max_length=255, choices=PETS, blank=True, null=True)
    political_experience_days      = models.PositiveIntegerField(_('Days of political experience'), max_length=10, null=True, blank=True, editable=False)
    work_experience_days           = models.PositiveIntegerField(_('Days of work experience'), max_length=10, null=True, blank=True, editable=False)

    hns_dev                 = models.BooleanField(_('I agree to my information being added to HNS.Dev'), blank=True, default=False)
    science                 = models.BooleanField(_('I agree to my information being used for scientific purposes'), blank=True, default=False)

    class Meta:
        verbose_name, verbose_name_plural = _('Politician Profile'), _('Politician Profiles')

    @property
    def popularity(self):
        if not hasattr(self, '_popularity'):
            candidacy_id = self.get_first_candidacy().id
            canpop, partypop = get_popularity(self.election_party().election_instance_id)
            self._popularity = int(canpop.get(candidacy_id, 0))
        if self._popularity < 20:
            return 20
        return self._popularity

    def get_first_candidacy(self):
	# JB 20120826 We now pick the candidacy with the highest id; this should be the most recent one
        candidacy = self.user.elections.order_by('-id').all()
        if candidacy.count() != 0:
            return candidacy[0]
        return None

    def profile_incomplete(self):
        return not self.marital_status

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
	# JB 20120826 We now pick the candidacy with the highest id; this should be the most recent one
        candidacy = self.user.elections.all().order_by('-id')
        if candidacy.count() != 0:
            return candidacy[0].election_party_instance.election_instance.council.region
        return None

    def party(self):
        "Returns the party  of the candidate"
        # Currently there is only one but this needs to be modified at a later
        # date for when there are past elections and so more partys
	# JB 20120826 We now pick the candidacy with the highest id; this should be the most recent one
        candidacy = self.user.elections.select_related('election_party_instance__party').order_by('-id')
        if candidacy.count() != 0:
            return candidacy[0].election_party_instance.party
        return None

    def election_party(self):
        """ Returns election party wrapper. """
	# JB 20120826 We now pick the candidacy with the highest id; this should be the most recent one
        candidacy = self.user.elections.all().select_related('election_party_instance__party').order_by('-id')
        if candidacy.count() != 0:
            return candidacy[0].election_party_instance
        return None

    def position(self):
        "Returns the position of the candidate on the party's list"
        # JB 20120908 We now pick the election with the highest id; this should be the most recent one
        candidacy = self.user.elections.order_by('-id').all()
        if candidacy.count() != 0:
            return candidacy[0].position
        return None

    def _calculate_age(self):
        if self.dateofbirth:
            d = date.today()
            bday = self.dateofbirth
            self.age = (d.year - bday.year) - int((d.month, d.day) < (bday.month, bday.day))
        else:
            self.age = None

    def __unicode__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self._calculate_age()
        super(PoliticianProfile, self).save(*args, **kwargs)




class ChanceryProfile(Profile):
    """
        A profile for a chancery
    """
    type = 'council_admin'

    gender      = models.CharField(_('Gender'), max_length=25, choices=GENDERS, default='Male')
    telephone   = models.CharField(_('Phone Number'), max_length=255, null=True, blank=True)
    workingdays = models.CharField(_('Working Days'), max_length=255, null=True, blank=True)
    street      = models.CharField(_('Street'), max_length=40, null=True, blank=True)
    house_num   = models.CharField(_('House Number'), max_length=5, null=True, blank=True)
    postcode    = models.CharField(_('Postcode'), max_length=7, null=True, blank=True,
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
    #Expenses   Reference



class ContactProfile(Profile):
    """
        A profile for a contact (for a party)
    """
    type = 'party_admin'

    gender = models.CharField(_('Gender'), max_length=25, choices=GENDERS, default='Male')
    telephone   = models.CharField(_('Phone Number'), max_length=255, null=True, blank=True)
    workingdays = models.CharField(_('Working Days'), max_length=255, null=True, blank=True)
    street      = models.CharField(_('Street'), max_length=40, null=True, blank=True)
    house_num   = models.CharField(_('House Number'), max_length=5, null=True, blank=True)
    postcode    = models.CharField(_('Postcode'), max_length=7, null=True, blank=True,
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
    #Expenses   Reference


# Profile Attribute Classes

class Link(models.Model):
    """
        A class to hold links the politician has
    """
    name        = models.CharField(_('Name'), max_length=255)
    url         = models.URLField(_('URL'), verify_exists=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    politician  = models.ForeignKey(PoliticianProfile, related_name='links', verbose_name=_('Politician') )

    class Meta:
        verbose_name, verbose_name_plural = _('Link'), _('Links')


class Connection(models.Model):
    """
        A class to hold links the politician has
    """
    type        = models.ForeignKey(ConnectionType, verbose_name=_('Type'), null=True, blank=True)
    url         = models.URLField(_('URL'), verify_exists=True)
    description = models.TextField(_('Description'), null=True, blank=True)
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
    location    = models.CharField(_('Location'), max_length=255)
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
    goal            = models.CharField(_('Goal'), max_length=100, help_text=_('Vul hier uw doel in.'))
    politician      = models.ForeignKey(PoliticianProfile, verbose_name=_('Politician'), related_name='goals')

    class Meta:
        verbose_name, verbose_name_plural = _('Goal'), _('Goals')
        ordering = ('goal', )

    @property
    def ranking(self):
        if not hasattr(self, '_ranking_cache'):
            self._ranking_cache = self.rankings.aggregate(Sum('ranking'), Count('ranking'))
        return self._ranking_cache['ranking__sum']

    @property
    def count_rankings(self):
        if not hasattr(self, '_ranking_cache'):
            self._ranking_cache = self.rankings.aggregate(Sum('ranking'), Count('ranking'))
        return self._ranking_cache['ranking__count']

class GoalRanking(models.Model):
    """
        A ranking of a goal. Either +1 or -1
    """
    ranking = models.SmallIntegerField(_('Ranking'))
    goal    = models.ForeignKey(PoliticalGoal, verbose_name=_('Goal'), related_name='rankings')
    user    = models.ForeignKey(User, verbose_name=_('User', related_name='rankings'))

    class Meta:
        verbose_name, verbose_name_plural = _('Ranking'), _('Rankings')
        ordering = ('ranking',)
        unique_together = (('goal','user'),)



class UserStatistics(models.Model):
    """
        One-to-One model used to store simple statistics (counters).

        Profile views are accumulated in a simple metric:

                           STAT_PROVIEW_INTERVAL
            tviews = ------------------------------------- * views
                     STAT_PROVIEW_INTERVAL + time_elapsed

        Where views is roughly number of views the profile was viewed,
        STAT_PROVIEW_INTERVAL is the time interval within which a single view
        lives and the time_elapsed is (now() - last_update_time). The tviews
        fades out as time_elapsed increases.

        With each view the "views" is updated as:

                          STAT_PROVIEW_INTERVAL
            views = ------------------------------------- * (views + 1)
                    STAT_PROVIEW_INTERVAL + time_elapsed

        Settings:
            STAT_PROVIEW_INTERVAL -- datetime.timedelta defines the time
                to live for each single view, when such interval is elapsed, the
                whole rating is 1/2, 1/3...


        Note: tviews can never be 0 if views > 0, so rating will fade out slowly,
        but will never be 0 and will increase fast as profile hits increase.
    """
    user            = models.OneToOneField(User, related_name="stats", unique=True, null = True, verbose_name=_('User'))

    # doesn't tell us how many times it was viewed, but tells instead how "hot"
    # the profile is. cheap and easy.
    profile_hits    = models.FloatField(_('Roughly number of views'), null = False, blank = False, default = 1)
    profile_hits_up = models.DateTimeField(_('View stats last update'), null = False, blank = False, default = datetime.datetime.now)

    # cached variables
    view_interval = settings.STAT_PROVIEW_INTERVAL if getattr(settings, 'STAT_PROVIEW_INTERVAL', None) else datetime.timedelta(days = 30)


    def update_profile_views(self, request):
        """ Updates profile rate """
        if check_unique_visitor(request, 'update_profile_view_rate'):
            self.profile_hits = self.get_profile_views(1)
            self.profile_hits_up = datetime.datetime.now()
            self.save()


    def get_profile_views(self, shift = 0):
        """ Returns current profile view rate. """
        winsec = 24*60*60 * self.view_interval.days + self.view_interval.seconds
        dl = (datetime.datetime.now() - self.profile_hits_up)
        dl = 24*60*60 * dl.days + dl.seconds
        # current rate with time penalty
        return (float(winsec) / (winsec + dl)) * (self.profile_hits + shift)



def user_statistics(u):
    """ Function creates UserStatistics on-the-fly on first access. """
    try:
        return u.stats
    except:
        UserStatistics(user = u).save()
        return u.stats


# Lazy create
User.statistics = property(user_statistics)



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

def full_name(self):
    if self.profile is None:
        return self.username
    return self.profile.full_name()
User.get_full_name = full_name

post_save.connect(cal_political_experience_days, sender=PoliticalExperience)
post_delete.connect(cal_political_experience_days, sender=PoliticalExperience)
post_save.connect(cal_work_experience_days, sender=WorkExperience)
post_delete.connect(cal_work_experience_days, sender=WorkExperience)
