import datetime

from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve


from utils.multipathform import Step, MultiPathFormWizard

from elections import settings
from elections.forms import InitialElectionInstanceForm,InitialCouncilForm, ElectionInstanceForm, CouncilForm, CouncilContactInformationForm, CandidacyForm, CouncilStylingSetupForm, ElectionInstanceSelectPartiesForm, EditElectionInstanceForm
from elections.functions import get_profile_forms, create_profile, profile_invite_email_templates

from elections.models import ElectionInstance, Council, ElectionEvent

from political_profiles.models import ChanceryProfile, PoliticianProfile
from political_profiles.forms import ChanceryProfileForm, ChanceryContactInformationForm

from invitations.models import Invitation

class AddElectionInstanceWizard(MultiPathFormWizard):
    """
        Wizard for adding an election instance and council
    """
    
    def __init__(self, *args, **kwargs):
        step1_forms = dict(
            initial_ei=InitialElectionInstanceForm,
        )
        # Get the form(s) for inviting a council admin and add them to step1_forms
        idx = 0;
        for profile_form in get_profile_forms('council_admin', 'invite'):
            step1_forms.update({'invite_contact_%s' % idx : profile_form})
            idx += 1
        
        #add step1
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
        """
            Called after all steps are done
        """
        try:
            # This needs to be easier !?!
            for path, forms in form_dict.iteritems():
                for name, form in forms.iteritems():
                    if name == 'initial_ei':
                        self.ei_data = form.cleaned_data
                    else:
                        if not hasattr(self, 'profile_data'):
                            self.profile_data = {}
                        cleaned_data = form.cleaned_data
                        for key, value in cleaned_data['name'].iteritems():
                            cleaned_data[key] = value
                        del cleaned_data['name']
                        self.profile_data.update(cleaned_data)
        
            #Get the election event
            ee = ElectionEvent.objects.get(pk=settings.ELECTION_EVENT_ID)
            #Create the council
            council = Council.objects.create(
                name='Council of %s' % self.ei_data['name'],
                region=self.ei_data['region'],
                level=self.ei_data['level']
            )
            #Create the election instance
            ei = ElectionInstance.objects.create(
                name=self.ei_data['name'],
                council=council,
                election_event=ee,
                start_date=datetime.datetime.now(),
                end_date=datetime.datetime.now(),
                wizard_start_date=datetime.datetime.now(),
            )
            #Create the profile
            profile = create_profile('council_admin', self.profile_data)
            #Link the profile to the council
            council.chanceries.add(profile.user)
            
            ei.modules.clear()
            ei.modules = self.ei_data['modules']
            
            #Create the invitation
            templates = profile_invite_email_templates('council_admin')
            invitation = Invitation.create(
                user_from=request.user, 
                user_to=profile.user,
                view='',
                text='Invitation text',
                subject='Invitation',
                html_template=templates['html'],
                plain_template=templates['plain'],
                )
            
        except Exception, e:
            transaction.rollback()
            raise
        else:
            transaction.commit()
        
        if request.POST.get('next', 'overview') == 'overview':
            return redirect('backoffice.election_event')
        raise NotImplementedError('Implement a redirect to the council edit wizard here.')

class EditElectionInstanceWizard(MultiPathFormWizard):
    """
        Wizard for editing an election instance
    """
    
    def __init__(self, election_instance_id, *args, **kwargs):
        self.election_instance_id = election_instance_id
        step1_forms = dict(
            editei=EditElectionInstanceForm,
        )
        
        step1 = Step('editelectioninstance',
            forms=step1_forms,
            initial=dict(
                editei=get_object_or_404(ElectionInstance, id=self.election_instance_id)
            ),
            template='backoffice/wizard/editelection/step1.html',
        )
        #default template is the base, each step can override it as needed (for buttons)
        template = 'backoffice/wizard/editelection/base.html',
        #import ipdb; ipdb.set_trace()
        super(EditElectionInstanceWizard, self).__init__(step1, template, *args, **kwargs)

    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0
    
    @transaction.commit_manually
    def done(self, request, form_dict):
        try:
            # This needs to be easier !?!
            for path, forms in form_dict.iteritems():
                for name, form in forms.iteritems():
                    self.ei_data = form.cleaned_data

        
            ei = ElectionInstance.objects.get(pk=self.election_instance_id)
        
            ei.name=self.ei_data['name']
            ei.save()
        
            ei.modules = []
            ei.modules = self.ei_data['modules']
            
            
        except Exception, e:
            transaction.rollback()
            raise
        
        else:
            transaction.commit()
        
        if request.POST.get('next', 'overview') == 'overview':
            return redirect('backoffice.election_event')
        raise NotImplementedError('Implement a redirect to the council edit wizard here.')
                    
