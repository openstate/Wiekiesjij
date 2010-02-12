from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured
from django.core.cache import cache

from elections import settings
from utils.functions import query_to_dict


def get_profile_app():
    """
        Return the profile app that's set to be used
    """
    try:
        package = import_module(settings.PROFILE_APP)
    except ImportError:
        raise ImproperlyConfigured("The PROFILE_APP setting refers to a non-existing package.")
        
    return package

def get_profile_model(for_function):
    """
        Return the profile model for a specific function
        Possible functions are:
        - 'candidate'
        - 'visitor'
        - 'council_admin'
        - 'party_admin'
    """
    return get_profile_app().get_profile_model(for_function)
    
    
def get_profile_forms(for_function, form_type):
    return get_profile_app().get_profile_forms(for_function, form_type)
    
    
def create_profile(for_function, data):
    """
        Creates a profile for the given for_function using the data
    """
    return get_profile_app().create_profile(for_function, data)
    
    
def profile_invite_email_templates(for_function):
    """
        Get the templates to use for sending an invitation
        
        Returns a dict with a plain and a hhtml key pointing to the template files to use
    """
    return get_profile_app().profile_invite_email_templates(for_function)
    
    
def replace_user(original_user, new_user, delete_original=True):
    """
        Function to replace the original_user with the new_user
        Handles all the related profile stuff too
    """
    return get_profile_app().replace_user(original_user, new_user, delete_original)
    
    
def get_profile_template(for_function, type):
    """
        Get the template to use to display a certain profile
        Returns False if not found
    """
    return get_profile_app().get_profile_template(for_function, type)
    
def _make_normalize_function(max_pop, max_sum):
    def f(item):
        ((c_id), (raw_sum, raw_pop)) = item
        new_sum = 100.0
        new_pop = 100.0

        if max_sum != 0:
            new_sum = float((raw_sum * 100) / max_sum)

        if max_pop != 0:
            new_pop = float((raw_pop * 100 / max_pop))

        return ((c_id), (new_sum, new_pop))
    return f
        
def get_popularity(election_instance_id):
    key = 'pop-%s' % (election_instance_id)
    result = cache.get(key)
    if result is None:
        query = """
            SELECT ec.id, SUM(COALESCE(ca.candidates_score, 0)) as sum, (1-COALESCE(us.profile_hits, 1))*100 AS pop
            FROM elections_candidacy ec 
            JOIN elections_electioninstanceparty p ON p.id = ec.election_party_instance_id
            LEFT JOIN frontoffice_candidateanswers ca ON ca.candidate_id = ec.candidate_id
            LEFT JOIN political_profiles_userstatistics us ON ec.candidate_id = us.user_id
            WHERE p.election_instance_id = %s
            GROUP BY ec.id
        """
        result = []
        max_pop = 0
        max_sum = 0
        for row in query_to_dict(query, election_instance_id):
            if max_pop < float(row['pop']):
                max_pop = float(row['pop'])
            if max_sum < int(row['sum']):
                max_sum = int(row['sum'])
            result.append((
                    (row['id']), (int(row['sum']), float(row['pop']))
                ))
            
        f = _make_normalize_function(max_pop, max_sum)
        result = dict(map(f, result))
        
        cache.set(key, result, 60*60*24) #24 hour cache
    
    return result

def calc_popularity(match, views):
    return int((match * 4 + views) / 5)