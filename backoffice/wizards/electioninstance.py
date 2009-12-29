import datetime

from django.db import transaction
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from utils.exceptions import PermissionDeniedException
from utils.multipathform import Step, MultiPathFormWizard

from elections import settings
from elections.functions import get_profile_forms, create_profile, profile_invite_email_templates, get_profile_model
from elections.forms import InitialElectionInstanceForm, EditElectionInstanceForm
from elections.forms import ElectionInstanceForm, ElectionInstanceSelectPartiesForm
from elections.forms import CouncilForm, CouncilStylingSetupForm, CouncilContactInformationForm
from elections.models import ElectionInstance, Council, ElectionEvent, ElectionInstanceQuestion
from invitations.models import Invitation


from utils.graphformwizard import GraphFormWizard
from utils.graphformwizard import Step as GStep



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
                name=ugettext('Council of %(name)s') % {'name': self.ei_data['name']},
                region=self.ei_data['region'],
                level=self.ei_data['level']
            )
            #Create the election instance
            ei = ElectionInstance.objects.create(
                name=self.ei_data['name'],
                council=council,
                election_event=ee,
                num_lists=1,
                start_date=datetime.datetime.now(),
                end_date=datetime.datetime.now(),
                wizard_start_date=datetime.datetime.now(),
            )
            #Create the profile
            created, profile = create_profile('council_admin', self.profile_data)
            
            #Link the profile to the council
            council.chanceries.add(profile.user)
            
            ei.modules.clear()
            ei.modules = self.ei_data['modules']
            
            
            questionset = self.ei_data['question_set']
            
            if questionset:
                for qsq in questionset.questionsetquestion_set.order_by('position'):
                    ElectionInstanceQuestion.objects.create(
                        election_instance = ei,
                        position = qsq.position,
                        question=qsq.question,
                        locked=True,
                    )
                
            
            #Create the invitation
            templates = profile_invite_email_templates('council_admin')
            
            #TODO: Change invitation text based on created or not
            
            Invitation.create(
                user_from=request.user, 
                user_to=profile.user,
                view=reverse('bo.election_setup', kwargs={'election_instance_id': ei.pk}),
                text="<p>U bent aangekomen op de beheerderpagina van Wiekiesjij. Om Wiekiesjij gereed te maken voor uw verkiezingen volgen er nu een aantal schermen waarin u informatie kunt achterlaten. Wanneer deze informatie is ingevuld zullen we overgaan tot het uitnodigen van de partijen die zullen participeren in deze verkiezingen.</p><p>We beginnen met het instellen van een wachtwoord voor Wiekiesjij door op <strong>Accepteer uitnodiging</strong> te klikken. Heeft u al eens eerder gebruik gemaakt van Wiekiesjij, drukt u dan op <strong>Ik heb al een account</strong>.</p><p>Om het gereedmaken van Wiekiesjij zo gemakkelijk mogelijk te laten verlopen hebben we een snelle start [link]handleiding[/link] beschikbaar gesteld die u kunt raadplegen.</p>",
                subject='Invitation',
                html_template=templates['html'],
                plain_template=templates['plain'],
                )
            
        except Exception:
            transaction.rollback()
            raise
        else:
            transaction.commit()
        
        if request.POST.get('skip', None) is not None:
            return redirect('bo.election_event')
        
        return redirect('bo.edit_council', id=ei.id)

