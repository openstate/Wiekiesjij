from django.db import models
from django.utils.translation import ugettext_lazy as _
from elections import settings
from datetime import datetime
from utils.functions import move_up, move_down
from utils.fields import DutchMobilePhoneField
from django.contrib.auth.models import User
from utils.emails import send_email

from elections.functions import get_popularity
from questions.settings import BACKOFFICE_QUESTION_TYPES


class Council(models.Model):
    """
    A council
    """
    name                = models.CharField(_('Name'), max_length=255)
    region              = models.CharField(_('Region'), max_length=255) #Autocomplete other council regions
    level               = models.CharField(_('Level'), max_length=255) #Autocomplete other council levels
    chanceries          = models.ManyToManyField(User, limit_choices_to=settings.CHANCERY_LIMITATION,
                                          verbose_name=_('Chanceries'), related_name='councils')
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
    description          = models.TextField(_('Description'), null=True, blank=True,
                                           help_text=_("A short description of the council"),)
    history             = models.TextField(_('History'), help_text=_("Hier kunt u een korte geschiedenis en beschrijving van uw Tweede Kamer invullen."),
                                           null=True, blank=True)
    background_color   = models.CharField(_('Background color'), max_length=6, null=True, blank=True)
    foreground_color   = models.CharField(_('Foreground color'), max_length=6, null=True, blank=True)
    another_color   = models.CharField(_('Another color'), max_length=6, null=True, blank=True)
    credit_warning  = models.DateTimeField(_('Credit Warning Datetime Stamp'), null=True, blank=True)
    credit          = models.PositiveIntegerField(_('Seats'), max_length=8, default=0)

    def __unicode__(self):
        return self.name

    @property
    def chancery_id(self):
        if self.chanceries.count() == 0:
            return None
        return self.chanceries.all()[0].pk

    class Meta:
        verbose_name, verbose_name_plural = _('Council'), _('Councils')
        ordering = ('name',)

    @property
    def profile_incomplete(self):
        return not self.seats or not self.street or not self.house_num or not self.postcode or not self.town

    def credit_left(self):
        total_credits = 0
        phone_nums = []
        if self.election_instances:

            for election_instance in self.election_instances.all():
                dict_phones = election_instance.visitor_results.filter(election_instance=election_instance, sent=None).exclude(telephone=None).values('telephone')
                for  dict_phone in dict_phones:
                    if 'telephone' in dict_phone.keys():
                        phone_nums.append(dict_phone['telephone'])

            total_credits = len(set(phone_nums))

        for event in self.events.all():
            if event.sent_datetime == None:
                recipients = event.sms_recipients()
                total_credits = total_credits + len(recipients)
        #print self.name, total_credits, phone_nums
        credits_left = self.credit - total_credits

        if self.credit_warning == None:
            if credits_left < 500:
                message = self.name + ' has only ' + str(credits_left) + ' credits left.'

                try:
                    send_email(
                                _('A Councils Credit is Low'),
                                'info@wiekiesjij.nl',
                                'webmaster@wiekiesjij.nl',
                                {'message': message },
                                {'plain': 'elections/credits_low.txt'},
                    )
                    self.credit_warning = datetime.now()
                    self.save()

                except:
                    pass
                message = '%s has only %s credits left. Please contact us if you would like to purchase more credit. If you do not have enough pre-bought credit when a message is sent you will be charged at a higher rate for that text message.'%(self.name, str(credits_left))

                try:
                    send_email(
                                _('Your Credit is Low'),
                                'info@wiekiesjij.nl',
                                'webmaster@wiekiesjij.nl',
                                {'message': message },
                                {'plain': 'elections/credits_low.txt'},
                    )
                    #'credits_warning+info@wiekiesjij.nl',
                    #'info@wiekiesjij.nl',
                    self.credit_warning = datetime.now()
                    self.save()
                except:
                    pass
        return credits_left


    @property
    def election_instance(self):
        if not hasattr(self, '_election_instance'):
            result = self.election_instances.filter(election_event__pk=settings.ELECTION_EVENT_ID)
            if result.count() == 0:
                return None
            self._election_instance = result[0]
        return self._election_instance

