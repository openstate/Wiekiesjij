from django.shortcuts import render_to_response
from django.template import RequestContext
from utils.multipathform import Step, MultiPathFormWizard
from elections.forms import InitialElectionInstanceForm,InitialCouncilForm
from elections.functions import get_profile_forms

class AddElectionInstanceWizard(MultiPathFormWizard):
    """
        Wizard for adding an election instance and council
    """
    def __init__(self, *args, **kwargs):
        step1_forms = dict(
            initial_ei=InitialElectionInstanceForm,
        )
        idx = 0;
        for profile_form in get_profile_forms('council_admin', 'invite'):
            step1_forms.update({'invite_contact_%s' % idx : profile_form})
            idx += 1
        step1 = Step('electioninstance', 
            forms=step1_forms,
            template='backoffice/wizard/addelection/base.html',
        )
        template = 'backoffice/wizard/addelection/base.html',
        super(AddElectionInstanceWizard, self).__init__(step1, template)
        
    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0
        
    def done(self, request, form_dict):
        # This needs to be easier !?!
        for path, forms in form_dict.iteritems():
            for name, form in forms.iteritems():
                if name == 'initial_ei':
                    #create election instance 
                    import ipdb; ipdb.set_trace()
                    #ei = ElectionInstance.objects.create(form.cleaned_data)
                    pass
                else:
                    import ipdb; ipdb.set_trace()
                    # Gather data from all other forms to create the council and admin
                    pass
        
        return render_to_response('backoffice/wizard/addelection/done.html', {}, contact_instance=RequestContext(request))