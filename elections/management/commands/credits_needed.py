from django.core.management import BaseCommand

from elections.settings import ELECTION_EVENT_ID
from elections.models import ElectionInstance, Council
from sms.models import get_credit

class Command(BaseCommand):
    help = 'Test how many credits accepte is gonna need'

    def handle(self, *args, **options):
        council_costs = {}
        councils = Council.objects.all()
        accepte_credit =  get_credit()
        
        for council in councils:
            try:
                ei = council.election_instances.get(election_event__id=ELECTION_EVENT_ID)
            except:
                ei = None

            if ei is not None and ei.modules.filter(slug='Event-SMS').count() == 0:
                continue

            council_count = 0
            for event in council.events.filter(sent_datetime__isnull=True).all():
                council_count += len(event.sms_recipients())
            
            council_costs.update({council.pk: council_count})
            
        #VisitorResult texts
        for ei in ElectionInstance.objects.filter(modules__slug__in=['SMS']):
            council_count = council_costs.get(ei.council.pk, 0)
            
            recipients = []
            for vr in ei.visitor_results.all():
                if vr.telephone:
                    recipients.append(vr.telephone)
                    
            council_count += len(list(set(recipients)))
            council_costs.update({ei.council.pk: council_count})
            
        credit_costs = 0
        for council in councils:
            if council.pk in council_costs:
                credit_costs += council_costs.get(council.pk, 0)
                print council, 'credits used:', council_costs.get(council.pk, 0)
                
        print '---'
        print 'Total:', credit_costs
        print 'Currently available:', accepte_credit
        return