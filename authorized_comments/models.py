from django.contrib.comments.models import Comment
from django.contrib.comments import signals
from django.core.mail import mail_managers
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site

def comment_flagged(sender, **kwargs):
    """
        Signal handler
    """
    flag = kwargs['flag']

    if flag.flag == flag.SUGGEST_REMOVAL:

        current_site = Site.objects.get_current()
        domain = current_site.domain

        subject = _('A comment was flagged')
        message = _("A comment was flagged as inappropiate. Check out http://%(domain)s") % dict(domain=domain+reverse('fo.goal', args=[flag.comment.object_pk])) #Hardcoded goal. Maybe change?
        mail_managers(subject, message, fail_silently=False)
        

    

# Connect the signal handler to the signal invoker
signals.comment_was_flagged.connect(comment_flagged)

class AuthorizedComment(Comment):

    def get_flag_url(self):
        return "/auth_comments/flag/%s/" % self.id

    def get_delete_url(self):
        return "/auth_comments/delete/%s/" % self.id
