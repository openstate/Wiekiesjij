from django.core.management import BaseCommand
from django.utils.translation import ugettext as _
from political_profiles.models import ConnectionType, WorkExperienceSector, PoliticalExperienceType, EducationLevel

class Command(BaseCommand):
    help = 'Adds Levels For Education, sectors for work experience and type for politial experience'

    def handle(self, *args, **options):
        work_sectors = [
            "Als zelfstandig ondernemer",
            "Bij de overheid",
            "Bij een non-profit organisatie",
            "In het bedrijfsleven",
            "In de bouw",
            "In het buitenland",
            "In de landbouw",
            "Bij defensie",
            "In het onderwijs",
            "In de politiek of openbaar bestuur",
            "Bij politie of justitie",
            "In de zorg",
        ]
        for sector in work_sectors:
            wes = WorkExperienceSector.objects.create(
                sector=sector
            )

        pol_sectors = [
            "In de Tweede Kamer",
            "In de Eerste Kamer",
            "Europese Politiek",
            "Provinciale of gemeentelijke politiek",
            "Elders in de politiek",
        ]
        for sector in pol_sectors:
            pet = PoliticalExperienceType.objects.create(
                type=sector,
                )

        ed_level = [
            'VMBO',
            'Mavo',
            'Havo',
            'VWO',
            'MBO',
            'HBO',
            'Universitair',
        ]

        for l in ed_level:
            el = EducationLevel.objects.create(
                level=l,
            )

        c_types = [
            'Website',
            'Weblog',
            'Linkedin',
            'Hyves',
            'Facebook',
            'Twitter',
            'RSS',
            'MySpace',
            'Netlog',
            'Flickr',
            'Plaxo',
        ]

        for c in c_types:
            ct =ConnectionType.objects.create(
                type=c,
            )

