from random import seed, choice
import string

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from utils.emails import send_email


class Invitation(models.Model):
    user_from       = models.ForeignKey(User, related_name="invitation_from", verbose_name=_('From User'))
    user_to         = models.ForeignKey(User, related_name="invitation_to", verbose_name=_('To User'))
    hash            = models.CharField(_('Hash'), max_length=32, unique=True)
    view            = models.CharField(_('View'), max_length=255, help_text=_('View the user should go to once the invitation is accepted'))
    text            = models.TextField(_('Text'), help_text=_('Message being displayed when the user first comes to the page'))
    
    subject         = models.CharField(_('Subject'), max_length=255, help_text=_('Subject of the invitation email'))
    html_template   = models.CharField(_('HTML template'), max_length=255, help_text=_('Html template to use for the invitation email'))
    plain_template  = models.CharField(_('Plain text template'), max_length=255, help_text=_('Plain text template to use for the invitation email'))
    
    type            = models.CharField(_('Type of the invited user'), null=True, blank=True, max_length=255)
    
    accepted        = models.BooleanField(_('Is Accepted?'), default=False)
    send_on         = models.DateTimeField(_('Email send'), blank=True, null=True, default=None) #Is the invitation send or not
    
    created         = models.DateTimeField(_('Created'), auto_now_add=True)
    updated         = models.DateTimeField(_('Updated'), auto_now=True)
    
    def __unicode__(self):
        return self.user_to.email
        
    def send(self):
        """
            Sends the invitation
        """
        send_email(
            self.subject, 
            'info@wiekiesjij.eu', 
            self.user_to.email, 
            {'invitation': self},
            {'html': self.html_template, 'plain': self.plain_template}
        )
        
    @classmethod
    def generate_hash(cls):
        """
            Generates a 32 characters hash with [a-zA-Z0-9]
        """
        seed()
        chars = string.letters + string.digits
        return ''.join([choice(chars) for i in range(32)])
        
        
    @classmethod
    def create(cls, user_from, user_to, view, text, subject, html_template, plain_template):
        """
            Create an invitation
        """
        return cls.objects.create(
            user_from = user_from,
            user_to = user_to,
            type = user_to.profile.type,
            view = view,
            text = text,
            subject = subject,
            html_template = html_template,
            plain_template = plain_template,
            hash = cls.generate_hash()
        )
        


