from django.db import transaction
from django.contrib.auth.models import User

from political_profiles.models import PoliticianProfile, ChanceryProfile, ContactProfile, VisitorProfile
from political_profiles.forms import PoliticianProfileForm, ChanceryProfileForm, ContactProfileForm
from political_profiles.forms import InitialChanceryProfileForm, InitialPoliticianProfileForm, ChanceryContactInformationForm
from political_profiles.forms import InitialContactProfileForm





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
            'invite': [InitialPoliticianProfileForm],
            }
    chancery_form_map = {
            'create': [ChanceryProfileForm],
            'edit': [ChanceryProfileForm],
            'invite': [InitialChanceryProfileForm],
            'contact_information': [ChanceryContactInformationForm]
            }
    contact_form_map = {
            'create': [ContactProfileForm],
            'edit': [ContactProfileForm],
            'invite': [InitialContactProfileForm],
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
    
    
def profile_invite_email_templates(for_function):
    templates = {
        'candidate': {
            'plain': 'political_profiles/emails/invitations/candidate.txt',
            'html': 'political_profiles/emails/invitations/candidate.html',
        },
        'visitor': {
            'plain': 'political_profiles/emails/invitations/visitor.txt',
            'html': 'political_profiles/emails/invitations/visitor.html',
        },
        'council_admin': {
            'plain': 'political_profiles/emails/invitations/council_admin.txt',
            'html': 'political_profiles/emails/invitations/council_admin.html',
        },
        'party_admin': {
            'plain': 'political_profiles/emails/invitations/party_admin.txt',
            'html': 'political_profiles/emails/invitations/party_admin.html',
        },
    }
    return templates[for_function]
    
def create_profile(for_function, data):
    """
        Create and return a profile object (with a linked user)
        Assumes data contains at least an email key
    """
    created = False
    try:
        user = User.objects.get(username=data['email'])
        if user.profile is None or user.profile.type != for_function:
            return (False, None)
    except User.DoesNotExist:
        created = True
        user = User.objects.create(
            username=data['email'],
            email=data['email'],
            is_active=False)
    
    if created:
        del data['email']
        data['user'] = user
        if for_function == 'candidate':
            profile = PoliticianProfile.objects.create(**data)
        elif for_function == 'council_admin':
            profile = ChanceryProfile.objects.create(**data)
        elif for_function == 'party_admin':
            profile = ContactProfile.objects.create(**data)
        elif for_function == 'visitor':
            profile = VisitorProfile.objects.create(**data)
        else:
            raise RuntimeError('%s is unknown' % for_function)
    else:
        profile = user.profile
    return (created, profile)
    
def get_profile_template(for_function, type):
    """
        Get the template for displaying certain profile information
        Returns False if no template is found
    """
    TEMPLATES = {
        'candidate': {
            'backoffice_profile': 'political_profiles/view/backoffice_profile/candidate.html',
        },
        'council_admin': {
            'backoffice_profile': 'political_profiles/view/backoffice_profile/council_admin.html',
        },
        'party_admin': {
            'backoffice_profile': 'political_profiles/view/backoffice_profile/party_admin.html',
        },
        'visitor': {
            'backoffice_profile': 'political_profiles/view/backoffice_profile/visitor.html',
        },
    }
    return TEMPLATES.get(for_function,{}).get(type, False)
   
@transaction.commit_on_success # Will rollback on any exception
def replace_user(original_user, new_user, delete_original=True):
    """
        Replace the original_user with the new user
        Delete the original_user
    """
    #one to one/ many to one relations
    related_fields = original_user._meta.get_all_related_objects()
    for related in related_fields:
        accessor = related.get_accessor_name()
        
        #Skip profile relations
        if accessor.endswith('profile'):
            continue

        relation = getattr(original_user, accessor)
        
        if relation is None:
            continue
            
        for obj in relation.all():
            setattr(obj, related.field.name, new_user)
            obj.save()
           
    #Many to many
    related_fields = original_user._meta.get_all_related_many_to_many_objects()
    for related in related_fields:
        accessor = related.get_accessor_name()

        relation = getattr(original_user, accessor)

        if relation is None:
            continue

        for obj in relation.all():
            manager = getattr(obj, related.field.name)
            manager.remove(original_user)
            manager.add(new_user)
            obj.save()
           
    
    #Delete original
    if delete_original:
        original_user.delete()
    