class EditElectionInstanceWizard(MultiPathFormWizard):
    """
        Wizard for editing an election instance
    """
    
    def __init__(self, election_instance_id, *args, **kwargs):
        self.election_instance_id = election_instance_id
        self.election_instance = get_object_or_404(ElectionInstance, id=self.election_instance_id)
        step1_forms = dict(
            editei=EditElectionInstanceForm,
        )
        
        step1 = Step('editelectioninstance',
            forms=step1_forms,
            initial=dict(
                editei=self.election_instance
            ),
            template='backoffice/wizard/editelection/step1.html',
            extra_context={'instance':self.election_instance, }
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
            ei.name=self.ei_data['name']
            ei.save()
        
            ei.modules = []
            ei.modules = self.ei_data['modules']
            
            
        except Exception:
            transaction.rollback()
            raise
        
        else:
            transaction.commit()
        
        if request.POST.get('skip', None) is not None:
            return redirect('bo.election_instance_view', id=ei.id)
        
        return redirect('bo.edit_council', id=ei.id)
        

#[NOTE: to see this wizard in action, url: /wiz/init/1/2
# of course you will need user 1, election instance 2
class ElectionSetupWizard(GraphFormWizard):

    # init action reloads the data
    fast_actions = frozenset(['init'])

    # wizard scenario
    scenario = GStep("chancery_registration", header = _("Welcome Chancellery!"), title = _("Registration")) \
                .forms(dict( [ ('chancery_registration%d' % idx, cls) for idx, cls in enumerate(get_profile_forms('council_admin', 'edit'))] )) \
                .field(help = _("This wizard will lead you through the process of setting up WieKiesJij? for your municipality.")) \
                .field(next_button = _("Proceed to instance setup")) \
                \
                .next('election_details', header = _("Details about this election"), title = _("This Election")) \
                .form('election_details1', ElectionInstanceForm) \
                .field(next_button = _("Proceed to Council Setup")) \
                \
                .next('council_contact_information', header = _("Council contact information"), title = _("The Council")) \
                .form('council_contact_information1', CouncilContactInformationForm) \
                .field(next_button = _("Proceed")) \
                \
                .next('council_additional_information', header = _("Council: additional information"), title = _("More Council")) \
                .form('council_additional_information1', CouncilForm) \
                .field(help = _("You can fill in this information later"), next_button = _("Proceed to Chancellery")) \
                \
                .next('council_styling_setup', header = _("Setup styling"), title=_("Styling")) \
                .form('council_styling_setup', CouncilStylingSetupForm) \
                .field(help = _("On this page you can setup the styling for the WieKiesJij? instance for your council.")) \
                .field(next_button = _("Proceed to Party selection")) \
                \
                .next('election_select_parties', template = 'backoffice/wizard/election_setup/step7.html') \
                .field(header = _("Previous parties"), title = _("Finish")) \
                .field(next_button = _("Finish")) \
                .form('election_select_parties', ElectionInstanceSelectPartiesForm)


    def __init__(self, name = None, template = 'backoffice/wizard/election_setup/_base.html'):
        super(type(self), self).__init__(name, template)


    def done(self, request, wizard_data, meta, *args, **kwargs):
        # OK, I'm to tired to finish this thing
        # The wizard data contains dicts with all the data
        # meta contains user_id and election_instance_id
        # we should save the data here and redirecto "done" location
        print wizard_data
        print meta

        return None


    def wizard_fast_action(self, request, action, step, step_path, url_step, url_action, *args, **kwargs):
        """Loads correct models"""

        if action == "init":
            if 'election_instance_id' not in kwargs:
                raise

            user_id = kwargs['user_id'] if 'user_id' in kwargs else request.user.id
            election_instance_id = kwargs['election_instance_id']

            # Checking if user really exists and if election_instanc exists. Getting those and passing it to the wizard.
            election_instance = get_object_or_404(ElectionInstance, id=election_instance_id)
            user = get_object_or_404(User, id=user_id)

            ChanceryProfileClass = get_profile_model('council_admin')
            if user.profile.__class__ is not ChanceryProfileClass:
                raise HttpResponseForbidden("Wrong user profile")

            # reload data
            data = {}
            # [FIXME: adress field should be prefixed in data, automatic prefixing will not work]
            # will be fixed later

            # step 1 data
            stepdata = {}
            for (idx, profile_form) in enumerate(get_profile_forms('council_admin', 'edit')):
                if idx == 0:            
                    data.update({'chancery_registration': {'chancery_registration%d' % idx: {
                        'name': {
                            'first_name': user.profile.first_name,
                            'last_name': user.profile.last_name,
                            'middle_name': user.profile.middle_name,
                        },
                        'gender': user.profile.gender,
                        'telephone': user.profile.telephone or '',
                        'workingdays': user.profile.workingdays or '',
                    }}})
                    
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

            return redirect(url_step[0], *url_step[1], **dict(url_step[2], path = ''))

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
        self.user_id, self.election_instance_id = kwargs['user_id'], kwargs['election_instance_id']
        
        self.election_instance = get_object_or_404(ElectionInstance, pk=self.election_instance_id)
        self.user = get_object_or_404(self.election_instance.council.chanceries, pk=self.user_id)
        
        if self.user.profile is None or self.user.profile.type != 'council_admin':
            raise PermissionDeniedException('Wrong profile type')
        self.chancery_profile = self.user.profile
        '''
        Loading forms and models from other applications.
        '''
        try:
            ChanceryProfileForm = get_profile_forms('council_admin', 'edit')[0]
            ChanceryContactInformationForm = get_profile_forms('council_admin', 'contact_information')[0]
        except Exception:
            raise

        '''
        TODO for checkboxes we need to populate the data properly, because now it doesn't happen.
        '''
        step1_forms = {}
        step1_initial = {}
         # Get the form(s) for chancery profile and add them to step1_forms
        idx = 0
        for profile_form in get_profile_forms('council_admin', 'edit'):
            step1_forms.update({'chancery_registration%s' % idx : profile_form})
            workingdays = self.chancery_profile.workingdays or ''
            step1_initial.update({'chancery_registration%s' % idx : {
                'name': {
                    'first_name': self.chancery_profile.first_name,
                    'middle_name': self.chancery_profile.middle_name,
                    'last_name': self.chancery_profile.last_name,
                },
                'gender': self.chancery_profile.gender,
                'telephone': self.chancery_profile.telephone,
                'workingdays': workingdays.split(','),
            }})
            idx += 1

        #FIXME:  step5_forms = {}
        #         step5_initial = {}
        #          # Get the form(s) for chancery profile and add them to step5_forms
        #         idx = 0
        #         for profile_form in get_profile_forms('council_admin', 'contact_information'):
        #             step5_forms.update({'chancery_contact_information%s' % idx : profile_form})
        #             step5_initial.update({'chancery_contact_information%s' % idx : {
        #                 'website': self.chancery_profile.website,
        #                 'address': {
        #                     'street': self.chancery_profile.street,
        #                     'number': self.chancery_profile.house_num,
        #                     'postalcode': self.chancery_profile.postcode,
        #                     'city': self.chancery_profile.town,
        #                 }
        #             }})
        #             idx += 1

        # Updates ChanceryProfile
        step1 = Step('chancery_registration',
                     forms=step1_forms,
                     template='backoffice/wizard/election_setup/step1.html',
                     initial=step1_initial,
                     extra_context={'instance':self.election_instance, })
        # Updates ElectionInstance
        step2 = Step('election_details',
                     forms={'election_details': ElectionInstanceForm},
                     template='backoffice/wizard/election_setup/step2.html',
                     initial={'election_details': self.election_instance},
                     extra_context={'instance':self.election_instance, })
        # Updates Council
        step3 = Step('council_contact_information',
                     forms={'council_contact_information': CouncilContactInformationForm},
                     template='backoffice/wizard/election_setup/step3.html',
                     initial={'council_contact_information': {
                        'name': self.election_instance.council.name,
                        'address': {
                            'street': self.election_instance.council.street,
                            'number': self.election_instance.council.house_num,
                            'postalcode': self.election_instance.council.postcode,
                            'city': self.election_instance.council.town,
                        },
                        'website': self.election_instance.council.website,
                        'email': self.election_instance.council.email,
                     }},
                     extra_context={'instance':self.election_instance, })
        # Updates Council
        step4 = Step('council_additional_information',
                     forms={'council_additional_information': CouncilForm},
                     template='backoffice/wizard/election_setup/step4.html',
                     initial={'council_additional_information': self.election_instance.council},
                     extra_context={'instance':self.election_instance, })
        # Updates ChanceryProfile
        #FIXME: step5 = Step('chancery_contact_information',
        #                      forms=step5_forms,
        #                      template='backoffice/wizard/election_setup/step5.html',
        #                      initial=step5_initial)
        # Updates Council
        # step6 = Step('council_styling_setup',
        #                      forms={'council_styling_setup': CouncilStylingSetupForm},
        #                      template='backoffice/wizard/election_setup/step6.html',
        #                      initial={'council_styling_setup': self.election_instance.council},
        #                      extra_context={'instance':self.election_instance, })
        #FIXME: scenario_tree = step1.next(step2.next(step3.next(step4.next(step5.next(step6)))))
        #FIXME: scenario_tree = step1.next(step2.next(step3.next(step4.next(step6))))
        scenario_tree = step1.next(step2.next(step3.next(step4)))

        template = 'backoffice/wizard/election_setup/base.html',
        super(self.__class__, self).__init__(scenario_tree, template)

    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0

    @transaction.commit_manually
    def done(self, request, form_dict):
        self.chancery_profile_data = {}
        self.council_data = {}
        self.election_instance_data = {}
        self.election_instance_parties_data = {}
        
        try:
            for path, forms in form_dict.iteritems():
                for name, form in forms.iteritems():
                    if name == 'chancery_registration0':          
                        self.chancery_profile_data.update({
                            'first_name': form.cleaned_data['name']['first_name'],
                            'middle_name': form.cleaned_data['name']['middle_name'],
                            'last_name': form.cleaned_data['name']['last_name'],
                            'gender': form.cleaned_data['gender'],
                            'workingdays': form.cleaned_data['workingdays'],
                            'telephone': form.cleaned_data['telephone']
                        })
                    #FIXME elif  name == 'chancery_contact_information0':
                    #                         self.chancery_profile_data.update({
                    #                             'street': form.cleaned_data['address']['street'],
                    #                             'house_num': form.cleaned_data['address']['number'],
                    #                             'postcode': form.cleaned_data['address']['postalcode'],
                    #                             'town': form.cleaned_data['address']['city'],
                    #                             'website': form.cleaned_data['website']
                    #                         })
                    elif name == 'council_contact_information':
                        self.council_data.update({
                            'name': form.cleaned_data['name'],
                            'street': form.cleaned_data['address']['street'],
                            'house_num': form.cleaned_data['address']['number'],
                            'postcode': form.cleaned_data['address']['postalcode'],
                            'town': form.cleaned_data['address']['city'],
                            'website': form.cleaned_data['website'],
                            'email': form.cleaned_data['email']
                        })
                    elif name in ('council_additional_information', 'council_styling_setup'):
                        self.council_data.update(form.cleaned_data)
                    elif name in ('election_details',):
                        self.election_instance_data.update(form.cleaned_data)
                    
            self.chancery_profile_data.update({'workingdays': ','.join(map(lambda x: str(x), self.chancery_profile_data.get('workingdays', [])))})
            
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

        except Exception, e:
            transaction.rollback()
            raise
        else:
            transaction.commit()

        return redirect('bo.election_setup_done', election_instance_id=self.election_instance.pk)