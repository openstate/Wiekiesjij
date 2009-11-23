from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from django.contrib.auth.models import User

class Council(models.Model):
    """
    A council
    """
    
    name        = models.CharField(_('Name'), max_length=255)    
    region      = models.CharField(_('Region'), max_length=255) #Autocomplete other council regions
    level       = models.CharField(_('Level'), max_length=255) #Autocomplete other council levels
    
    chancery    = models.ForeignKey(User, limit_choices_to=settings.CHANCERY_LIMITATION, verbose_name=_('Chancery'))
    
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
    
    class Meta:
        verbose_name, verbose_name_plural = _('Election Event'), _('Election Events')

class ElectionInstance(models.Model):
    """
    A election instance for an election event
    e.g. Municipality Groningen (for Election Event Municipality elections 2010)
    """
    
    council         = models.ForeignKey(Council, verbose_name=_('Council'))
    election_event  = models.ForeignKey(ElectionEvent, verbose_name=_('Election Event'))
    
    parties         = models.ManyToManyField('Party', verbose_name=_('Parties'))
    questions       = models.ManyToManyField(settings.QUESTION_MODEL, 
                            through='ElectionInstanceQuestion', 
                            verbose_name=_('Questions'))
                            
    class Meta:
        verbose_name, verbose_name_plural = _('Election Instance'), _('Election Instances')

class ElectionInstanceQuestion(models.Model):
    """
        Links a election instance to a question
        Has a locked property to indicate that the question is only editable for the admin
    """
    election_instance   = models.ForeignKey(ElectionInstance, verbose_name=_('Election Instance'))
    question            = models.ForeignKey(settings.QUESTION_MODEL, verbose_name=_('Question'))
    
     #locked means it can only be edited by admins because it's used in multiple electioninstances
    locked              = models.BooleanField(_('Locked'), default=False)

    class Meta:
        verbose_name, verbose_name_plural = _('Election Instance Question'), _('Election Instance Questions')
    
class Party(models.Model):
    """
        A party within an election instance
    """
    
    name    = models.CharField(_('Name'), max_length=255)

    contact = models.ForeignKey(User, limit_choices_to=settings.CONTACT_LIMITATION, verbose_name=_('Contact'))
    
    region  = models.CharField(_('Region'), max_length=255) #autocomplete other party regions
    level   = models.CharField(_('Level'), max_length=255) #autocomplete other party levels
    
    class Meta:
        verbose_name, verbose_name_plural = _('Party'), _('Parties')


class Candidacy(models.Model):
    """
        A candidacy for a position within a council for optionally a party.
        Position indicated the number on the list.
    """
    party               = models.ForeignKey(Party, 
                                related_name='candidates', 
                                null=True, 
                                blank=True, 
                                verbose_name=_('Party'))
    
    politician          = models.ForeignKey(User, 
                                limit_choices_to=settings.POLITICIAN_LIMITATION, 
                                verbose_name=_('Politician'))
    
    election_instance   = models.ForeignKey(ElectionInstance, verbose_name=('Election Instance'))
    position            = models.PositiveIntegerField(_('Position'))
    
    answers             = models.ManyToManyField(settings.ANSWER_MODEL, verbose_name=_('Answers'))
    
    class Meta:
        verbose_name, verbose_name_plural = _('Candidacy'), _('Candidacies')

        