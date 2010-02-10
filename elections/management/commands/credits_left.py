from django.core.management import BaseCommand
from datetime import datetime
from elections.models import ElectionInstance, Council
from frontoffice.models import VisitorResult
from sms.models import sendsms, get_credit
from utils.emails import send_email

class Command(BaseCommand):
    help='Sends warnings if credit is less than 500 for each election instance. and one global omount for accepte'
    
    def handle(self, *args, **options):
        councils_credit = 0
        over_drawn = 0
        for council in Council.objects.all():
            if council.election_instances:
                councils_credit_left = council.credit_left()
                councils_credit = councils_credit + council.credit
                if councils_credit_left < 0:
                    over_drawn = over_drawn - councils_credit_left

        credit_left = get_credit()
        
        margin = credit_left - councils_credit - over_drawn

        if margin < 0:
            message = 'WARINING: Accepte has not enough credit bought. Currently Accepte has %s credits left. Councils have reserved: %s. %s credits have not been reserved. Total (Acceptes credits - reserver - non_reserved): %s' %(str(credit_left), str(councils_credit), str(over_drawn),str(margin))

            try:
                send_email(
                        'Credits Negative -- IMPORTANT',
                        'bmcmahon@gmail.com',
                        'bmcmahon@gmail.com',
                        {'message': message },
                        {'plain': 'elections/credits_low.txt'},
                )

            except:
                pass

        elif margin < 2000:

            message = 'Accepte may not have enough credit bought. Currently Accepte has %s credits left. Councils have reserved: %s. %s credits have not been reserved. Total (Acceptes credits - reserver - non_reserved): %s' %(str(credit_left), str(councils_credit), str(over_drawn),str(margin))

            try:
                send_email(
                            'Credits Low',
                            'bmcmahon@gmail.com',
                            'bmcmahon@gmail.com',
                            {'message': message },
                            {'plain': 'elections/credits_low.txt'},
                )


            except:
                pass

        else:
            pass