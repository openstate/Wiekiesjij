from django.core.management import BaseCommand

from elections.models import Council
from sms.models import sendsms
class Command(BaseCommand):
    help = 'Sends smss at correct time'
    
    def handle(self, *args, **options):
        councils = Council.objects.all()
        for council in councils:
            for event in council.events.all():
                recipients = event.sms_recipients()
                print sendsms(event.originator, recipients, event.message, event.event_datetime)

