from django.core.management import BaseCommand
from django.utils.translation import ugettext as _
from political_profiles.models import PoliticianProfile
 
class Command(BaseCommand):
    help = 'Fills the age column for all politicians who have a dateofbirth set'
    
    def handle(self, *args, **options):
        print "This might take a while"
        for pol in PoliticianProfile.objects.filter(dateofbirth__isnull=False, age__isnull=True):
            pol.save()
        print "Done"


