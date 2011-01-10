from django.core.management import BaseCommand
from political_profiles.models import ConnectionType, WorkExperienceSector, PoliticalExperienceType, EducationLevel

class Command(BaseCommand):
    help = 'Adds Levels For Education, sectors for work experience and type for politial experience'

    def handle(self, *args, **options):
        work_sectors = [
            "In de bouw",
            "In het buitenland",
            "In de landbouw of visserij",
            "Bij defensie",
            "In het onderwijs",
            "In de politiek of openbaar bestuur",
            "Bij de politie of justitie",
            "In de zorg",
            "Als zelfstandig ondernemer",
            "Bij de overheid",
            "Bij een non-profit organisatie",
            "In het bedrijfsleven",
            "Anders",

        ]
        for sector in work_sectors:
            WorkExperienceSector.objects.create(
                sector=sector
            )

        pol_sectors = [
            "Op landelijk niveau",
            "Op gemeentelijk niveau",
            "Op provinciaal niveau",
            "Op Europees niveau",
        ]
        for sector in pol_sectors:
            PoliticalExperienceType.objects.create(
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
            EducationLevel.objects.create(
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
            ConnectionType.objects.create(
                type=c,
            )

