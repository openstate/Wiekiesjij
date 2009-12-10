from django.db import models
from django.utils.translation import ugettext_lazy as _
from elections import settings
import datetime

from django.contrib.auth.models import User


class Council(models.Model):
    """
    A council
    """
    name                = models.CharField(_('Name'), max_length=255)
    region              = models.CharField(_('Region'), max_length=255) #Autocomplete other council regions
    level               = models.CharField(_('Level'), max_length=255) #Autocomplete other council levels
    chanceries          = models.ManyToManyField(User, limit_choices_to=settings.CHANCERY_LIMITATION,
                                          verbose_name=_('Chanceries'))
    abbreviation        = models.CharField(_('Abbreviated Name'), max_length=15)
    email               = models.EmailField(_('E-Mail'))
    street              = models.CharField(_('Street'), max_length=40)
    house_num           = models.CharField(_('House Number'), max_length=5)
    postcode            = models.CharField(_('Postcode'), max_length=7, help_text=_("Postcode (e.g. 9725 EK or 9211BV)"))
    town                = models.CharField(_('Town/City'), max_length=30)
    seats               = models.PositiveIntegerField(_('Seats'), max_length=30, null=True, blank=True)
    website             = models.URLField(_('Councils Website'), max_length=255, verify_exists=True, null=True,
                                          blank=True)
    picture             = models.ImageField(_('Picture'), upload_to='media/council', null=True, blank=True,
                                     help_text=_("A picture that will be used when displaying council details."),)
    desciption          = models.CharField(_('Description'), max_length=255, null=True, blank=True,
                                           help_text=_("A short description of the council"),)
    history             = models.CharField(_('History'), max_length=255, help_text=_("A short history of the council"),
                                           null=True, blank=True)
    background_color   = models.CharField(_('Background color'), max_length=6, help_text=_("Background color"),
                                          null=True, blank=True)
    foreground_color   = models.CharField(_('Foreground color'), max_length=6, help_text=_("Foreground color"),
                                          null=True, blank=True)
    another_color   = models.CharField(_('Another color'), max_length=6, help_text=_("Another color"),
                                          null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name, verbose_name_plural = _('Council'), _('Councils')

    def profile_incomplete(self):
        return not self.seats or not self.website or not self.picture or not self.description or not self.history

class ElectionEvent(models.Model):
    """
    A election event
    e.g. European Predisent elections 2009, Municipality elections 2010
    """
    
    name            = models.CharField(_('Name'), max_length=255)
    parent_region   = models.CharField(_('Parent region'), max_length=255) #autocomplete other electionevent regions
    level           = models.CharField(_('Level'), max_length=255) #autocomplete other electionevent levels
    desciption  = models.CharField(_('Description'), max_length=255, null=True, blank=True)
    question_due_period = models.PositiveIntegerField(_('Question due period')) #7
    profile_due_period = models.PositiveIntegerField(_('Profile due period')) #7
    candidate_due_period = models.PositiveIntegerField(_('Candidate due period')) #33
    party_due_period = models.PositiveIntegerField(_('Party due period')) #33

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name, verbose_name_plural = _('Election Event'), _('Election Events')

class ElectionInstanceModule(models.Model):
    """
        Holds modules for election instances
    """
    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'), unique=True)
    
    class Meta:
        verbose_name, verbose_name_plural = _('Module'), _('Modules')
        ordering = ('name',)
        
    def __unicode__(self):
        return self.name
        
    
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
    wizard_start_date = models.DateTimeField(_('Wizard start date'))
    num_lists       = models.PositiveIntegerField(_('Number of lists'), null=True, blank=True)
    website         = models.URLField(_('Elections Website'), max_length=255, verify_exists=True, null=True, blank=True)
    modules         = models.ManyToManyField('ElectionInstanceModule', verbose_name=_('Modules'), null=True, blank=True)

    def __unicode__(self):
        return self.council.name

    class Meta:
        verbose_name, verbose_name_plural = _('Election Instance'), _('Election Instances')    
        
    def party_dict(self):
        list = dict(map(lambda x: (x, None), range(1, self.num_lists+1)))
        list.update(dict(map(lambda x: (x.position, x), self.electioninstanceparty_set.all())))
        return list

    def question_deadline(self):
        return self.wizard_start_date.date() - datetime.timedelta(days=self.election_event.question_due_period)

    def profile_deadline(self):
        return self.wizard_start_date.date() - datetime.timedelta(days=self.election_event.profile_due_period)

    def candidate_deadline(self):
        return self.wizard_start_date.date() - datetime.timedelta(days=self.election_event.candidate_due_period)

    def party_deadline(self):
        return self.wizard_start_date.date() - datetime.timedelta(days=self.election_event.party_due_period)

    def question_overdue(self):
        return datetime.date.today() > self.question_deadline()

    def profile_overdue(self):
        return datetime.date.today() > self.profile_deadline()

    def candidate_overdue(self):
        return datetime.date.today() > self.candidate_deadline()

    def party_overdue(self):
        return datetime.date.today() > self.party_deadline()

    def add_party(self, party_name, position=0):
        '''
        Adds a party to the ElectionInstance, using ElectionInstanceParty.
        It only adds a name to the list, so the rest of the data shall be added manually.
        Returns ElectionInstanceParty object on success or boolean False on failure.
        @param str party_name
        @return mixed
        '''
        try:
            party = Party(name=party_name)
            party.save(force_insert=True)
            party_instance = ElectionInstanceParty(election_instance=self,
                                                   party=party,
                                                   list_length=settings.ELECTION_INSTANCE_PARTY_LIST_LENGTH_INITIAL,
                                                   position=position)
            party_instance.save(force_insert=True)
            party_instance.position = party_instance.id
            party_instance.save()
            return party_instance
        except Exception, e:
            print e
            return False
    
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

    def profile_incomplete(self):
        return not self.website or not self.slogan or not self.email or not self.goals or not self.description or \
               not self.history or not self.manifasto_summary or not self. manifesto or not self.logo

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

    def profile_incomplete(self):
        return True#self.candidate.profile.profile_incomplete()

    def questions_incomplete(self):
        return len(self.election_party_instance.instance.questions) - len(self.answers)

    def move_down(self):
        '''
        Changes the position of the current item with position of the previous one.
        Returns changed posotion of the current element on success or boolean False on failure.
        @return int

        Works!
        '''
        previous = self.__class__.objects.filter(position__lt=self.position).order_by('-position')[:1]
        if not previous:
            return False
        else:
            previous = previous[0]
            current_position = self.position
            self.position = previous.position
            previous.position = current_position
            self.save()
            previous.save()
            return self.position

    def move_up(self):
        '''
        Changes the position of the current item with position of the next one.
        Returns changed posotion of the current element on success or boolean False on failure.
        @return int
        '''
        next = self.__class__.objects.filter(position__gt=self.position).order_by('position')[:1]
        if not next:
            return False
        else:
            next = next[0]
            current_position = self.position
            self.position = next.position
            next.position = current_position
            self.save()
            next.save()
            return self.position

class ElectionInstanceParty(models.Model):
    """
        A link between the party, the election instance and the candidates
    """
    election_instance = models.ForeignKey(ElectionInstance, verbose_name=_('Election Instance'))
    party = models.ForeignKey(Party, verbose_name=_('Party'))
    position = models.PositiveIntegerField(_('Party Position'))
    list_length = models.PositiveIntegerField(_('List length'))

    def candidate_dict(self):
        list = dict(map(lambda x: (x, None), range(1, self.list_length+1)))
        list.update(dict(map(lambda x: (x.position, x), self.candidates.all())))
        return list

    def candidates_invited(self):
        return len(self.candidates.all())

    def candidates_notinvited(self):
        return self.list_length - self.candidates_invited()

    def candidates_profile_incomplete(self):
        return len(filter(lambda x: x.profile_incomplete(), self.candidates.all()))

    def candidates_questions_incomplete(self):
        return len(filter(lambda x: x.questions_incomplete(), self.candidates.all()))

    def __unicode__(self):
        return self.election_instance.council.name + " - " + self.party.name

    def move_down(self):
        '''
        Changes the position of the current item with position of the previous one.
        Returns changed posotion of the current element on success or boolean False on failure.
        @return int

        Works!
        '''
        previous = self.__class__.objects.filter(position__lt=self.position).order_by('-position')[:1]
        if not previous:
            return False
        else:
            previous = previous[0]
            current_position = self.position
            self.position = previous.position
            previous.position = current_position
            self.save()
            previous.save()
            return self.position

    def move_up(self):
        '''
        Changes the position of the current item with position of the next one.
        Returns changed posotion of the current element on success or boolean False on failure.
        @return int
        '''
        next = self.__class__.objects.filter(position__gt=self.position).order_by('position')[:1]
        if not next:
            return False
        else:
            next = next[0]
            current_position = self.position
            self.position = next.position
            next.position = current_position
            self.save()
            next.save()
            return self.position
