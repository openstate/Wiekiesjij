import datetime

from django.db import transaction
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse

from utils.multipathform import Step, MultiPathFormWizard

from elections import settings
from elections.functions import get_profile_forms, create_profile, profile_invite_email_templates, get_profile_model
from elections.forms import InitialElectionInstanceForm, EditElectionInstanceForm
from elections.forms import ElectionInstanceForm, ElectionInstanceSelectPartiesForm
from elections.forms import CouncilForm, CouncilStylingSetupForm, CouncilContactInformationForm
from elections.models import ElectionInstance, Council, ElectionEvent
from invitations.models import Invitation


from utils.graphformwizard import GraphFormWizard
from utils.graphformwizard import Step as GStep
from django.http import Http404, HttpResponseRedirect



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
                num_lists=self.ei_data['num_lists'],
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
            Invitation.create(
                user_from=request.user, 
                user_to=profile.user,
                view='',
                text='Invitation text',
                subject='Invitation',
                html_template=templates['html'],
                plain_template=templates['plain'],
                )
            
        except Exception:
            transaction.rollback()
            raise
        else:
            transaction.commit()
        
        if request.POST.get('next', 'overview') == 'overview':
            return redirect('backoffice.election_event')
        return redirect('backoffice.edit_council', id=ei.id)

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
            ei.num_lists=self.ei_data['num_lists']
            ei.name=self.ei_data['name']
            ei.save()
        
            ei.modules = []
            ei.modules = self.ei_data['modules']
            
            
        except Exception:
            transaction.rollback()
            raise
        
        else:
            transaction.commit()
        
        if request.POST.get('next', 'overview') == 'overview':
            return redirect('backoffice.election_event')
        raise NotImplementedError('Implement a redirect to the council edit wizard here.')
        




class ElectionSetupWizard(GraphFormWizard):

    fast_actions = frozenset(['init'])

    # wizard scenario
    scenario = GStep("chancery_registration", title = "Welcome Chancellery!") \
                .forms(dict( [ ('chancery_registration%d' % idx, cls) for idx, cls in enumerate(get_profile_forms('council_admin', 'edit'))] )) \
                .next('election_details') \
                .form('election_details1', ElectionInstanceForm) \
                .next('council_contact_information') \
                .form('council_contact_information1', CouncilContactInformationForm) \
                .next('council_additional_information') \
                .form('council_additional_information1', CouncilForm) \
                .next('chancery_contact_information') \
                .forms(dict( [ ('chancery_contact_information%d' % idx, cls) for idx, cls in enumerate(get_profile_forms('council_admin', 'contact_information'))] )) \
                .next('council_styling_setup') \
                .form('council_styling_setup', CouncilStylingSetupForm) \
                .next('election_select_parties') \
                .form('election_select_parties', ElectionInstanceSelectPartiesForm)


    def __init__(self, name = None, template = 'backoffice/wizard/election_setup/base.html'):
        super(type(self), self).__init__(name, template)


    def done(self, request, wizard_data, meta, *args, **kwargs):
        print wizard_data
        return None


    def wizard_fast_action(self, request, action, step, step_path, url_step, url_action, *args, **kwargs):
        """Loads correct models"""

        if action == "init":
            if 'election_instance_id' not in kwargs:
                raise

            user_id = kwargs['user_id'] if 'user_id' in kwargs else request.user.id
            election_instance_id = kwargs['election_instance_id']

            # Checking if user really exists and if election_instanc exists. Getting those and passing it to the wizard.
            election_instance = get_object_or_404(ElectionInstance, id = election_instance_id)
            user = get_object_or_404(User, id = user_id)

            ChanceryProfileClass = get_profile_model('council_admin')
            if user.profile.__class__ is not ChanceryProfileClass:
                raise HttpResponseForbidden("Wrong user profile")

            # reload data
            data = {}

            # step 1 data
            stepdata = {}
            for (idx, profile_form) in enumerate(get_profile_forms('council_admin', 'edit')):
                form = GStep.new_form(form = profile_form, initial = user.profile)
                stepdata['chancery_registration%s' % idx] = getattr(form, 'cleaned_data', {})
            
            data['chancery_registration'] = stepdata

            # step 2 data
            form = GStep.new_form(form = ElectionInstanceForm, initial = election_instance)
            data['election_details'] = {'election_details' : getattr(form, 'cleaned_data', {})}

            # step 3 data
            form = GStep.new_form(form = CouncilContactInformationForm, initial = election_instance.council.__dict__)
            data['council_contact_information'] = {'council_contact_information': getattr(form, 'cleaned_data', {})}
            
            # step 4 data
            form = GStep.new_form(form = CouncilForm, initial = election_instance.council)
            data['council_additional_information'] = {'council_additional_information': getattr(form, 'cleaned_data', {})}

            # step 5 data
            stepdata = {}
            for (idx, profile_form) in enumerate(get_profile_forms('council_admin', 'contact_information')):
                form = GStep.new_form(form = profile_form, initial = user.profile)
                stepdata['chancery_contact_information%s' % idx] = getattr(form, 'cleaned_data', {})

            data['chancery_contact_information'] = stepdata

            # step 6 data
            form = GStep.new_form(form = CouncilStylingSetupForm, initial = election_instance.council)
            data['council_styling_setup'] = {'council_styling_setup': getattr(form, 'cleaned_data', {})}

            # step 7 data
            form = GStep.new_form(form = ElectionInstanceSelectPartiesForm, initial = election_instance.parties.all())
            data['election_select_parties'] = {'election_select_parties': getattr(form, 'cleaned_data', {})}

            # store instances, we will use it in done()
            meta = {
                'user_id': user.id,
                'election_instance_id': election_instance.id,
            }
            # store data
            self.save_data(request, data, meta, *args, **kwargs)

            return HttpResponseRedirect(reverse(url_step[0], args = url_step[1], kwargs=dict(url_step[2], path = '')))

        # end of init
        raise Http404
    


