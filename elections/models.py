from django.db import models
from django.utils.translation import ugettext_lazy as _
from elections import settings

from django.contrib.auth.models import User


class Council(models.Model):
    """
    A council
    """
    name        = models.CharField(_('Name'), max_length=255)    
    region      = models.CharField(_('Region'), max_length=255) #Autocomplete other council regions
    level       = models.CharField(_('Level'), max_length=255) #Autocomplete other council levels
    chanceries  = models.ManyToManyField(User, limit_choices_to=settings.CHANCERY_LIMITATION,
                    verbose_name=_('Chanceries'))
    abbreviation= models.CharField(_('Abbreviated Name'), max_length=15)
    email       = models.EmailField(_('E-Mail'))
    street      = models.CharField(_('Street'), max_length=40)
    house_num   = models.CharField(_('House Number'), max_length=5)
    postcode  	= models.CharField(_('Postcode'), max_length=7, help_text=_("Postcode (e.g. 9725 EK or 9211BV)"))
    town        = models.CharField(_('Town/City'), max_length=30)
    seats       = models.PositiveIntegerField(_('Seats'), max_length=30, null=True, blank=True)
    website     = models.URLField(_('Councils Website'), max_length=255, verify_exists=True, null=True, blank=True)
    picture     = models.ImageField(_('Picture'), upload_to='media/council',
                    help_text=_("A picture that will be used when displaying council details."), null=True, blank=True)
    desciption  = models.CharField(_('Description'), max_length=255, help_text=_("A short description of the council"),
                null=True, blank=True)
    history     = models.CharField(_('History'), max_length=255 , help_text=_("A short history of the council"),
                    null=True, blank=True)

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name, verbose_name_plural = _('Council'), _('Councils')

class ElectionEvent(models.Model):
    """
    A election event
    e.g. European Predisent elections 2009, Municipality elections 2010
    """
    
    name            = models.CharField(_('Name'), max_length=255)
    parent_region   = models.CharField(_('Parent region'), max_length=255) #autocomplete other electionevent regions
    level           = models.CharField(_('Level'), max_length=255) #autocomplete other electionevent levels
    desciption  = models.CharField(_('Description'), max_length=255, null=True, blank=True)

    def __unicode(self):
        return self.name
    
    class Meta:
        verbose_name, verbose_name_plural = _('Election Event'), _('Election Events')

class ElectionInstance(models.Model):
    """
    A election instance for an election event
    e.g. Municipality Groningen (for Election Event Municipality elections 2010)
    """
    
    council         = models.ForeignKey(Council, verbose_name=_('Council'))
    election_event  = models.ForeignKey(ElectionEvent, verbose_name=_('Election Event'))
    parties         = models.ManyToManyField('Party', verbose_name=_('Parties'), through='ElectionInstanceParty')
    questions       = models.ManyToManyField('questions.Question', through='ElectionInstanceQuestion', verbose_name=_('Questions'), null=True, blank=True)
    name            = models.CharField(_('Name'), max_length=255)
    start_date      = models.DateTimeField(_('Start Date'))
    end_date        = models.DateTimeField(_('End Date'))
    website         = models.URLField(_('Elections Website'), max_length=255, verify_exists=True, null=True, blank=True)

    def __unicode__(self):
        return self.council
    class Meta:
        verbose_name, verbose_name_plural = _('Election Instance'), _('Election Instances')    
    
class ElectionInstanceQuestion(models.Model):
    """
        Links a election instance to a question
        Has a locked property to indicate that the question is only editable for the admin
    """
    election_instance   = models.ForeignKey(ElectionInstance, verbose_name=_('Election Instance'))
    question            = models.ForeignKey('questions.Question', verbose_name=_('Question'))
    
     #locked means it can only be edited by admins because it's used in multiple electioninstances
    locked              = models.BooleanField(_('Locked'), default=False)

    def __unicode__(self):
        return self.election_instance.council
    class Meta:
        verbose_name, verbose_name_plural = _('Election Instance Question'), _('Election Instance Questions')
    
class Party(models.Model):
    """
        A party within an election instance
    """
    region  = models.CharField(_('Region'), max_length=255) #autocomplete other party regions
    level   = models.CharField(_('Level'), max_length=255) #autocomplete other party levels
    name        = models.CharField(_('Name'), max_length=255)
    abbreviation = models.CharField(_('Abbreviated Name'), max_length=10)
    website     = models.CharField(_('Parties Website'), max_length=255, null=True, blank=True)
    contacts    = models.ManyToManyField(User, limit_choices_to=settings.CONTACT_LIMITATION, verbose_name=_('Contacts'))
    slogan      = models.CharField(_('Slogan'), max_length=255, null=True, blank=True)
    telephone	= models.CharField(_('Phone Number'), max_length=255)
    email		= models.EmailField(_('E-Mail'), null=True, blank=True)
    goals		= models.CharField(_('Goals'), max_length=255, null=True, blank=True)
    description	= models.CharField(_('Description'), max_length=255, null=True, blank=True)
    history		= models.CharField(_('Short History'), max_length=255, null=True, blank=True)
    manifasto_summary = models.CharField(_('Manifesto Summary'), max_length=255, null=True, blank=True)
    manifesto   = models.CharField(_('Manifesto'), max_length=2550, null=True, blank=True)
    logo = models.ImageField(_('Image'), upload_to='media/party', null=True, blank=True)

    def __unicode__(self):
        if self.abbreviation:
            return self.abbreviation
        else:
            return self.name
        
    class Meta:
        verbose_name, verbose_name_plural = _('Party'), _('Parties')


class Candidacy(models.Model):
    """
        A candidacy for a position within a council for optionally a party.
        Position indicated the number on the list.
    """
    election_party_instance     = models.ForeignKey('ElectionInstanceParty', 
                                                verbose_name=_('Election Party Instance'), 
                                                related_name='candidates')
    candidate                   = models.ForeignKey(User, 
                                        limit_choices_to=settings.POLITICIAN_LIMITATION, 
                                        verbose_name=_('Politician'))
    position                    = models.PositiveIntegerField(_('Position'))
    answers                     = models.ManyToManyField('questions.Answer', verbose_name=_('Answers'))

    def __unicode__(self):
        return self.candidate.username
    
    class Meta:
        verbose_name, verbose_name_plural = _('Candidacy'), _('Candidacies')

        
class ElectionInstanceParty(models.Model):
    """
        A link between the party, the election instance and the candidates
    """
    election_instance = models.ForeignKey(ElectionInstance, verbose_name=_('Election Instance'))
    party = models.ForeignKey(Party, verbose_name=_('Party'))
    position = models.PositiveIntegerField(_('Party Position'))

    def __unicode(self):
        return self.election_instance.council + " - " + self.party.name