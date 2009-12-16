from django.core.management import BaseCommand
from django.utils.translation import ugettext as _
from political_profiles.models import ConnectionType, WorkExperienceSector, PoliticalExperienceType, EducationLevel
 
class Command(BaseCommand):
    help = 'Adds Levels For Education, sectors for work experience and type for politial experience'
    
    def handle(self, *args, **options):
        wes = WorkExperienceSector.objects.create(
            sector='IT',
          )
        pet = PoliticalExperienceType.objects.create(
            type='EU',
          )
        el = EducationLevel.objects.create(
            level='MBO',
          )
        ct =ConnectionType.objects.create(
            type='Website',
          )
        print "ConnectionType added with id %d" % ct.pk
        ct =ConnectionType.objects.create(
            type='Blog',
          )
        print "ConnectionType added with id %d" % ct.pk
        ct =ConnectionType.objects.create(
            type='Linkedin',
          )
        print "ConnectionType added with id %d" % ct.pk
        print "WorkExperienceSector added with id %d" % wes.pk
        print "PoliticalExperienceType added with id %d" % pet.pk
        print "EducationLevel added with id %d" % el.pk