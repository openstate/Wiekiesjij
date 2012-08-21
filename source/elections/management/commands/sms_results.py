from django.core.management import BaseCommand
from datetime import datetime
from elections.models import ElectionInstance
from frontoffice.models import VisitorResult
from sms.models import sendsms
from sms.models import get_credit
from utils.emails import send_email
class Command(BaseCommand):
    help = 'Sends smss at correct time'

    def handle(self, *args, **options):
        accepte_credits = get_credit()
        for election_instance in ElectionInstance.objects.all():
            if election_instance.modules.filter(slug='SMS').count() != 0:

                phone_nums = VisitorResult.objects.filter(election_instance=election_instance).exclude(telephone=None).values('telephone').distinct()
                for phone_num in phone_nums:
                    if accepte_credits > 0:
                        visitor_results = VisitorResult.objects.filter(election_instance=election_instance, telephone=phone_num['telephone']).latest()
                        if visitor_results.sent == None:
                            #get(election_instance=election_instance, telephone=phone_num).
                            top_3 = visitor_results.candidate_answers.order_by('-candidates_score')[:3]
                            message = 'Voting is tomorrow, your top three candidates were '
                            for candidate in top_3:

                                message= message + str(candidate.candidate.profile.full_name()) + ', score: ' + str(candidate.candidates_score) + ' '

                            sendsms(election_instance.council.name[0:11], phone_num['telephone'], message, datetime.now())
                            visitor_results.sent = datetime.now()
                            visitor_results.save()
                            accepte_credits = accepte_credits - 1


                    else:
                        message = 'ERROR: Accepte has not enough credit bought to send queued sms\'s. Buy credits imediately! To identify how many, run credits_left command. Then Purchase required amount. Then Manually run sms_results command again.'

                        send_email(
                                'Credits Negative -- Error',
                                'info@wiekiesjij.nl',
                                'webmaster@wiekiesjij.nl',
                                {'message': message },
                                {'plain': 'elections/credits_low.txt'},
                        )
                        return False
        return True
