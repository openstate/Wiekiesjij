from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from utils.multipathform import Step, MultiPathFormWizard


from elections.forms import InitialElectionPartyForm, ElectionPartyContactForm, ElectionPartyAdditionalForm, ElectionPartyDescriptionForm
from elections.functions import get_profile_forms

from elections.models import Party, ElectionInstanceParty


class AddElectionPartyWizard(MultiPathFormWizard):
    def __init__(self, instance, position, *args, **kwargs):
        self.election_instance = instance
        step1_forms = dict(
            initial_ep=InitialElectionPartyForm,
        )
        step1_forms['initial_ep'].set_num_lists(instance.num_lists)
        idx = 0;
        for profile_form in get_profile_forms('party_admin', 'invite'):
            step1_forms.update({'invite_contact_%s' % idx : profile_form})
            idx += 1
        step1 = Step('electionparty', 
            forms=step1_forms,
            template='backoffice/wizard/addelectionparty/step1.html',
            initial={'initial_ep': {'position': position}}
        )
        #default template is the base, each step can override it as needed (for buttons)
        template = 'backoffice/wizard/addelectionparty/base.html',
        super(AddElectionPartyWizard, self).__init__(step1, template, *args, **kwargs)
        
    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0
        
    def done(self, request, form_dict):
        # This needs to be easier !?!
        for path, forms in form_dict.iteritems():
            for name, form in forms.iteritems():
                if name == 'initial_ep':
                    #create election instance 
                    self.ep_data = form.cleaned_data
                else:
                    if not hasattr(self, 'invite_data'):
                        self.invite_data = {}
                    self.invite_data.update(form.cleaned_data)

        party = Party.objects.create(
            region = self.election_instance.council.region,
            level = self.election_instance.council.level,
            name = self.ep_data['name'],
            abbreviation = self.ep_data['abbreviation'])
        
        eip = ElectionInstanceParty.objects.create(
            party=party,
            election_instance=self.election_instance,
            position=self.ep_data['position'],
            list_length=10)
        
        #Invite party admin
        
        return HttpResponseRedirect("%sthankyou/" % (request.path))

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
        self.eip.party.email = data['email']
        self.eip.party.website = data['website']
        self.eip.party.slogan = data['slogan']
        #self.eip.party.logo = data['logo']
        #num_seats??
        self.eip.party.description = data['description']
        self.eip.party.history = data['history']
        self.eip.party.manifesto = data['manifesto']
        self.eip.party.save()

        self.eip.list_length = int(data['list_length'])
        self.eip.save()

        return HttpResponseRedirect(reverse('backoffice.election_instance_view', args=[self.eip.election_instance.id]))

