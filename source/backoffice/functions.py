from elections.models import ElectionInstance
from utils.exceptions import PermissionDeniedException

def check_permissions(request, id, type):
    """
        Checks propper permissions for the current user:
        
        Type can be one of:
        
        'council_admin' - id is expected to be election_instance_id
        'party_admin' - id to be an election_instance_party
        'candidate' - id to be an election_instance_party
        
        Issue: It would be better to work with objects to prevent the party_id being passed instead of 
        the election_instance_party, now we just have to assume it's ok
    """
    if request.user.is_authenticated():
        if request.user.is_staff:
            return
        if request.user.profile is None:
            raise PermissionDeniedException()
        
        if type == 'council_admin' and request.user.councils.filter(election_instances__pk=id):
            return
        elif type == 'party_admin':
            if request.user.profile.type == 'council_admin' and request.user.councils.filter(election_instances__election_instance_parties__pk=id):
                return
            elif request.user.parties.filter(election_instance_parties__pk=id):
                return
        elif type == 'candidate':
            if request.user.profile.type == 'council_admin' and request.user.councils.filter(election_instances__election_instance_parties__pk=id):
                return
            elif request.user.profile.type == 'party_admin' and request.user.parties.filter(election_instance_parties__pk=id):
                return
            elif request.user.elections.filter(election_party_instance__pk=id):
                return
            
    raise PermissionDeniedException()