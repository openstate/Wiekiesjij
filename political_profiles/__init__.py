from political_profiles.models import PoliticianProfile, ChanceryProfile, ContactProfile, VisitorProfile
from political_profiles.forms import PoliticianProfileForm, ChanceryProfileForm, ContactProfileForm
from political_profiles.forms import InitialChanceryProfileForm


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
    politician_form_map = {
            'create': [PoliticianProfileForm],
            'edit': [PoliticianProfileForm],
            'invite': [PoliticianProfileForm],
            }
    chancery_form_map = {
            'create': [ChanceryProfileForm],
            'edit': [ChanceryProfileForm],
            'invite': [InitialChanceryProfileForm],
            }
    contact_form_map = {
            'create': [ContactProfileForm],
            'edit': [ContactProfileForm],
            'invite': [ContactProfileForm],
            }

    if model_map[for_function] == PoliticianProfile:
        return politician_form_map[type]
    elif model_map[for_function] == ChanceryProfile:
        return chancery_form_map[type]
    elif model_map[for_function] == ContactProfile:
        return contact_form_map[type]
    
    return []

def get_profile_wizards(for_function, type):
    """
        Get a list of forms to use for the <type> action
    """
    politician_form_wizard_map = {
            #'create': [PoliticianProfileFormWizard],
            #'edit': [PoliticianProfileFormWizard],
            #'invite': [PoliticianProfileFormWizard],
            }
    chancery_form_wizard_map = {
            #'create': [ChanceryProfileFormWizard],
            #'edit': [ChanceryProfileFormWizard],
            #'invite': [ChanceryProfileFormWizard],
            }
    contact_form_wizard_map = {
            #'create': [ContactProfileFormWizard],
            #'edit': [ContactProfileFormWizard],
            #'invite': [ContactProfileFormWizard],
            }

    if model_map[for_function] == PoliticianProfile:
        return politician_form_wizard_map[type]
    elif model_map[for_function] == ChanceryProfile:
        return chancery_form_wizard_map[type]
    elif model_map[for_function] == ContactProfile:
        return contact_form_wizard_map[type]

    return []