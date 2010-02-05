from django.core.management import BaseCommand
from datetime import datetime
from elections.models import ElectionInstance
from frontoffice.models import VisitorResult
from sms.models import sendsms
class Command(BaseCommand):
    help = 'Sends smss at correct time'
    
    def handle(self, *args, **options):
        for election_instance in ElectionInstance.objects.all():
            #if election_instance.modules.filter(slug='SMS').count() != 0:

            phone_nums = VisitorResult.objects.filter(election_instance=election_instance).exclude(telephone=None).values('telephone').distinct()
            #print phone_nums
            for phone_num in phone_nums:

                visitor_results = VisitorResult.objects.filter(election_instance=election_instance, telephone=phone_num['telephone']).latest()
                print visitor_results
                #get(election_instance=election_instance, telephone=phone_num).

                print sendsms(election_instance.council.name[0:11], phone_num['telephone'], visitor_results.hash, datetime.now())

