import datetime

from django.core.management.base import LabelCommand

from invitations.models import Invitation
 
class Command(LabelCommand):
    help = 'Used to send pending invitations'
    args = "[profile_type]"
    label = 'profile_type'
    
    def handle_label(self, profile_type, *args, **options):
        #get at max 5 rows from the database
        invitations = Invitation.objects.filter(type=profile_type, accepted=False, send_on=None).order_by('created')[:4]
        invitations_temp = list(invitations)
        #stores ids in a variable from invitations
        invitation_ids = [x.pk for x in invitations_temp]

        #updates all rows with the selected id's in the _database_
        Invitation.objects.filter(id__in=invitation_ids).update(send_on=datetime.datetime.min)

        for invite in invitations_temp:
            invite.send()
            invite.send_on = datetime.datetime.now()
            invite.save()
            
        print "Done"
