import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from utils.multipathform import Step, MultiPathFormWizard
from elections.forms import InitialElectionInstanceForm,InitialCouncilForm
from elections.functions import get_profile_forms

from elections.models import ElectionInstance, Council, ElectionEvent

class AddElectionInstanceWizard(MultiPathFormWizard):
    """
        Wizard for adding an election instance and council
    """
    # TODO: Add election_event_id
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
                    self.ei_data = form.cleaned_data
                else:
                    if not hasattr(self, 'council_data'):
                        self.council_data = {}
                    self.council_data.update(form.cleaned_data)
        
        council = Council.objects.create(
            name='Council of %s' % self.ei_data['name'],
            region=self.ei_data['region'],
            level=self.ei_data['level']
        )
        
        ee = ElectionEvent.objects.all()[0]
        ei = ElectionInstance.objects.create(
            name=self.ei_data['name'],
            council=council,
            election_event=ee,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now(),
            wizard_start_date=datetime.datetime.now(),
        )
        
        #Invite council admin
        
        
        
        return render_to_response('backoffice/wizard/addelection/done.html', {}, context_instance=RequestContext(request))