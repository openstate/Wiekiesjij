from django.db import models
from django.utils.translation import ugettext_lazy as _
import urllib, urllib2
from xml.dom.minidom import parseString
import types
from datetime import datetime
from sms.settings import USERNAME, PASSWORD, DEFAULT_MOLLIEGW
from  sms.exceptions import by_code

def sendsms(originator, recipients, message, deliverydate):

    args = {}
    new_sms = Sms()
    args['username'] = USERNAME
    args['password'] = PASSWORD
    args['originator'] = originator
    args['recipients'] = recipients
    args['message'] = message
    args['gateway'] = None
    args['deliverydate'] = deliverydate
    molliegw = DEFAULT_MOLLIEGW

    # optional arguments
    new_sms.originator = originator
    recipient_list = ''
    for recipient in recipients:
        recipient_list = recipient_list + str(recipient)
    new_sms.recipients = recipient_list
    new_sms.message = message
    new_sms.deliverydate = deliverydate
    url = molliegw + "?" + urllib.urlencode(args)
    response = urllib2.urlopen(url)
    new_sms.sent_time = datetime.now()
    responsexml = response.read()
    dom = parseString(responsexml)
    new_sms.numbers_sent_to = int(dom.getElementsByTagName("recipients")[0].childNodes[0].data)
    new_sms.success = dom.getElementsByTagName("success")[0].childNodes[0].data
    new_sms.resultcode = int(dom.getElementsByTagName("resultcode")[0].childNodes[0].data)
    new_sms.resultmessage = dom.getElementsByTagName("resultmessage")[0].childNodes[0].data


    if new_sms.success != "true":
        e = by_code[new_sms.resultcode]
        new_sms.error = e
        new_sms.save()
        raise e(new_sms.resultmessage)
    else:
        new_sms.sent = True


    new_sms.save()
    return 'SMS sent'




class Sms(models.Model):
    """
       SMS record
    """
    originator = models.CharField(_('Whois sending the message'), max_length=11)
    sent_time     = models.DateTimeField(_('Sent Date and Time'), blank = True)
    recipients  = models.TextField(_('Phone Numbers of recipients'))
    numbers_sent_to = models.TextField(_('Phone Numbers of recipients'))
    sent        = models.BooleanField(_('Message was sent'), default = False)
    success = models.TextField(_('Success of sms send'))
    resultmessage       = models.TextField(_('Result Message'), blank = True)
    resultcode       = models.TextField(_('Result Code'), blank = True)
    error = models.TextField(_('Result Code'), blank = True)
    message       = models.CharField(_('SMS Message'), max_length=160)
    deliverydate    = models.DateTimeField(_('Date and Time to send sms'), blank = True)
    scheduling_description  = models.TextField(_('Information about sms for identifying'), blank = True)

#    def __unicode__(self):
#        return u"%s sent %s on %s for sending on %s to the following numbers: %s" % (self.originator, self.message, self.sent_time.strftime('%d-%m-%Y %H:%M:%S.%f'), self.deliverydate.strftime('%d-%m-%Y %H:%M:%S.%f'), self.recipients)


