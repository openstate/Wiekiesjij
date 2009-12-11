from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User




class GraphFormWizardSession(models.Model):
    """Used to store the wizard's data"""
    user          = models.ForeignKey(User, verbose_name=_('User'))
    date          = models.DateTimeField(_('Last access'), auto_now = True)
    wizard_class  = models.CharField(_('Wizards class name'), max_length=255)
    wizard_name   = models.CharField(_('Wizards instance name'), max_length=255, null=True, blank = True)
    content       = models.TextField(_('Session data'), blank = True)
    meta          = models.TextField(_('Meta data'), blank = True)
    complete      = models.BooleanField(_('Is this session complete?'), default = False)
