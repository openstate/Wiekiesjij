from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User



class GraphFormWizardSession(models.Model):
    """Used to store the wizard's data"""
    user          = models.ForeignKey(User, verbose_name=_('User'), null = True)
    date          = models.DateTimeField(_('Last access'), auto_now = True)
    wizard_class  = models.CharField(_('Wizards class name'), max_length=255)
    wizard_name   = models.CharField(_('Wizards instance name'), max_length=255, null=True, blank = True)
    content       = models.TextField(_('Session data'), blank = True)
    meta          = models.TextField(_('Meta data'), blank = True)
    complete      = models.BooleanField(_('Is this session complete?'), default = False)


class PostLog(models.Model):
    """
        Log file for posts
    """
    
    path        = models.CharField(_('Request path'), max_length=255)
    
    data        = models.TextField(_('Post data'), blank=False)

    user        = models.ForeignKey(User, verbose_name=_('User'), null=True)
    ipaddress   = models.IPAddressField(_('Ip address of the user'))
    
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name, verbose_name_plural = _('Post Log'), _('Post logs')
        ordering = ('-created',)
    
    def __unicode__(self):
        return u"%s by %s on %s" % (self.path, self.user.email, self.created.strftime('%d-%m-%Y %H:%M:%S.%f'))

    