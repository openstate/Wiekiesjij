import string
from random import seed, choice
from datetime import datetime
from django.db import models

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from elections.models import ElectionInstance
class VisitorResult(models.Model):
    """
        The results of a visitors match of a candidate.
    """

    user                = models.ForeignKey(User, verbose_name=_('User'), blank=True, null=True)
    ipaddress           = models.IPAddressField(_('Ip address of the user'), blank=True, null=True)
    hash                = models.CharField(_('Hash'), max_length=32, unique=True)
    datetime_stamp      = models.DateTimeField(_('Date Time Stamp'), default=datetime.now)
    visitor_answers     = models.TextField(_('Visitor Answer List'), blank=True, null=True)
    telephone           = models.CharField(_('Phone Number'), max_length=50, blank=True, null=True)
    election_instance   = models.ForeignKey(ElectionInstance, related_name='visitor_results', verbose_name=_('Election Instance'), blank=True, null=True)
    sent                = models.DateTimeField(_('Dent DateTime'), blank=True, null=True)

    class Meta:
        verbose_name, verbose_name_plural = _('Question'), _('Questions')
        get_latest_by = 'datetime_stamp'



    @classmethod
    def generate_hash(cls):
        """
            Generates a 32 characters hash with [a-zA-Z0-9]
        """
        chars = string.letters + string.digits
        while True:
            hash = ''.join([choice(chars) for i in xrange(32)])
            try:
                VisitorResult.objects.filter(hash = hash).get()
            except:
                return hash

    @classmethod
    def create(cls):
        """
            Create an result object
        """
        return cls.objects.create(
            hash = cls.generate_hash()
        )

    def __unicode__(self):
        return self.hash


class CandidateAnswers(models.Model):
    """
        The politicians answers that were used for a particular result of a visitor.
    """
    visitor_result      = models.ForeignKey(VisitorResult, verbose_name=_('Visitor Result'), related_name='candidate_answers', blank=True, null=True)
    candidate           = models.ForeignKey(User, verbose_name=_('Candidate'), blank=True, null=True)
    candidate_answers   = models.TextField(_('Candidates Answer List'), blank=True, null=True)
    candidate_question_scores = models.TextField(_('Question Score List'), blank=True, null=True)
    candidates_score    = models.PositiveIntegerField(_('Candidates Score'), max_length=3, blank=True, null=True)

    def __unicode__(self):
        return self.candidate.profile.full_name()


