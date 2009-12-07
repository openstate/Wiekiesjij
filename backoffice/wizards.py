import datetime

from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from utils.multipathform import Step, MultiPathFormWizard
from elections import settings
from elections.forms import InitialElectionInstanceForm,InitialCouncilForm, ElectionInstanceForm, CouncilForm, CouncilContactInformationForm, CandidacyForm, CouncilStylingSetupForm, ElectionInstanceSelectPartiesForm
from elections.functions import get_profile_forms, create_profile
from elections.models import ElectionInstance, Council, ElectionEvent

from political_profiles.models import ChanceryProfile, PoliticianProfile
from political_profiles.forms import ChanceryProfileForm, ChanceryContactInformationForm

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
        
    @transaction.commit_manually
    def done(self, request, form_dict):
        try:
            # This needs to be easier !?!
            for path, forms in form_dict.iteritems():
                for name, form in forms.iteritems():
                    if name == 'initial_ei':
                        #create election instance 
                        self.ei_data = form.cleaned_data
                    else:
                        if not hasattr(self, 'profile_data'):
                            self.profile_data = {}
                        cleaned_data = form.cleaned_data
                        for key, value in cleaned_data['name'].iteritems():
                            cleaned_data[key] = value
                        del cleaned_data['name']
                        self.profile_data.update(cleaned_data)
        
        
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
            profile = create_profile('council_admin', self.profile_data)
            council.chanceries.add(profile.user)
        
            #TODO: Save the enabled modules somewhere
            #TODO: Create the invitation 
        
        except Exception, e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()
        
        if request.POST.get('next', 'overview') == 'overview':
            return redirect('backoffice.election_event')
        raise NotImplementedError('Implement a redirect to the council edit wizard here.')            


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
        step5_forms = dict(
            chancery_contact_information=ChanceryContactInformationForm,
        )
        step6_forms = dict(
            council_styling_setup=CouncilStylingSetupForm,
        )
        step7_forms = dict(
            election_select_parties=ElectionInstanceSelectPartiesForm,
        )

        step1 = Step('chancery_registration',
                    forms=step1_forms,
                    template='backoffice/wizard/election_setup/step1.html',)
        step2 = Step('election_details',
                    forms=step2_forms,
                    template='backoffice/wizard/election_setup/step2.html',)
        step3 = Step('council_contact_information',
                     forms=step3_forms,
                     template='backoffice/wizard/election_setup/step3.html',)
        step4 = Step('council_additional_information',
                     forms=step4_forms,
                     template='backoffice/wizard/election_setup/step4.html',)
        step5 = Step('chancery_contact_information',
                     forms=step5_forms,
                     template='backoffice/wizard/election_setup/step5.html',)
        step6 = Step('council_styling_setup',
                     forms=step6_forms,
                     template='backoffice/wizard/election_setup/step6.html',)
        step7 = Step('election_select_parties',
                     forms=step7_forms,
                     template='backoffice/wizard/election_setup/step7.html',)

        scenario_tree = step1.next(
                                   step2.next(
                                              step3.next(
                                                         step4.next(
                                                                    step5.next(
                                                                               step6.next(
                                                                                          step7
                                                                                          ))))))

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

class AddCandidateWizard(MultiPathFormWizard):
    """
        Wizard for adding a Candidate
    """

    def __init__(self, *args, **kwargs):
        step1_forms = dict(
        )
        idx = 0;
        for profile_form in get_profile_forms('candidate', 'invite'):
            step1_forms.update({'invite_contact_%s' % idx : profile_form})
            idx += 1
        step1 = Step('candidate',
            forms = step1_forms,
            template = 'backoffice/wizard/addcandidate/step1.html',
        )
        template='backoffice/wizard/addcandidate/base.html'
        super(AddCandidateWizard, self).__init__(step1, template)

    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0

    def done(self, request, form_dict):
        for path, forms in form_dict.iteritems():
            for name, form in forms.iteritems():
                if name == 'initial_form':
                    self.form_data = form.cleaned_data
                else:
                    if not hasattr(self, 'form_data'):
                        self.form_data = {}
                    self.form_data.update(form.cleaned_data)

        tmp_data = {
            'first_name': self.form_data['name']['first_name'],
            'middle_name': self.form_data['name']['middle_name'],
            'last_name': self.form_data['name']['first_name'],
            'email': self.form_data['email'],
            'gender': self.form_data['gender'],
        }
        import ipdb; ipdb.set_trace()
        create_profile('candidate', tmp_data)

        #politician = PoliticianProfile.objects.create(
        #    first_name = self.form_data['name']['first_name'],
        #    middle_name = self.form_data['name']['middle_name'],
        #    last_name = self.form_data['name']['last_name'],
        #    email = self.form_data['email'],
        #    gender = self.form_data['gender'],
        #)

        return HttpResponseRedirect("%sthankyou/" % (request.path))