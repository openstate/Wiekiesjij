import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from utils.multipathform import Step, MultiPathFormWizard

from elections import settings

from elections.forms import InitialElectionInstanceForm,InitialCouncilForm, ElectionInstanceForm, CouncilForm
from elections.forms import CouncilContactInformationForm

from elections.functions import get_profile_forms, create_profile
from elections.models import ElectionInstance, Council, ElectionEvent

from political_profiles.models import ChanceryProfile
from political_profiles.forms import ChanceryProfileForm

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
            template='backoffice/wizard/addelection/step1.html',
        )
        #default template is the base, each step can override it as needed (for buttons)
        template = 'backoffice/wizard/addelection/base.html',
        super(AddElectionInstanceWizard, self).__init__(step1, template, *args, **kwargs)
        
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
                    if not hasattr(self, 'profile_data'):
                        self.profile_data = {}
                    self.profile_data.update(form.cleaned_data)
        
        
        ee = ElectionEvent.objects.get(pk=settings.ELECTION_EVENT_ID)
        council = Council.objects.create(
            name='Council of %s' % self.ei_data['name'],
            region=self.ei_data['region'],
            level=self.ei_data['level']
        )
        
        ei = ElectionInstance.objects.create(
            name=self.ei_data['name'],
            council=council,
            election_event=ee,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now(),
            wizard_start_date=datetime.datetime.now(),
        )
        #TODO: Save Modules
        create_profile('council_admin', self.profile_data)
        
        #Invite council admin
        # PROBLEM: How do we know what the profile forms returned?
        # PROBLEM: How do we know what object we should create for the profile?
        
        
        return HttpResponseRedirect("%sthankyou/" % (request.path))

class ElectionSetupWizard(MultiPathFormWizard):
    """
        #2.1.5 of interaction design.
    """
    # TODO: Add election_event_id
    def __init__(self, *args, **kwargs):
        step1_forms = dict(
            chancery_profile_form=ChanceryProfileForm,
        )
        step2_forms = dict(
            election_instance=ElectionInstanceForm,
        )
        step3_forms = dict(
            council_contact_information=CouncilContactInformationForm,
        )
        step4_forms = dict(
            council_additional_information=CouncilForm,
        )

        step1 = Step('chancery_registration_1',
                    forms=step1_forms,
                    template='backoffice/wizard/election_setup/step1.html',)
        step2 = Step('chancery_registration_2',
                    forms=step2_forms,
                    template='backoffice/wizard/election_setup/step2.html',)
        step3 = Step('chancery_registration_3',
                     forms=step3_forms,
                     template='backoffice/wizard/election_setup/step3.html',)
        step4 = Step('chancery_registration_4',
                     forms=step4_forms,
                     template='backoffice/wizard/election_setup/step4.html',)
        step5 = Step('chancery_registration_5',
                     forms=step4_forms,
                     template='backoffice/wizard/election_setup/step5.html',)

        scenario_tree = step1.next(
                                   step2.next(
                                              step3.next(
                                                         step4
                                               )))

        template = 'backoffice/wizard/election_setup/base.html',
        super(ElectionSetupWizard, self).__init__(scenario_tree, template)

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

        # council = Council.objects.create(
        #             name='Council of %s' % self.ei_data['name'],
        #             region=self.ei_data['region'],
        #             level=self.ei_data['level']
        #         )
        #
        #         ee = ElectionEvent.objects.all()[0]
        #         ei = ElectionInstance.objects.create(
        #             name=self.ei_data['name'],
        #             council=council,
        #             election_event=ee,
        #             start_date=datetime.datetime.now(),
        #             end_date=datetime.datetime.now(),
        #             wizard_start_date=datetime.datetime.now(),
        #         )

        #Invite council admin

        return HttpResponseRedirect("%sthankyou/" % (request.path))