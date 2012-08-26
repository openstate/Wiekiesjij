from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Count
from political_profiles.models import ConnectionType, WorkExperienceSector, PoliticalExperienceType, EducationLevel

class Command(BaseCommand):
    help = 'Lists those users who are candidates in multiple different elections'

    def handle(self, *args, **options):
	users = User.objects.annotate(num_elect = Count('elections')).filter(num_elect__gt = 1)
	print "%s users participating in multiple elections" % users.count()
	for u in users:
	    for candidacy in u.elections.select_related('election_party_instance__party').order_by('-id'):
		print u.email, u.profile.last_name, candidacy.id, candidacy.election_party_instance, candidacy.election_party_instance.party

# candidacy = self.user.elections.select_related('election_party_instance__party').order_by('position')
#         if candidacy.count() != 0:
#		return candidacy[0].election_party_instance.party
