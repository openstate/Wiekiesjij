from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class CandidateInvitation(models.Model):
    user_from = models.ForeignKey(User, related_name="invitation_from", verbose_name=_('From User'))
    user_to = models.ForeignKey(User, related_name="invitation_to", verbose_name=_('To User'))
    hash = models.CharField(max_length=32)
    accepted = models.BooleanField()
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    view = models.CharField(max_length=255)
    text = models.TextField()
    email = models.CharField(max_length=255)

    def __unicode__(self):
        return self.user_to.email