class ElectionSetupWizard(MultiPathFormWizard):
    """
    # 2.1.5 - 2.6 of interaction design.

    We expect to have council, election instance and chancery already created. We need to  "Council ID",
    "Election Instance ID" and "Chancery ID". So we only update them.

    We expect to have "Election Instance ID" and "Chancery ID" passed to the wizard. From "Election Instance" we get
    the "Council". Those ids are to be included in invitation e-mail.

    Those we get as named arguments and process them in __init__().
        @param int user_id --required
        @param int election_instance_id --required

    For the rest behaves like its' parent.
    """
    def __init__(self, *args, **kwargs):
        # Getting "user_id" and "election_instance_id" passed to the Wizard.
        try:
            self.user_id, self.election_instance_id = kwargs['user_id'], kwargs['election_instance_id']

            # Checking if user really exists and if election_instanc exists. Getting those and passing it to the wizard.
            self.election_instance = ElectionInstance.objects.get(id=self.election_instance_id)
            self.user = User.objects.get(id=self.user_id)
            self.chancery_profile = ChanceryProfile.objects.get(user=self.user_id)
        except Exception, e:
            raise e

        '''
        TODO for step "chancery_registration". Prepopulate form data with information stored in model in case if
        chancery already exists.
        '''
        step1_forms = dict(chancery_registration=ChanceryProfileForm,) # Updates ChanceryProfile
        step2_forms = dict(election_details=ElectionInstanceForm,) # Updates ElectionInstance
        step3_forms = dict(council_contact_information=CouncilContactInformationForm,) # Updates Council
        step4_forms = dict(council_additional_information=CouncilForm,) # Updates Council
        step5_forms = dict(chancery_contact_information=ChanceryContactInformationForm,) # Updates ChanceryProfile
        step6_forms = dict(council_styling_setup=CouncilStylingSetupForm,) # Updates Council
        step7_forms = dict(election_select_parties=ElectionInstanceSelectPartiesForm,) # Updates ElectionInstance

        step1 = Step('chancery_registration',
                     forms=step1_forms,
                     template='backoffice/wizard/election_setup/step1.html',
                     initial=self.chancery_profile.__dict__)
        step2 = Step('election_details',
                     forms=step2_forms,
                     template='backoffice/wizard/election_setup/step2.html',
                     initial=self.election_instance.__dict__)
        step3 = Step('council_contact_information',
                     forms=step3_forms,
                     template='backoffice/wizard/election_setup/step3.html',
                     initial=self.election_instance.council.__dict__)
        step4 = Step('council_additional_information',
                     forms=step4_forms,
                     template='backoffice/wizard/election_setup/step4.html',
                     initial=self.election_instance.council.__dict__)
        step5 = Step('chancery_contact_information',
                     forms=step5_forms,
                     template='backoffice/wizard/election_setup/step5.html',
                     initial=self.chancery_profile.__dict__)
        step6 = Step('council_styling_setup',
                     forms=step6_forms,
                     template='backoffice/wizard/election_setup/step6.html',
                     initial=self.election_instance.council.__dict__)
        step7 = Step('election_select_parties',
                     forms=step7_forms,
                     template='backoffice/wizard/election_setup/step7.html',
                     initial=self.election_instance.__dict__)

        scenario_tree = step1.next(step2.next(step3.next(step4.next(step5.next(step6.next(step7))))))

        template = 'backoffice/wizard/election_setup/base.html',

        super(ElectionSetupWizard, self).__init__(scenario_tree, template)

    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0

    @transaction.commit_manually
    def done(self, request, form_dict):
        try:
            # This needs to be easier !?!
            for path, forms in form_dict.iteritems():
                for name, form in forms.iteritems():
                    print name, ': '; print form.cleaned_data.items(), '\n\n'
                    if name in ('chancery_registration', 'chancery_contact_information'):
                        # Updates the ChanceryProfile with data from step 1 or 5.
                        if not hasattr(self, 'chancery_profile_data'):
                            self.chancery_profile_data = {}
                        # We merge two dictinaries, letting the form data to overwrite the existing data
                        self.chancery_profile_data = dict(self.chancery_profile_data.items() + form.cleaned_data.items())
                    elif name in ('council_contact_information', 'council_additional_information', 'council_styling_setup'):
                        # Updates the Council with data from step 3, 4 or 6.
                        if not hasattr(self, 'council_data'):
                            self.council_data = {}
                        # We merge two dictinaries, letting the form data to overwrite the existing data
                        self.council_data = dict(self.council_data.items() + form.cleaned_data.items())
                    elif name in ('election_details', 'election_select_parties'):
                        # Updates the Election Instance from step 2 or 7.
                        if not hasattr(self, 'election_instance_data'):
                            self.election_instance_data = {}
                        # We merge two dictinaries, letting the form data to overwrite the existing data
                        self.election_instance_data = dict(self.election_instance_data.items() + form.cleaned_data.items())
                    else:
                        pass # TODO: throw an error


            self.chancery_profile_data['workingdays'] = ','.join(map(lambda x: str(x), self.chancery_profile_data['workingdays']))
            
            print '\nself.chancery_profile_data: \n', self.chancery_profile_data
            print '\nself.election_instance_data: \n', self.election_instance_data
            print '\nself.council_data: \n', self.council_data

            # Here we need to update the ChanceryProfile
            for (key, value) in self.chancery_profile_data.items():
                setattr(self.chancery_profile, key, value)
                #self.chancery_profile.key = value

            self.chancery_profile.save(force_update=True) # Updating the ChanceryProfile

            # Here we need to update the Council
            for (key, value) in self.council_data.items():
                setattr(self.election_instance.council, key, value)
                #self.election_instance.council.key = value

            self.election_instance.council.save(force_update=True) # Updating the Council
            
            # Here we need to update the ElectionInstance
            for (key, value) in self.election_instance_data.items():
                setattr(self.election_instance, key, value)
                #self.election_instance.key = value

            self.election_instance.save(force_update=True) # Updating the ElectionInstance
        except Exception, e:
            transaction.commit()#transaction.rollback()
            raise e
        else:
            transaction.commit()

        print '\nUpdate data:\n'
        print '\nElection Instance\n', self.election_instance.__dict__
        print '\nCouncil\n', self.election_instance.council.__dict__
        print '\nChanceryProfile\n', self.chancery_profile.__dict__

        print '\n', 'ElectionInstance (from database): ', '\n'
        ei_updated = ElectionInstance.objects.get(id=self.election_instance_id)
        print '\n', ei_updated.__dict__
        print '\n', 'Council (from database): ', '\n'
        print '\n', ei_updated.council.__dict__

        u_updated = ChanceryProfile.objects.get(user=self.user)
        print '\n', 'User (from database): ', '\n'
        print '\n', u_updated.__dict__
        
        if request.POST.get('next', 'overview') == 'overview':
            return redirect('backoffice.election_setup')
        raise NotImplementedError('Implement a redirect to the council edit wizard here.')