class ElectionEvent(models.Model):
    """
    A election event
    e.g. European Predisent elections 2009, Municipality elections 2010
    """

    default_date    = models.DateTimeField(_('Default Date'), help_text = _("Default date for all election instances"), default = datetime.now)
    name            = models.CharField(_('Name'), max_length=255)
    parent_region   = models.CharField(_('Parent region'), max_length=255) #autocomplete other electionevent regions
    level           = models.CharField(_('Level'), max_length=255) #autocomplete other electionevent levels
    description  = models.CharField(_('Description'), max_length=255, null=True, blank=True)
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

    council         = models.ForeignKey(Council, verbose_name=_('Council'), related_name='election_instances')
    election_event  = models.ForeignKey(ElectionEvent, verbose_name=_('Election Event'))
    parties         = models.ManyToManyField('Party', verbose_name=_('Parties'), through='ElectionInstanceParty')
    questions       = models.ManyToManyField('questions.Question', through='ElectionInstanceQuestion', verbose_name=_('Questions'), null=True, blank=True)
    name            = models.CharField(_('Name'), max_length=255)
    start_date      = models.DateTimeField(_('Start Date'))
    end_date        = models.DateTimeField(_('End Date'))
    wizard_start_date = models.DateTimeField(_('Wizard start date'))
    num_lists       = models.PositiveIntegerField(_('Number of lists'), default = 0)
    website         = models.URLField(_('Elections Website'), max_length=255, verify_exists=True, null=True, blank=True)
    modules         = models.ManyToManyField('ElectionInstanceModule', verbose_name=_('Modules'), null=True, blank=True)

    def __unicode__(self):
        return self.council.name

    class Meta:
        verbose_name, verbose_name_plural = _('Election Instance'), _('Election Instances')

    def party_dict(self):
        list = dict(map(lambda x: (x, None), range(1, self.num_lists+1)))
        list.update(dict(map(lambda x: (x.position, x), self.election_instance_parties.all())))
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
        except Exception:
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
    position            = models.PositiveIntegerField(_('Position'), default=0)

    def __unicode__(self):
        return self.election_instance.council.name + ' - ' + self.question.title

    class Meta:
        verbose_name, verbose_name_plural = _('Election Instance Question'), _('Election Instance Questions')
        ordering = ('position', 'question__id',)

    def move_down(self):
        '''
        Changes the position value with next row
        '''
        return move_down(self, 'position', 1000, {'election_instance': self.election_instance.id})

    def move_up(self):
        '''
        Changes the position value with previous row
        '''
        return move_up(self, 'position', 1, {'election_instance': self.election_instance.id})

class ElectionInstanceQuestionAnswer(models.Model):
    '''
        Answer to the given question. Containst actual value to the question.
    '''
    election_instance_question = models.ForeignKey(ElectionInstanceQuestion, verbose_name=_('Election Instance Question'))
    candidate = models.ForeignKey(User, limit_choices_to=settings.POLITICIAN_LIMITATION, verbose_name=_('Candidate'))
    answer_value = models.CharField(_('Answer'), null=True, blank=True, max_length=255)

    def __unicode__(self):
        return self.election_instance_question.election_instance.council.name + \
               ' - ' + self.election_instance_question.question.title + ' - ' + str(self.answer_value)

    class Meta:
        verbose_name, verbose_name_plural = _('Election Instance Question Answer'), _('Election Instance Question Answers')
        unique_together = (('election_instance_question', 'candidate'))

