import datetime

from django.core.management import BaseCommand

from invitations.models import Invitation
 
class Command(BaseCommand):
    help = 'Used to send pending invitations'
    
    def handle(self, *args, **options):
        invitations = Invitation.objects.filter(accepted=False, send_on=None).order_by('created')[:50]
        
        #First mark them al as busy being send (to prevent duplication)
        invitations.update(send_on=datetime.datetime.min)
        for invitation in invitations:
            invitation.send()
            invitation.send_on = datetime.datetime.now
            invitation.save()
    
        print "Done sending invitations"
        
        
