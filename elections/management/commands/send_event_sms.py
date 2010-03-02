from django.core.management import BaseCommand
from optparse import make_option

from elections.models import CouncilEvent
from sms.models import sendsms
from datetime import datetime
from sms.models import get_credit

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
            make_option('--list', '-l', action='store_true', default=False, dest='list',
                help='Lists the events with the ids'),
            make_option('--send', '-s', default=None, dest='send',
                help='Specifies which event is to send them for'),
            make_option('--fake', '-f', default=None, dest='fake',
                help='Specifies which event is to send them for'),
        )
    help = 'Sends sms for a certain event'
    
    def handle(self, *args, **options):
        
        list_events = options.get('list')
        send = options.get('send')
        fake = options.get('fake')
        
        accepte_credit = get_credit()
        
        if list_events:
            for event in CouncilEvent.objects.filter(sent_datetime__isnull=True).all():
                print '%s - %s for %s' % (event.pk, event.title, event.council)
            return True
        
        if fake or send:
            id = fake or send
            try:
                event = CouncilEvent.objects.get(pk=id)
            except:
                print "Event not found"
                return False
            
        
            if event.sent_datetime == None:
                if accepte_credit > 0:
                    recipients = event.sms_recipients()
                    
                    if send:
                        sendsms(event.originator, recipients, event.message, datetime.now())
                        event.sent_datetime = datetime.now()
                        event.save()
                        accepte_credit = accepte_credit - len(recipients)
                    elif fake:
                        print "Would send %s messages for the event" % (len(recipients))
                else:
                    print "Not enough credits"
                    return False
            return True
        