class Party(models.Model):
    """
        A party within an election instance
    """
    region  = models.CharField(_('Region'), max_length=255) #autocomplete other party regions
    level   = models.CharField(_('Level'), max_length=255) #autocomplete other party levels
    name        = models.CharField(_('Name'), max_length=255)
    abbreviation = models.CharField(_('Abbreviated Name'), max_length=20)
    address_street      = models.CharField( ('Street'), max_length=255, null=True, blank=True)
    address_number      = models.CharField( ('Number'), max_length=255, null=True, blank=True)
    address_postalcode  = models.CharField( ('Postalcode'), max_length=255, null=True, blank=True)
    address_city        = models.CharField( ('City'), max_length=255, blank=True, null=True)
    website     = models.CharField(_('Parties Website'), max_length=255, null=True, blank=True)
    contacts    = models.ManyToManyField(User, limit_choices_to=settings.CONTACT_LIMITATION, verbose_name=_('Contacts'), related_name='parties')
    slogan      = models.CharField(_('Slogan'), max_length=255, null=True, blank=True)
    telephone	= models.CharField(_('Phone Number'), max_length=255)
    email		= models.EmailField(_('E-Mail'), null=True, blank=True)
    goals		= models.CharField(_('Goals'), max_length=255, null=True, blank=True)
    description	= models.CharField(_('Description'), max_length=255, null=True, blank=True)
    history		= models.CharField(_('Short History'), max_length=255, null=True, blank=True)
    manifesto_summary   = models.TextField(_('Manifesto Summary'), null=True, blank=True)
    manifesto   = models.URLField(_('Manifesto'), max_length=255, null=True, blank=True)
    logo = models.ImageField(_('Image'), upload_to='media/party', null=True, blank=True)
    num_seats = models.PositiveIntegerField(_('Number of seats'), null=True, blank=True, help_text=_('The number of seats you currently hold'))
    movie        = models.URLField(_('Movie'), max_length=255, verify_exists=True, blank=True, null=True,
                                      help_text=_('Link to YouTube video'))

    class Meta:
        verbose_name, verbose_name_plural = _('Party'), _('Parties')

    def __unicode__(self):
        if self.abbreviation:
            return self.abbreviation
        else:
            return self.name

    @property
    def popularity(self):
        if not hasattr(self, '_popularity'):
            candpop, partypop = get_popularity(self.current_eip.election_instance_id)
            self._popularity = int(partypop.get(self.current_eip.pk, 0))
        if self._popularity < 20:
            return 20
        return self._popularity

    def profile_incomplete(self):
        return not self.address_street or not self.address_number or not self.address_postalcode or not self.address_city or not self.abbreviation or not self.name or not self.description

    @property
    def address(self):
        return {
            'street': self.address_street,
            'number': self.address_number,
            'postalcode': self.address_postalcode,
            'city': self.address_city,
        }

    @property
    def current_eip(self):
        if not hasattr(self, '_eip'):
            result = self.election_instance_parties.filter(election_instance__election_event__pk=settings.ELECTION_EVENT_ID)
            if result.count():
                self._eip = result[0]
            else:
                return None
        return self._eip

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
                                        verbose_name=_('Politician'), related_name='elections')
    position                    = models.PositiveIntegerField(_('Position'))
    answers                     = models.ManyToManyField('questions.Answer', verbose_name=_('Answers'))


    def __unicode__(self):
        return self.candidate.username

    class Meta:
        verbose_name, verbose_name_plural = _('Candidacy'), _('Candidacies')
        unique_together = (
            ('election_party_instance', 'candidate'),
            ('election_party_instance', 'position'),
        )

    def profile_incomplete(self):
        return (self.candidate.profile.profile_incomplete() or self.answers.count() == 0)

    def questions_incomplete(self):
        return len(self.election_party_instance.instance.questions) - len(self.answers)

    def move_down(self):
        '''
        Changes the position value with next row
        '''
        return move_down(self, 'position', self.election_party_instance.list_length, {'election_party_instance': self.election_party_instance.id})

    def move_up(self):
        '''
        Changes the position value with previous row
        '''
        return move_up(self, 'position', 1, {'election_party_instance': self.election_party_instance.id})

class ElectionInstanceParty(models.Model):
    """
        A link between the party, the election instance and the candidates
    """
    election_instance = models.ForeignKey(ElectionInstance, verbose_name=_('Election Instance'), related_name='election_instance_parties')
    party = models.ForeignKey(Party, verbose_name=_('Party'), related_name='election_instance_parties')
    position = models.PositiveIntegerField(_('Party Position'))
    list_length = models.PositiveIntegerField(_('List length'), default = 0)

    class Meta:
        unique_together = ('election_instance', 'position')

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

    def candidates_active(self):
        return self.candidates.filter(candidate__is_active=True).count()

    def candidates_complete(self):
        qc = self.election_instance.questions.filter(question_type__in=BACKOFFICE_QUESTION_TYPES).count()
        return self.candidates.annotate(num_answers=models.Count('answers')).filter(num_answers__gt=qc).count()

    def candidate_completeness_perc(self):
        try:
            return 100 * self.candidates_complete()/self.list_length
        except:
            return 0

    def __unicode__(self):
        return self.election_instance.council.name + " - " + self.party.name

    def move_down(self):
        '''
        Changes the position value with next row
        '''
        return move_down(self, 'position', self.election_instance.num_lists, {'election_instance': self.election_instance.id})

    def move_up(self):
        '''
        Changes the position value with previous row
        '''
        return move_up(self, 'position', 1, {'election_instance': self.election_instance.id})

class CouncilEvent(models.Model):

    council  = models.ForeignKey(Council, verbose_name=_('Council'), related_name='events')
    title = models.CharField(_('Title'), max_length=60)
    originator = models.CharField(_('SMS Originator'), max_length=11)
    location = models.TextField(_('Location'))
    message = models.CharField(_('SMS Message'), max_length=140)
    event_datetime  = models.DateTimeField(_('Date and Time of Event'), blank = True)
    sent_datetime = models.DateTimeField(_('Date and Time when sms were sent'), blank = True, null=True)

    def __unicode__(self):
        return self.title

    def sms_recipients(self):
        recipient_list = []
        for subscription in self.sms_subscriptions.all():
            recipient_list.append(subscription.phone_number)
        rset = set(recipient_list)
        return list(rset)



class SmsSubscription(models.Model):
    council_event = models.ForeignKey(CouncilEvent, verbose_name=_('Council Event'), related_name='sms_subscriptions')
    phone_number = models.CharField(_('Phone Number'), max_length=15)
