import datetime

from django.core.management import BaseCommand

from elections.models import ElectionEvent


class Command(BaseCommand):
    help = 'Adds an electionevent'

    def handle(self, *args, **options):
        ee = ElectionEvent.objects.create(
            name='Tweede Kamerverkiezingen 2012',
            parent_region='Nederland',
            level='landelijk',
            default_date=datetime.datetime(2012, 9, 12),
            question_due_period=7,
            profile_due_period=7,
            candidate_due_period=14,
            party_due_period=16,
        )
        print "ElectionEvent added with id %d" % ee.pk

