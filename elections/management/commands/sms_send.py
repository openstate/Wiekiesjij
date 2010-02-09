from django.core.management import BaseCommand

from elections.models import Council
from sms.models import sendsms
from datetime import datetime, timedelta
class Command(BaseCommand):
    help = 'Sends smss at correct time'
    
    def handle(self, *args, **options):
        councils = Council.objects.all()
        for council in councils:
            for event in council.events.all():
                if event.sent_datetime == None and (event.event_datetime - timedelta(days=1)) < datetime.now():
                    
                    try:
                        recipients = event.sms_recipients()
                        sendsms(event.originator, recipients, event.message, event.event_datetime)
                        event.sent_datetime = datetime.now()
                        event.save()
                    except:
                        pass