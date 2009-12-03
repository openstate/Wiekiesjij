from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from utils.multipathform import MultiPathFormWizard, Step

# Even though your IDE might say this is an unused import, please do not remove the following Form imports
from political_profiles.forms import *

def form_view(request, profile_type):
    try:
        formslist = dict(
            generic_form = globals()[profile_type],
        )
    except KeyError:
        raise NameError(profile_type + ' is not an existing form')


    step_args = dict(
        forms = formslist,
    )

    steps = Step('add_election_instance', forms=step_args['forms'], template='backoffice/wizard/step1.html')
    politician_profile_wizard = MultiPathFormWizard(steps)

    return politician_profile_wizard(request)