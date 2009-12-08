from django.core.management import BaseCommand

from elections.models import ElectionInstanceModule
 
class Command(BaseCommand):
    help = 'Adds modules for the election instances'
    
    def handle(self, *args, **options):
        eim, created = ElectionInstanceModule.objects.get_or_create(
            name='SMS Module',
            slug='SMS',
        )
        if created:
            print "Module added: %s" % eim.name
        else:
            print "Module exists: %s" % eim.name
