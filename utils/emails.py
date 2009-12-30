from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMultiAlternatives
from django.template import loader, Context
from django.contrib.sites.models import Site

def _render_content(context, template):
    '''
    Renders context of the e-mail. If no template specified, simply returns the context back, otherwise loads context
    into the specified template.
    '''

    if template:
        t = loader.get_template(template)
        return t.render(Context(context))
    return context

def send_email(subject, from_email, to, context, template):
    '''
    Sends an e-mail. Additionally might send an html version as an attachment.
    subject - text
    from_email - text
    to - text
    context - dictionary
    template - dictionary, must have at least one key named "plain"
    '''
    if not template.has_key('plain'):
        raise Exception(_("No plain-text template is specified for sending of an e-mail."))
        
    #Add the current site to the context
    current_site = Site.objects.get_current()
    site_name = current_site.name
    domain = current_site.domain
    context.update({'site_name': site_name, 'domain': domain})
    
    to_list = [to]
    bcc_list = ['wietse.vanderwal+wiekiesjij_mail@accepte.nl']
    text_content = _render_content(context, template['plain'])
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_list, bcc_list)

    if template.has_key('html'):
        html_content = _render_content(context, template['html'])
        msg.attach_alternative(html_content, "text/html")

    msg.send()