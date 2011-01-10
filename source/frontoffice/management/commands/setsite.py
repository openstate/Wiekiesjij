from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--name', '-n', dest='name',
            help='Sets the website name'),
       )
    args = '<domain>'
    help = 'Updates the site with the id specified in the settings to the given domain'
    
    def handle(self, *args, **options):
        domain = args[0]
        name = options.get('name')
        site = Site.objects.get_current()
        site.domain = domain
        if name:
            site.name = name
        site.save()
        print "Updated site"
        