class AddCandidateWizard(MultiPathFormWizard):
    """
        Wizard for adding a Candidate
    """

    def __init__(self, *args, **kwargs):
        step1_forms = dict()
        idx = 0;
        for profile_form in get_profile_forms('candidate', 'invite'):
            step1_forms.update({'invite_contact_%s' % idx : profile_form})
            idx += 1
        step1 = Step('candidate',
            forms = step1_forms,
            template = 'backoffice/wizard/addcandidate/step1.html',
        )
        template = 'backoffice/wizard/addcandidate/base.html'
        super(AddCandidateWizard, self).__init__(step1, template)

    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0

    @transaction.commit_manually
    def done(self, request, form_dict):
        try:
            for path, forms in form_dict.iteritems():
                for name, form in forms.iteritems():
                    if name == 'initial_form':
                        self.form_data = form.cleaned_data
                    else:
                        if not hasattr(self, 'form_data'):
                            self.form_data = {}
                        self.form_data.update(form.cleaned_data)

            #TODO: Connect to EI/party

            #Store data
            tmp_data = {
                'first_name': self.form_data['name']['first_name'],
                'middle_name': self.form_data['name']['middle_name'],
                'last_name': self.form_data['name']['first_name'],
                'email': self.form_data['email'],
                'gender': self.form_data['gender'],
            }
            candidate = create_profile('candidate', tmp_data)

            #Create invitation
            templates = profile_invite_email_templates('candidate')
            invitation = Invitation.create(
                user_from = request.user,
                user_to = candidate.user,
                view = '',
                text = 'Invitation text',
                subject = 'Invitation',
                html_template = templates['html'],
                plain_template = templates['plain'],
            )
        except Exception, e:
            transaction.rollback()
            raise
        else:
            transaction.commit()

        #TODO: Make args=[1] dynamic. In addcandidate/step1.html too ('Cancel'-link)

        return HttpResponseRedirect(reverse('backoffice.election_party_view', args=[1]))
                            