#TODO: use profile_form function for the forms !
class ElectionSetupWizard2(MultiPathFormWizard):
    """
    Steps 2.1.5 - 2.6 of interaction design.

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
            self.chancery_profile = self.user.profile
            ChanceryProfileClass = get_profile_model('council_admin')
            if ChanceryProfileClass.__name__ != self.user.profile.__class__.__name__:
                raise Exception
        except Exception, e:
            raise e

        '''
        Loading forms and models from other applications.
        '''
        try:
            ChanceryProfileForm = get_profile_forms('council_admin', 'edit')[0]
            ChanceryContactInformationForm = get_profile_forms('council_admin', 'contact_information')[0]
        except Exception, e:
            raise e

        '''
        TODO for checkboxes we need to populate the data properly, because now it doesn't happen.
        '''
        step1_forms = {}
        step1_initial = {}
         # Get the form(s) for chancery profile and add them to step1_forms
        idx = 0
        for profile_form in get_profile_forms('council_admin', 'edit'):
            step1_forms.update({'chancery_registration%s' % idx : profile_form})
            step1_initial.update({'chancery_registration%s' % idx : self.chancery_profile})
            idx += 1

        step5_forms = {}
        step5_initial = {}
         # Get the form(s) for chancery profile and add them to step5_forms
        idx = 0
        for profile_form in get_profile_forms('council_admin', 'contact_information'):
            step5_forms.update({'chancery_contact_information%s' % idx : profile_form})
            step5_initial.update({'chancery_contact_information%s' % idx : self.chancery_profile})
            idx += 1

        # Updates ChanceryProfile
        step1 = Step('chancery_registration',
                     forms=step1_forms,
                     template='backoffice/wizard/election_setup/step1.html',
                     initial=step1_initial)
        # Updates ElectionInstance
        step2 = Step('election_details',
                     forms={'election_details': ElectionInstanceForm},
                     template='backoffice/wizard/election_setup/step2.html',
                     initial={'election_details': self.election_instance})
        # Updates Council
        step3 = Step('council_contact_information',
                     forms={'council_contact_information': CouncilContactInformationForm},
                     template='backoffice/wizard/election_setup/step3.html',
                     initial={'council_contact_information': self.election_instance.council.__dict__})
        # Updates Council
        step4 = Step('council_additional_information',
                     forms={'council_additional_information': CouncilForm},
                     template='backoffice/wizard/election_setup/step4.html',
                     initial={'council_additional_information': self.election_instance.council})
        # Updates ChanceryProfile
        step5 = Step('chancery_contact_information',
                     forms=step5_forms,
                     template='backoffice/wizard/election_setup/step5.html',
                     initial=step5_initial)
        # Updates Council
        step6 = Step('council_styling_setup',
                     forms={'council_styling_setup': CouncilStylingSetupForm},
                     template='backoffice/wizard/election_setup/step6.html',
                     initial={'council_styling_setup': self.election_instance.council})
        # Updates ElectionInstance
        step7 = Step('election_select_parties',
                     forms={'election_select_parties': ElectionInstanceSelectPartiesForm},
                     template='backoffice/wizard/election_setup/step7.html',
                     initial={'election_select_parties': self.election_instance.parties.all()})

        scenario_tree = step1.next(step2.next(step3.next(step4.next(step5.next(step6.next(step7))))))

        template = 'backoffice/wizard/election_setup/base.html',
        super(self.__class__, self).__init__(scenario_tree, template)

    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0

    @transaction.commit_manually
    def done(self, request, form_dict):
        try:
            for path, forms in form_dict.iteritems():
                for name, form in forms.iteritems():
                    if 'chancery_registration' in name or 'chancery_contact_information' in name:
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
                    elif name in ('election_details',):
                        # Updates the Election Instance from step 2
                        if not hasattr(self, 'election_instance_data'):
                            self.election_instance_data = {}
                        # We merge two dictinaries, letting the form data to overwrite the existing data
                        self.election_instance_data = dict(self.election_instance_data.items() + form.cleaned_data.items())
                    elif name in ('election_select_parties',):
                        # Updates the Election Instance from step 7.
                        if not hasattr(self, 'election_instance_parties_data'):
                            self.election_instance_parties_data = {}
                        # We merge two dictinaries, letting the form data to overwrite the existing data
                        self.election_instance_parties_data = dict(self.election_instance_parties_data.items() + form.cleaned_data.items())
                    else:
                        pass # TODO: throw an error

            self.chancery_profile_data['workingdays'] = ','.join(map(lambda x: str(x), self.chancery_profile_data['workingdays']))

            # Here we need to update the ChanceryProfile
            for (key, value) in self.chancery_profile_data.items():
                setattr(self.chancery_profile, key, value)

            self.chancery_profile.save(force_update=True) # Updating the ChanceryProfile

            # Here we need to update the Council
            for (key, value) in self.council_data.items():
                setattr(self.election_instance.council, key, value)

            self.election_instance.council.save(force_update=True) # Updating the Council

            # Here we need to update the ElectionInstance
            for (key, value) in self.election_instance_data.items():
                setattr(self.election_instance, key, value)

            self.election_instance.save(force_update=True) # Updating the ElectionInstance

            # Now we add all parties to the list
            map(lambda x: self.election_instance.add_party(x), self.election_instance_parties_data['parties'])

        except Exception, e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()

        if request.POST.get('next', 'overview') == 'overview':
            return redirect(reverse('backoffice.election_setup_done'))
        raise NotImplementedError('Implement a redirect to the council edit wizard here.')