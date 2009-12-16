from elections import settings
from elections.models import ElectionEvent

def election_event(request):
    try:
        return {'election_event': ElectionEvent.objects.get(pk=settings.ELECTION_EVENT_ID)}
    except:
        pass