from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _



class OpenIDMap(models.Model):
    """
        Maps OpenID to politician profile. Each social network can have its own
        OpenID.
    """
    user            = models.ForeignKey(User, verbose_name=_('Related user'), related_name="openids", null=False)
    openid          = models.CharField(_('Per container OpenID'), max_length=50, blank=False, null=False)
    container       = models.CharField(_('Container domain'), max_length=250, blank=False, null=False)
    created         = models.DateTimeField(_('Date Time Stamp'), auto_now = True)

    class Meta:
        unique_together = (('openid','container'),)