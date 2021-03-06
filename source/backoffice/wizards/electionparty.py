import copy

from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext

from elections.forms import InitialElectionPartyForm, ElectionPartyContactForm, ElectionPartyAdditionalForm, ElectionPartyDescriptionForm
from elections.functions import get_profile_forms, create_profile, profile_invite_email_templates
from elections.models import Party, ElectionInstanceParty

from political_profiles.forms import  ContactProfileForm

from utils.exceptions import PermissionDeniedException
from utils.multipathform import Step, MultiPathFormWizard

from invitations.models import Invitation



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
            extra_context={'instance':self.election_instance, }
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
                position=self.ep_data['position'])
                # list_length=self.ep_data['list_length'])

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
                view=reverse('bo.party_contact_wizard', kwargs={'id': eip.pk}),
                text='<p>U bent aangekomen op de beheerderpagina van Wiekiesjij. Om Wiekiesjij gereed te maken voor uw partij volgen er nu een aantal schermen waarin u informatie kunt achterlaten. Wanneer deze informatie is ingevuld zullen we overgaan tot het uitnodigen van de kandidaten van uw partij.</p><p>We beginnen met het instellen van een wachtwoord voor Wiekiesjij door op <strong>Accepteer uitnodiging</strong> te klikken. Heeft u al eens eerder gebruik gemaakt van Wiekiesjij, drukt u dan op <strong>Ik heb al een account</strong>.</p><p>Om het gereedmaken van Wiekiesjij zo gemakkelijk mogelijk te laten verlopen hebben we een snelle start [link] handleiding [/link] beschikbaar gesteld die u kunt raadplegen.</p>',
                subject=ugettext('Invitation Wiekiesjij'),
                html_template=templates['html'],
                plain_template=templates['plain'],
                )

        except:
            transaction.rollback()
            raise
        else:
            transaction.commit()
        
        if request.POST.get('skip', None) is not None:
            return redirect('bo.election_instance_view', id=self.election_instance.id)

        return redirect('bo.election_party_edit', id=eip.id)


class ElectionPartyEditWizard(MultiPathFormWizard):
    def __init__(self, eip, *args, **kwargs):
        self.eip = eip
        self.election_instance = self.eip.election_instance
        step1_forms = dict(
            election_party_contact_form=ElectionPartyContactForm
        )
        step2_forms = dict(
            election_party_additional_form=ElectionPartyAdditionalForm
        )
        step3_forms = dict(
            election_party_description_form=ElectionPartyDescriptionForm
        )
      

        initial = copy.deepcopy(eip.party.__dict__)
        initial.update({'list_length': eip.list_length})
        initial.update({'address': eip.party.address})

        step1 = Step('election_party_contact_form',
                    forms=step1_forms,
                    initial={'election_party_contact_form': initial},
                    template='backoffice/wizard/setupelectionparty/step1.html',
                    extra_context={'instance':self.election_instance, 'eip':self.eip })
        step2 = Step('election_party_additional_form',
                    forms=step2_forms,
                    initial={'election_party_additional_form': initial},
                    template='backoffice/wizard/setupelectionparty/step2.html',
                    extra_context={'instance':self.election_instance, 'eip':self.eip },
                    )
        step3 = Step('election_party_description_form',
                    forms=step3_forms,
                    initial={'election_party_description_form': initial},
                    template='backoffice/wizard/setupelectionparty/step3.html',
                    extra_context={'instance':self.election_instance, 'eip':self.eip })


        template = 'backoffice/wizard/election_party_setup/base.html',
        super(ElectionPartyEditWizard, self).__init__(step1.next(step2.next(step3)), template, *args, **kwargs)

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
        self.eip.party.movie = data['movie']
        self.eip.party.num_seats = data['num_seats']
        self.eip.party.logo = data['logo']
        self.eip.party.description = data['description']
        self.eip.party.history = data['history']
        self.eip.party.manifesto = data['manifesto']

        self.eip.party.manifesto_summary = data['manifesto_summary']
        self.eip.party.save()


        self.eip.list_length = int(data['list_length'])
        self.eip.save()

        return redirect('bo.election_party_view', self.eip.id)

