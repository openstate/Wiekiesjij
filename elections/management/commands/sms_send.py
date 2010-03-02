from django.core.management import BaseCommand

from elections.models import Council
from sms.models import sendsms
from datetime import datetime, timedelta
from sms.models import get_credit
from utils.emails import send_email

class Command(BaseCommand):
    help = 'Sends sms at correct time'
    
    def handle(self, *args, **options):
        councils = Council.objects.all()
        accepte_credit =  get_credit()
        for council in councils:
            for event in council.events.all():
                if event.sent_datetime == None and (event.event_datetime - timedelta(days=1)) < datetime.now():
                    if accepte_credit > 0:

                        recipients = event.sms_recipients()
                        sendsms(event.originator, recipients, event.message, datetime.now())
                        event.sent_datetime = datetime.now()
                        event.save()
                        accepte_credit = accepte_credit - len(recipients)

                    else:
                        message = 'ERROR: Accepte has not enough credit bought to send queued sms\'s. Buy credits imediately! To identify how many, run credits_left command. Then Purchase required amount. Then Manually run sms_send command again.'

                        send_email(
                                'Credits Negative -- Error',
                                'info@wiekiesjij.nl',
                                'bmcmahon@gmail.com',
                                {'message': message },
                                {'plain': 'elections/credits_low.txt'},
                        )
                        return False
        return True