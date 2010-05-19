import datetime

from django.core.management import BaseCommand
from django.contrib.auth.models import User

from elections.models import ElectionEvent, ElectionInstance, Council
from political_profiles.models import ChanceryProfile

 
class Command(BaseCommand):
    help = 'Adds an electionevent'
    
    def handle(self, *args, **options):
        ee = ElectionEvent.objects.create(
            name='Tweede kamer verkiezingen 2010',
            parent_region='Nederland',
            level='landelijk',
            default_date=datetime.datetime(2010, 6, 9),
            question_due_period=7,
            profile_due_period=7,
            candidate_due_period=30,
            party_due_period=33,
        )
        print "ElectionEvent added with id %d" % ee.pk
        u = User.objects.create(
            username='wiekiesjij',
            email='info@wiekiesjij.nl',
        )
        u.set_password('ikkiesmij')
        cp = ChanceryProfile.objects.create(
            user=u,
            terms_and_conditions=True,
        )
        
        c = Council.objects.create(
            name='Tweede kamer',
            region='Nederland',
            level='landelijk',
            abbreviation='Tweede kamer',
            email='info@wiekiesjij.nl',
            street='Nieuwe boteringenstraat',
            house_num='30',
            postcode='9712 PM',
            town='Groningen',
            seats='150',
            website='http://www.tweedekamer.nl/Verkiezingen',
        )
        c.chanceries = [u]
        
        ei = ElectionInstance.objects.create(
            council=c,
            election_event=ee,
            name='Tweedekamer',
            start_date=ee.default_date,
            end_date=ee.default_date,
            wizard_start_date=ee.default_date
        )
