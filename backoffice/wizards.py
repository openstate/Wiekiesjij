from utils.multipathform import Step, MultiPathFormWizard
from elections.forms import InitialElectionInstanceForm

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
        template = 'backoffice/wizard/addelection/base.html',
        super(AddElectionInstanceWizard, self).__init__(step1, template)
        
    def done(self, request, form_dict):
        print form_dict
        return