from django.db import transaction
from django.shortcuts import redirect

from utils.multipathform import Step, MultiPathFormWizard

from invitations.models import Invitation

from elections.forms import InitialElectionPartyForm, ElectionPartyContactForm, ElectionPartyAdditionalForm, ElectionPartyDescriptionForm
from elections.functions import get_profile_forms, create_profile, profile_invite_email_templates

from elections.models import Party, ElectionInstanceParty


class AddElectionPartyWizard(MultiPathFormWizard):
    def __init__(self, instance, position, *args, **kwargs):
        self.election_instance = instance
        step1_forms = dict(
            initial_ep=InitialElectionPartyForm,
        )
        self.position = position
        idx = 0;
        for profile_form in get_profile_forms('party_admin', 'invite'):
            step1_forms.update({'invite_contact_%s' % idx : profile_form})
            idx += 1
        step1 = Step('electionparty', 
            forms=step1_forms,
            template='backoffice/wizard/addelectionparty/step1.html',
            initial={'initial_ep': {'position': position}},
        )
        #default template is the base, each step can override it as needed (for buttons)
        template = 'backoffice/wizard/addelectionparty/base.html',
        super(AddElectionPartyWizard, self).__init__(step1, template, *args, **kwargs)
        
    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0
        
    @transaction.commit_manually
    def done(self, request, form_dict):
        try:
            for path, forms in form_dict.iteritems():
                for name, form in forms.iteritems():
                    if name == 'initial_ep':
                        #create election instance
                        self.ep_data = form.cleaned_data
                    else:
                        if not hasattr(self, 'profile_data'):
                            self.profile_data = {}
                        cleaned_data = form.cleaned_data
                        for key, value in cleaned_data['name'].iteritems():
                            cleaned_data[key] = value
                        del cleaned_data['name']
                        self.profile_data.update(cleaned_data)

            party = Party.objects.create(
                region = self.election_instance.council.region,
                level = self.election_instance.council.level,
                name = self.ep_data['name'],
                abbreviation = self.ep_data['abbreviation'])

            eip = ElectionInstanceParty.objects.create(
                party=party,
                election_instance=self.election_instance,
                position=self.ep_data['position'],
                list_length=self.ep_data['list_length'])

            #Create the profile
            created, profile = create_profile('party_admin', self.profile_data)
            #Link the profile to the party
            party.contacts.add(profile.user)

            #Create the invitation
            templates = profile_invite_email_templates('party_admin')
            
            #TODO: change invitation text based on created
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
            return redirect('bo.election_instance_view', id=self.election_instance.id)
        return redirect('bo.election_party_edit', id=eip.id)


class ElectionPartySetupWizard(MultiPathFormWizard):
    def __init__(self, eip, *args, **kwargs):
        self.eip = eip

        step1_forms = dict(
            election_party_contact_form=ElectionPartyContactForm
        )
        step2_forms = dict(
            election_party_additional_form=ElectionPartyAdditionalForm
        )
        step3_forms = dict(
            election_party_description_form=ElectionPartyDescriptionForm
        )

        initial = eip.party.__dict__
        initial.update({'list_length': eip.list_length})
        initial.update({'address': eip.party.address})

        step1 = Step('election_party_contact_form',
                    forms=step1_forms,
                    initial={'election_party_contact_form': initial},
                    template='backoffice/wizard/setupelectionparty/step1.html',)
        step2 = Step('election_party_additional_form',
                    forms=step2_forms,
                    initial={'election_party_additional_form': initial},
                    template='backoffice/wizard/setupelectionparty/step2.html',)
        step3 = Step('election_party_description_form',
                    forms=step3_forms,
                    initial={'election_party_description_form': initial},
                    template='backoffice/wizard/setupelectionparty/step3.html',)
        template = 'backoffice/wizard/election_party_setup/base.html',
        super(ElectionPartySetupWizard, self).__init__(step1.next(step2.next(step3)), template, *args, **kwargs)

    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0

    def done(self, request, form_dict):
        data = {}
        for path, forms in form_dict.iteritems():
            for name, form in forms.iteritems():
                data.update(form.cleaned_data)
                
        self.eip.party.name = data['name']
        self.eip.party.abbreviation = data['abbreviation']
        self.eip.party.address_street = data['address']['street']
        self.eip.party.address_number = data['address']['number']
        self.eip.party.address_postalcode = data['address']['postalcode']
        self.eip.party.address_city = data['address']['city']
        self.eip.party.telephone = data['telephone']
        self.eip.party.email = data['email']
        self.eip.party.website = data['website']
        self.eip.party.slogan = data['slogan']
        self.eip.party.num_seats = data['num_seats']
        #self.eip.party.logo = data['logo']
        self.eip.party.description = data['description']
        self.eip.party.history = data['history']
        self.eip.party.manifesto = data['manifesto']
        self.eip.party.save()

        self.eip.list_length = int(data['list_length'])
        self.eip.save()

        return redirect('bo.election_instance_view', self.eip.election_instance.id)