class PartyContactWizard(MultiPathFormWizard):
    def __init__(self, eip_id, user_id, *args, **kwargs):
        self.eip = get_object_or_404(ElectionInstanceParty, pk=eip_id)
        self.election_instance = self.eip.election_instance
        if user_id is None:
            self.user = self.eip.party.contacts.all()[0]
        else:
            self.user = get_object_or_404(self.eip.party.contacts, pk=user_id)
        
        if not self.user.profile or self.user.profile.type != 'party_admin':
            raise PermissionDeniedException('Wrong user profile type')
                        
        workingdays = self.user.profile.workingdays or ''
        self.user_profile_dict = {
            'name': {'first_name': self.user.profile.first_name, 'middle_name': self.user.profile.middle_name, 'last_name': self.user.profile.last_name, },
            'gender': self.user.profile.gender,
            #'picture': self.user.profile.picture,
            'telephone': self.user.profile.telephone,
            'workingdays': workingdays.split(','),
        }
     

        step1_forms = dict(
            party_contact = ContactProfileForm
        )
        step2_forms = dict(
            election_party_contact_form=ElectionPartyContactForm
        )
        step3_forms = dict(
            election_party_additional_form=ElectionPartyAdditionalForm
        )
        step4_forms = dict(
            election_party_description_form=ElectionPartyDescriptionForm
        )

        initial = copy.deepcopy(self.eip.party.__dict__)
        initial.update({'list_length': self.eip.list_length})
        initial.update({'address': self.eip.party.address})

        step1 = Step('party_contact',
                    forms=step1_forms,
                    template='backoffice/wizard/partycontact/step1.html',
                    initial={'party_contact': self.user_profile_dict },
                    extra_context={'instance':self.election_instance, 'eip':self.eip })
        step2 = Step('election_party_contact_form',
                    forms=step2_forms,
                    initial={'election_party_contact_form': initial},
                    template='backoffice/wizard/partycontact/step2.html',
                    extra_context={'instance':self.election_instance, 'eip':self.eip })
        step3 = Step('election_party_additional_form',
                    forms=step3_forms,
                    initial={'election_party_additional_form': initial},
                    template='backoffice/wizard/partycontact/step3.html',
                    extra_context={'instance':self.election_instance, 'eip':self.eip },
                    )
        step4 = Step('election_party_description_form',
                    forms=step4_forms,
                    initial={'election_party_description_form': initial},
                    template='backoffice/wizard/partycontact/step4.html',
                    extra_context={'instance':self.election_instance, 'eip':self.eip })

        template = 'backoffice/wizard/partycontact/base.html',
        super(PartyContactWizard, self).__init__(step1.next(step2.next(step3.next(step4))), template, *args, **kwargs)

    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0

    @transaction.commit_manually
    def done(self, request, form_dict):
        try:
            data = {}
            for path, forms in form_dict.iteritems():
                for name, form in forms.iteritems():
                    if name == 'party_contact':
                        self.user_profile_dict = form.cleaned_data
                    else:
                        data.update(form.cleaned_data)
        
            self.user.profile.first_name = self.user_profile_dict['name']['first_name']
            self.user.profile.middle_name = self.user_profile_dict['name']['middle_name']
            self.user.profile.last_name =  self.user_profile_dict['name']['last_name']
            self.user.profile.gender  = self.user_profile_dict['gender']
            self.user.profile.telephone = self.user_profile_dict['telephone']
            self.user.profile.workingdays = ','.join(map(lambda x: str(x), self.user_profile_dict.get('workingdays', [])))
            #self.user.profile.picture = self.user_profile_dict['email']

            self.user.profile.save(force_update=True) # Updating the ContactsProfile
            
            self.user.save(force_update=True)
            
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
            self.eip.party.movie = data['movie']
            self.eip.party.num_seats = data['num_seats']
            self.eip.party.logo = data['logo']
            self.eip.party.description = data['description']
            self.eip.party.history = data['history']
            self.eip.party.manifesto = data['manifesto']
            self.eip.party.manifesto_summary = data['manifesto_summary']
            self.eip.party.save()
            
            if data['list_length']:
                self.eip.list_length = int(data['list_length'])
            self.eip.save()

        except Exception:
            transaction.rollback()
            raise
        else:
            transaction.commit()

        return redirect('bo.party_contact_wizard_done', self.eip.id)

