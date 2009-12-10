import datetime

from django.core.management import BaseCommand

from invitations.models import Invitation
 
class Command(BaseCommand):
    help = 'Used to send pending invitations'
    
    def handle(self, *args, **options):
        #get at max 50 rows from the database
        invitations = Invitation.objects.filter(accepted=False, send_on=None).order_by('created')[:50]
        invitations_temp = list(invitations)
        #stores ids in a variable from invitations
        invitation_ids = invitations.values_list('id', flat=True)

        #updates all rows with the selected id's in the _database_
        Invitation.objects.filter(id__in=invitation_ids).update(send_on=datetime.datetime.min)

        for invite in invitations_temp:
            invite.send()
            invite.send_on = datetime.datetime.now()
            invite.save()
