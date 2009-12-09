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

class CouncilEditWizard(MultiPathFormWizard):
    """
    Wizard to update Council profile information.

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
                e = Exception
                raise Exception
        except Exception, e:
            raise e

        # Updates Council contact information
        step1 = Step('council_contact_information',
                     forms={'council_contact_information': CouncilContactInformationForm},
                     template='backoffice/wizard/council/edit/step1.html',
                     initial={'council_contact_information': self.election_instance.council})
        # Updates Council additional information
        step2 = Step('council_additional_information',
                     forms={'council_additional_information': CouncilForm},
                     template='backoffice/wizard/council/edit/step2.html',
                     initial={'council_additional_information': self.election_instance.council})
        # Updates Council styling setup
        step3 = Step('council_styling_setup',
                     forms={'council_styling_setup': CouncilStylingSetupForm},
                     template='backoffice/wizard/council/edit/step3.html',
                     initial={'council_styling_setup': self.election_instance.council})

        scenario_tree = step1.next(step2.next(step3))

        template = 'backoffice/wizard/council/edit/base.html',

        super(self.__class__, self).__init__(scenario_tree, template)

    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0

    @transaction.commit_manually
    def done(self, request, form_dict):
        try:
            for path, forms in form_dict.iteritems():
                for name, form in forms.iteritems():
                    if name in ('council_contact_information', 'council_additional_information', 'council_styling_setup'):
                        # Updates the Council with data from step 1, 2 or 3.
                        if not hasattr(self, 'council_data'):
                            self.council_data = {}
                        # We merge two dictinaries, letting the form data to overwrite the existing data
                        self.council_data = dict(self.council_data.items() + form.cleaned_data.items())
                    else:
                        pass # TODO: throw an error

            # Here we need to update the Council
            for (key, value) in self.council_data.items():
                setattr(self.election_instance.council, key, value)

            self.election_instance.council.save(force_update=True) # Updating the Council
        except Exception, e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()

        if request.POST.get('next', 'overview') == 'overview':
            return redirect(reverse('backoffice.council_edit_done'))
        raise NotImplementedError('Implement a redirect to the council edit wizard here.')