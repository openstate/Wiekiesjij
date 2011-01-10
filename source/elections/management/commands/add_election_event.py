import datetime

from django.core.management import BaseCommand

from elections.models import ElectionEvent

 
class Command(BaseCommand):
    help = 'Adds an electionevent'
    
    def handle(self, *args, **options):
        ee = ElectionEvent.objects.create(
            name='Provinciale Statenverkiezingen 2011',
            parent_region='Nederland',
            level='landelijk',
            default_date=datetime.datetime(2011, 3, 2),
            question_due_period=7,
            profile_due_period=7,
            candidate_due_period=30,
            party_due_period=33,
        )
        print "ElectionEvent added with id %d" % ee.pk
        
