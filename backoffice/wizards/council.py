import datetime

from django.db import transaction
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse

from utils.multipathform import Step, MultiPathFormWizard

from elections import settings
from elections.functions import get_profile_forms, create_profile, profile_invite_email_templates
from elections.forms import InitialElectionInstanceForm, EditElectionInstanceForm
from elections.forms import ElectionInstanceForm, ElectionInstanceSelectPartiesForm
from elections.forms import CouncilForm, CouncilStylingSetupForm, CouncilContactInformationForm
from elections.models import ElectionInstance, Council, ElectionEvent

class EditCouncilWizard(MultiPathFormWizard):
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
        # Updates ChanceryProfile
        step1 = Step('chancery_registration',
                     forms={'chancery_registration': ChanceryProfileForm},
                     template='backoffice/wizard/election_setup/step1.html',
                     initial={'chancery_registration': self.chancery_profile})
        # Updates ElectionInstance
        step2 = Step('election_details',
                     forms={'election_details': ElectionInstanceForm},
                     template='backoffice/wizard/election_setup/step2.html',
                     initial={'election_details': self.election_instance})
        # Updates Council
        step3 = Step('council_contact_information',
                     forms={'council_contact_information': CouncilContactInformationForm},
                     template='backoffice/wizard/election_setup/step3.html',
                     initial={'council_contact_information': self.election_instance.council})
        # Updates Council
        step4 = Step('council_additional_information',
                     forms={'council_additional_information': CouncilForm},
                     template='backoffice/wizard/election_setup/step4.html',
                     initial={'council_additional_information': self.election_instance.council})
        # Updates ChanceryProfile
        step5 = Step('chancery_contact_information',
                     forms={'chancery_contact_information': ChanceryContactInformationForm},
                     template='backoffice/wizard/election_setup/step5.html',
                     initial={'chancery_contact_information': self.chancery_profile})
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

        super(ElectionSetupWizard, self).__init__(scenario_tree, template)

    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0

    @transaction.commit_manually
    def done(self, request, form_dict):
        try:
            for path, forms in form_dict.iteritems():
                for name, form in forms.iteritems():
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
            transaction.commit()#transaction.rollback()
            raise e
        else:
            transaction.commit()

        if request.POST.get('next', 'overview') == 'overview':
            return redirect(reverse('backoffice.election_setup_done'))
        raise NotImplementedError('Implement a redirect to the council edit wizard here.')