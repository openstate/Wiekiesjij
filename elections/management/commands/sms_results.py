from django.core.management import BaseCommand
from datetime import datetime
from elections.models import ElectionInstance
from frontoffice.models import VisitorResult
from sms.models import sendsms
class Command(BaseCommand):
    help = 'Sends smss at correct time'
    
    def handle(self, *args, **options):

        for election_instance in ElectionInstance.objects.all():
            if election_instance.modules.filter(slug='SMS').count() != 0:
            
                phone_nums = VisitorResult.objects.filter(election_instance=election_instance).exclude(telephone=None).values('telephone').distinct()
                for phone_num in phone_nums:

                    visitor_results = VisitorResult.objects.filter(election_instance=election_instance, telephone=phone_num['telephone']).latest()

                    #get(election_instance=election_instance, telephone=phone_num).
                    top_3 = visitor_results.candidate_answers.order_by('-candidates_score')[:3]
                    message = 'Voting is tomorrow your top three candidates were '
                    for candidate in top_3:
                        message= message + str(candidate.candidate.profile.full_name()) + ', score: ' + str(candidate.candidates_score) + ' '
                    sendsms(election_instance.council.name[0:11], phone_num['telephone'], message, datetime.now())


