from django.core.management import BaseCommand
from sms.functions import credit_left

class Command(BaseCommand):
    help='Sends warnings if credit is less than 500 for each election instance. and one global omount for accepte'
    def handle(self, *args, **options):
        credit_left()