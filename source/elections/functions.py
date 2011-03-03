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
    

def get_popularity(election_instance_id):
    key = 'popu-%s' % (election_instance_id)
    result = cache.get(key)
    if result is None:
        from political_profiles.models import UserStatistics
        from django.conf import settings as stts
        import sys
        
        winsec = 24*60*60 * UserStatistics.view_interval.days + UserStatistics.view_interval.seconds

        if stts.DATABASES['default']['ENGINE'].find('sqlite') != -1:
            pop = """COALESCE((({0} / ({0} + (strftime('%%s', 'now') - strftime('%%s', us.profile_hits_up)))) * us.profile_hits), 0) as pop""".format(winsec)

        elif stts.DATABASES['default']['ENGINE'].find('mysql') != -1:
            pop = """COALESCE((({0} / ({0} + time_to_sec(timediff(now(), us.profile_hits_up)))) * us.profile_hits), 0) as pop""".format(winsec)
            
        else:
            raise Exception('Unsupported database engine. Please add DB specific date-time manipulation code');

        #[FIXME: by taking sum of scores we give to high penalties for people that
        # where not in top 5, but have almost no difference in score with top 5]
        query = """
            SELECT ec.id, p.id as party_id, COUNT(ca.candidates_score) as sum, {0}
            FROM elections_candidacy ec 
            JOIN elections_electioninstanceparty p ON p.id = ec.election_party_instance_id
            LEFT JOIN frontoffice_candidateanswers ca ON ca.candidate_id = ec.candidate_id
            LEFT JOIN political_profiles_userstatistics us ON ec.candidate_id = us.user_id
            WHERE p.election_instance_id = %s
            GROUP BY ec.id, p.id
        """.format(pop)
        
        canresult = []

        pmin, pmax = float(sys.maxint), 0
        smin, smax = sys.maxint, 0
        for row in query_to_dict(query, election_instance_id):
            pop = float(row['pop'])
            pmin, pmax = min(pmin, pop), max(pmax, pop)

            sum = float(row['sum'])
            smin, smax = min(smin, sum), max(smax, sum)
            canresult.append((row['id'], row['party_id'], (sum, pop)))

        # normalized [0..100], floats
        presult = {}
        cand_result = {}

        # with 1 candidate smax == smin
        smin, stot = (smin, smax - smin) if smax > smin else (smin - 1, 1)
        pmin, ptot = (pmin, pmax - pmin) if pmax > pmin else (pmin - 1, 1)
        for (cid, pid, (sum, pop)) in canresult:
            sum = ((sum - smin) / stot) * 100
            pop = ((pop - pmin) / ptot) * 100
            pp = calc_popularity(sum, pop)
            cand_result[cid] = pp
            pcur, pcount = presult.get(pid, (0.0, 0))
            presult[pid] = (pcur + pp, pcount + 1)

        #normalize parties
        #[FIXME: average is really bad statistics! will flat out all peaks (leaders
        # of the parties). Better to compensate it with all values with Z-score > 0.x
        presult = dict(map(lambda (pid, (popsum, count)): (pid, popsum / count), presult.iteritems()))
        pmax, pmin = max(presult.itervalues()), min(presult.itervalues())
        pmin, ptot = (pmin, pmax - pmin) if pmax > pmin else (pmin - 1, 1)
        presult = dict(map(lambda (pid, pop): (pid, ((pop - pmin) / ptot) * 100), presult.iteritems()))

        # cache data
        result = (cand_result, presult)
        cache.set(key, result, 60*60*24) #24 hour cache
    
    return result

def calc_popularity(match, views):
    return int((match * 4 + views) / 5)