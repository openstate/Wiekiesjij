from django.db import transaction
from django.shortcuts import redirect

from utils.multipathform import Step, MultiPathFormWizard

from elections.forms import CouncilForm, CouncilStylingSetupForm, CouncilContactInformationForm

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
    def __init__(self, election_instance, *args, **kwargs):
        self.election_instance = election_instance

        # Updates Council contact information
        step1 = Step('council_contact_information',
                     forms={'council_contact_information': CouncilContactInformationForm},
                     template='backoffice/wizard/council/edit/step1.html',
                     initial={'council_contact_information': {'name': self.election_instance.council.name,
                                                               'address': {'street': self.election_instance.council.street,
                                                                            'number': self.election_instance.council.house_num,
                                                                            'postalcode': self.election_instance.council.postcode,
                                                                            'city': self.election_instance.council.town,
                                                                           },
                                                                'website': self.election_instance.council.website,}})
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
                        self.council_data.update(form.cleaned_data)
                        
            # Here we need to update the Council
            for (key, value) in self.council_data.items():
                if key == 'address':
                    self.election_instance.council.street = value['street']
                    self.election_instance.council.house_num = value['number']
                    self.election_instance.council.postcode = value['postalcode']
                    self.election_instance.council.town = value['city']
                else:
                    setattr(self.election_instance.council, key, value)

            self.election_instance.council.save(force_update=True) # Updating the Council
        except Exception:
            transaction.rollback()
            raise
        else:
            transaction.commit()

        
        return redirect('backoffice.election_instance_view', id=self.election_instance.id)