from elections import settings
from elections.models import ElectionEvent

def election_event(request):
    return {
            'election_event': ElectionEvent.objects.get(pk=settings.ELECTION_EVENT_ID),
            #'election_instane_id': settings.ELECTION_INSTANCE_ID
            }
    
