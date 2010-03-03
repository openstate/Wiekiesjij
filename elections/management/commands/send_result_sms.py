from django.core.management import BaseCommand
from optparse import make_option

from elections.models import ElectionInstance
from sms.models import sendsms
from datetime import datetime
from sms.models import get_credit

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
            make_option('--list', '-l', action='store_true', default=False, dest='list',
                help='Lists the election instances'),
            make_option('--send', '-s', default=None, dest='send',
                help='Specifies the election instance to send the text messages for'),
            make_option('--fake', '-f', default=None, dest='fake',
                help='Shows the number of text messages that will be send for the election instance'),
        )
    help = 'Sends sms for a certain election instnace'
    
    def handle(self, *args, **options):
        
        list_eis = options.get('list')
        send = options.get('send')
        fake = options.get('fake')
        
        accepte_credit = get_credit()
        
        if list_eis:
            for ei in ElectionInstance.objects.filter(modules__slug='SMS').filter(visitor_results__sent__isnull=True).distinct().all():
                print "%s - %s" % (ei.pk, ei.name)
            return True
        
        if fake or send:
            id = fake or send
            try:
                ei = ElectionInstance.objects.get(pk=id)
            except:
                print "Election Instance not found"
                return False
            
            if ei.modules.filter(slug='SMS').count() == 0 or ei.visitor_results.filter(sent__isnull=True).count() == 0:
                print "Nothing to do"
                return False
                
            if accepte_credit > 0:
                
                recipients = ei.visitor_results.distinct('telephone').filter(telephone__isnull=False).values_list('telephone', flat=True)
                recipients = list(set(recipients))
                
                if send:
                    sendsms('Wiekiesjij', recipients, 'Vandaag tot 21.00 uur: gemeenteraadsverkiezingen! U kunt uw stem uitbrengen in een stemlokaal naar keuze. Neem uw stempas en ID-bewijs mee!', datetime.now())
                    ei.visitor_results.update(sent=datetime.now())
                    accepte_credit = accepte_credit - len(recipients)
                elif fake:
                    print "Would send %s messages for the election instance" % (len(recipients))
            else:
                print "Not enough credits"
                return False
            return True
