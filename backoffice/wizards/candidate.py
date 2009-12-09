from django.db import transaction
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404

from utils.multipathform import Step, MultiPathFormWizard

from elections.models import Candidacy, ElectionInstanceParty
from elections.functions import get_profile_forms, create_profile, profile_invite_email_templates

#TODO: Use the get_profile_forms method and remove these
from political_profiles.forms import PoliticianProfileForm, LinkForm, InterestForm, AppearenceForm, WorkExperienceForm
from political_profiles.forms import EducationForm, PoliticalExperienceForm

from invitations.models import Invitation

class PoliticianProfileWizard(MultiPathFormWizard):
    """
        Wizard for a candidate to editing their own profile
    """
    def __init__(self, *args, **kwargs):
        # Getting "user_id"
        """
        try:
            self.user_id = kwargs['user_id'],

            # Checking if user really exists and if election_instanc exists. Getting those and passing it to the wizard.

            self.user = User.objects.get(id=self.user_id)
            #self.chancery_profile = ChanceryProfile.objects.get(user=self.user_id)
        except Exception, e:
            raise e
        """

        step1_forms = dict(initial_candidate = PoliticianProfileForm,)
        step2_forms = dict(link=LinkForm,)
        step3_forms = dict(intrest=InterestForm,)
        step4_forms = dict(appearence=AppearenceForm,)
        step5_forms = dict(work= WorkExperienceForm,)
        step6_forms = dict(education=EducationForm,)
        step7_forms = dict(political=PoliticalExperienceForm,)

        step1 = Step('candidate_edit',
                    forms=step1_forms,
                    template='backoffice/wizard/politician_profile/step1.html',)
        step2 = Step('link',
                    forms=step2_forms,
                    template='backoffice/wizard/politician_profile/step2.html',)
        step3 = Step('interest',
                    forms=step3_forms,
                     template='backoffice/wizard/politician_profile/step3.html',)
        step4 = Step('appearance',
                    forms=step4_forms,
                    template='backoffice/wizard/politician_profile/step4.html',)
        step5 = Step('work',
                    forms=step5_forms,
                    template='backoffice/wizard/politician_profile/step5.html',)
        step6 = Step('education',
                    forms=step6_forms,
                    template='backoffice/wizard/politician_profile/step6.html',)
        step7 = Step('political',
                    forms=step7_forms,
                    template='backoffice/wizard/politician_profile/step7.html',)

        scenario_tree = step1.next(step2.next(step3.next(step4.next(step5.next(step6.next(step7))))))

        #default template is the base, each step can override it as needed (for buttons)

        template = 'backoffice/wizard/politician_profile/base.html',

        super(PoliticianProfileWizard, self).__init__(scenario_tree, template)


    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0
    
    @transaction.commit_manually
    def done(self, request, form_dict):
        try:
            for path, forms in form_dict.iteritems():
                for name, form in forms.iteritems():
                    if name == 'initial_candidate':
                        self.candidate_data = form.cleaned_data
                    elif name == 'link':
                        self.link = form.cleaned_data
                    elif name == 'intrest':
                        self.intrest = form.cleaned_data
                    elif name == 'appearence':
                        self.appearence = form.cleaned_data
                    elif name == 'work':
                        self.work = form.cleaned_data
                    elif name == 'political':
                        self.political = form.cleaned_data
                    elif name == 'education':
                        self.education = form.cleaned_data



            #Get the polictician profile
            #politician = PoliticalProfile.objects.get(user_id=self.user.id)
            #print politician


        except Exception, e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()

        if request.POST.get('next', 'overview') == 'overview':
            return redirect('backoffice.profile_complete')
        raise NotImplementedError('Implement a redirect to the council edit wizard here.')
        
        
class AddCandidateWizard(MultiPathFormWizard):
    """
        Wizard for adding a Candidate
    """

    def __init__(self, *args, **kwargs):
        self.election_instance_party_id = 1 #kwargs['election_instance_party_id']
        self.position = 1 #kwargs['position']
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

            #Store data
            tmp_data = {
                'first_name': self.form_data['name']['first_name'],
                'middle_name': self.form_data['name']['middle_name'],
                'last_name': self.form_data['name']['last_name'],
                'email': self.form_data['email'],
                'gender': self.form_data['gender'],
            }
            self.candidate = create_profile('candidate', tmp_data)

            #Link candidate to party
            candidacy = Candidacy(
                election_party_instance = get_object_or_404(ElectionInstanceParty, party=self.election_instance_party_id),
                candidate = self.candidate.user,
                position = self.position,
            )
            candidacy.save()

            #Create invitation
            templates = profile_invite_email_templates('candidate')
            Invitation.create(
                user_from = request.user,
                user_to = self.candidate.user,
                view = '',
                text = 'Invitation text',
                subject = 'Invitation',
                html_template = templates['html'],
                plain_template = templates['plain'],
            )

        except Exception:
            transaction.rollback()
            raise
        else:
            transaction.commit()
        #TODO: Make args=[1] dynamic. In addcandidate/step1.html too ('Cancel'-link)


        return HttpResponseRedirect(reverse('backoffice.election_party_view', args=[1]))