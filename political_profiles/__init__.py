from political_profiles.models import PoliticianProfile, ChanceryProfile, ContactProfile, VisitorProfile

model_map = {
    'candidate': PoliticianProfile,
    'visitor': VisitorProfile,
    'council_admin': ChanceryProfile,
    'party_admin':  ContactProfile,
}

def get_profile_model(for_function):
    """
        Get the profile model to use for the specific function within the election system
    """
    return model_map[for_function]
    
def get_profile_forms(for_function, type):
    """
        Get a list of forms to use for the <type> action
    """
    return model_map[for_function].get_forms(type)