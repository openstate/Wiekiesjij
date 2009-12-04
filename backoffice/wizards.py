from django.shortcuts import render_to_response
from utils.multipathform import Step, MultiPathFormWizard
from elections.forms import InitialElectionInstanceForm,InitialCouncilForm
from django.template import RequestContext

class AddElectionInstanceWizard(MultiPathFormWizard):
    """
        Wizard for adding an election instance
    """
    def __init__(self, *args, **kwargs):
        step1 = Step('electioninstance', 
            forms=dict(
                initial_ei=InitialElectionInstanceForm,
            ),
            template='backoffice/wizard/addelection/step1.html',
        )
        step2 = Step('council', 
            forms=dict(
                initial_council=InitialCouncilForm,
            ),
            template='backoffice/wizard/addelection/step2.html',
        )
        step1.next(step2)
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
                    pass
                elif name == 'initial_counsil':
                    #create council
                    pass
        
        return render_to_response('backoffice/wizard/addelection/done.html', {}, contact_instance=RequestContext(request))