from django.core.management import BaseCommand

from political_profiles.models import WorkExperienceSector, PoliticalExperienceType, EducationLevel
 
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
        print "WorkExperienceSector added with id %d" % wes.pk
        print "PoliticalExperienceType added with id %d" % pet.pk
        print "EducationLevel added with id %d" % el.pk