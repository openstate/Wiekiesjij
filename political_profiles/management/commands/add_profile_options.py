from django.core.management import BaseCommand
from django.utils.translation import ugettext as _
from political_profiles.models import ConnectionType, WorkExperienceSector, PoliticalExperienceType, EducationLevel
 
class Command(BaseCommand):
    help = 'Adds Levels For Education, sectors for work experience and type for politial experience'
    
    def handle(self, *args, **options):
        wes = WorkExperienceSector.objects.create(
            sector='In de politiek/het openbaar bestuur',
          )
        print "WorkExperienceSector added with id %d" % wes.pk
        wes = WorkExperienceSector.objects.create(
            sector='Bij de overheid',
          )
        print "WorkExperienceSector added with id %d" % wes.pk
        wes = WorkExperienceSector.objects.create(
            sector='Bij een non-profit organisatie',
        )
        print "WorkExperienceSector added with id %d" % wes.pk
        wes = WorkExperienceSector.objects.create(
            sector='In de zorg',
          )
        print "WorkExperienceSector added with id %d" % wes.pk
        wes = WorkExperienceSector.objects.create(
            sector='In het onderwijs',
          )
        print "WorkExperienceSector added with id %d" % wes.pk
        wes = WorkExperienceSector.objects.create(
            sector='In de dienstverlening',
          )
        print "WorkExperienceSector added with id %d" % wes.pk
        wes = WorkExperienceSector.objects.create(
            sector='In het bedrijfsleven',
          )
        print "WorkExperienceSector added with id %d" % wes.pk
        wes = WorkExperienceSector.objects.create(
            sector='In de landbouw',
          )
        print "WorkExperienceSector added with id %d" % wes.pk
        wes = WorkExperienceSector.objects.create(
            sector='Als zelfstandig ondernemer',
          )
        print "WorkExperienceSector added with id %d" % wes.pk
        wes = WorkExperienceSector.objects.create(
            sector='In het buitenland',
          )
        print "WorkExperienceSector added with id %d" % wes.pk
        wes = WorkExperienceSector.objects.create(
            sector='Geen ervaring',
          )
        print "WorkExperienceSector added with id %d" % wes.pk
        pet = PoliticalExperienceType.objects.create(
            type='Partij',
          )
        print "PoliticalExperienceType added with id %d" % pet.pk
        pet = PoliticalExperienceType.objects.create(
            type='Politieke Vereniging',
          )
        print "PoliticalExperienceType added with id %d" % pet.pk
        pet = PoliticalExperienceType.objects.create(
            type='Politieke Jongerenorganisatie',
          )
        print "PoliticalExperienceType added with id %d" % pet.pk
        pet = PoliticalExperienceType.objects.create(
            type='Overig',
          )
        print "PoliticalExperienceType added with id %d" % pet.pk
        pet = PoliticalExperienceType.objects.create(
            type='Gemeente',
          )
        print "PoliticalExperienceType added with id %d" % pet.pk
        pet = PoliticalExperienceType.objects.create(
            type='Waterschap',
          )
        print "PoliticalExperienceType added with id %d" % pet.pk
        pet = PoliticalExperienceType.objects.create(
            type='Provincie',
          )
        print "PoliticalExperienceType added with id %d" % pet.pk
        pet = PoliticalExperienceType.objects.create(
            type='Tweede Kamer',
          )
        print "PoliticalExperienceType added with id %d" % pet.pk
        pet = PoliticalExperienceType.objects.create(
            type='Eerste Kamer',
          )
        print "PoliticalExperienceType added with id %d" % pet.pk
        pet = PoliticalExperienceType.objects.create(
            type='Europese Unie',
          )
        print "PoliticalExperienceType added with id %d" % pet.pk
        pet = PoliticalExperienceType.objects.create(
            type='Verdragsorganisatie',
          )
        print "PoliticalExperienceType added with id %d" % pet.pk
        pet = PoliticalExperienceType.objects.create(
            type='Lobby',
          )
        print "PoliticalExperienceType added with id %d" % pet.pk

        el = EducationLevel.objects.create(
            level='VMBO',
          )
        print "EducationLevel added with id %d" % el.pk
        el = EducationLevel.objects.create(
            level='Mavo',
          )
        print "EducationLevel added with id %d" % el.pk
        el = EducationLevel.objects.create(
            level='Havo',
          )
        print "EducationLevel added with id %d" % el.pk
        el = EducationLevel.objects.create(
            level='VWO',
          )
        print "EducationLevel added with id %d" % el.pk
        el = EducationLevel.objects.create(
            level='MBO',
          )
        print "EducationLevel added with id %d" % el.pk
        el = EducationLevel.objects.create(
            level='HBO',
          )
        print "EducationLevel added with id %d" % el.pk
        el = EducationLevel.objects.create(
            level='Universitair',
          )
        print "EducationLevel added with id %d" % el.pk


        ct =ConnectionType.objects.create(
            type='Website',
          )
        print "ConnectionType added with id %d" % ct.pk
        ct =ConnectionType.objects.create(
            type='Weblog',
          )
        print "ConnectionType added with id %d" % ct.pk
        ct =ConnectionType.objects.create(
            type='Linkedin',
          )
        print "ConnectionType added with id %d" % ct.pk

        ct =ConnectionType.objects.create(
            type='Hyves',
          )
        print "ConnectionType added with id %d" % ct.pk

        ct =ConnectionType.objects.create(
            type='Facebook',
          )
        print "ConnectionType added with id %d" % ct.pk

        ct =ConnectionType.objects.create(
            type='Twitter',
          )
        print "ConnectionType added with id %d" % ct.pk

        ct =ConnectionType.objects.create(
            type='RSS',
          )
        print "ConnectionType added with id %d" % ct.pk

        ct =ConnectionType.objects.create(
            type='MySpace',
          )
        print "ConnectionType added with id %d" % ct.pk

        ct =ConnectionType.objects.create(
            type='Netlog',
          )
        print "ConnectionType added with id %d" % ct.pk

        ct =ConnectionType.objects.create(
            type='Flickr',
          )
        print "ConnectionType added with id %d" % ct.pk

        ct =ConnectionType.objects.create(
            type='Plaxo',
          )
        print "ConnectionType added with id %d" % ct.pk

        ct =ConnectionType.objects.create(
            type='Article',
          )
        print "ConnectionType added with id %d" % ct.pk


