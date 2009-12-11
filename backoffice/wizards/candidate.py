from django.db import transaction
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404

from utils.multipathform import Step, MultiPathFormWizard

from elections.models import Candidacy, ElectionInstanceParty
from elections.functions import get_profile_forms, create_profile, profile_invite_email_templates


from political_profiles.forms import PoliticianProfileForm, LinkForm, InterestForm, AppearanceForm, WorkExperienceForm
from political_profiles.forms import EducationForm, PoliticalExperienceForm

from invitations.models import Invitation

class PoliticianProfileAppearanceWizard(MultiPathFormWizard):
    """
        Wizard for a candidate to editing their own profiles Appearances
    """
    def __init__(self, *args, **kwargs):
        step1_forms = dict(appearance=AppearanceForm,)
        step1 = Step('candidate_edit_appearance',
                    forms=step1_forms,
                    template='backoffice/wizard/politician_profile/step1.html',)
        scenario_tree = step1
        #default template is the base, each step can override it as needed (for buttons)
        template = 'backoffice/wizard/politician_profile/base.html',
        super(PoliticianProfileAppearanceWizard, self).__init__(scenario_tree, template)

    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0

    @transaction.commit_manually
    def done(self, request, form_dict):
        try:
            for path, forms in form_dict.iteritems():
                for name, form in forms.iteritems():
                    if name == 'appearance':
                        self.candidate_appearance_data = form.cleaned_data
        except Exception, e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()

        if request.POST.get('next', 'overview') == 'overview':
            return redirect(reverse('backoffice.politician_profile_appearance', kwargs={'user_id':1}))
        raise NotImplementedError('Implement a redirect to the council edit wizard here.')

class PoliticianProfilePoliticalWizard(MultiPathFormWizard):
    """
        Wizard for a candidate to editing their own profiles Work
    """
    def __init__(self, *args, **kwargs):
        step1_forms = dict(political=PoliticalExperienceForm,)
        step1 = Step('candidate_edit_political',
                    forms=step1_forms,
                    template='backoffice/wizard/politician_profile/step1.html',)
        scenario_tree = step1
        #default template is the base, each step can override it as needed (for buttons)
        template = 'backoffice/wizard/politician_profile/base.html',
        super(PoliticianProfilePoliticalWizard, self).__init__(scenario_tree, template)

    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0

    @transaction.commit_manually
    def done(self, request, form_dict):
        try:
            for path, forms in form_dict.iteritems():
                for name, form in forms.iteritems():
                    if name == 'political':
                        self.candidate_political_data = form.cleaned_data
        except Exception, e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()

        if request.POST.get('next', 'overview') == 'overview':
            return redirect(reverse('backoffice.politician_profile_political', kwargs={'user_id':1}))
        raise NotImplementedError('Implement a redirect to the council edit wizard here.')

class PoliticianProfileWorkWizard(MultiPathFormWizard):
    """
        Wizard for a candidate to editing their own profiles Work
    """
    def __init__(self, *args, **kwargs):
        step1_forms = dict(work=WorkExperienceForm,)
        step1 = Step('candidate_edit_work',
                    forms=step1_forms,
                    template='backoffice/wizard/politician_profile/step1.html',)
        scenario_tree = step1
        #default template is the base, each step can override it as needed (for buttons)
        template = 'backoffice/wizard/politician_profile/base.html',
        super(PoliticianProfileWorkWizard, self).__init__(scenario_tree, template)

    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0

    @transaction.commit_manually
    def done(self, request, form_dict):
        try:
            for path, forms in form_dict.iteritems():
                for name, form in forms.iteritems():
                    if name == 'work':
                        self.candidate_work_data = form.cleaned_data
        except Exception, e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()

        if request.POST.get('next', 'overview') == 'overview':
            return redirect(reverse('backoffice.politician_profile_work', kwargs={'user_id':1}))
        raise NotImplementedError('Implement a redirect to the council edit wizard here.')

class PoliticianProfileInterestWizard(MultiPathFormWizard):
    """
        Wizard for a candidate to editing their own profiles links
    """
    def __init__(self, *args, **kwargs):
        step1_forms = dict(interest=InterestForm,)
        step1 = Step('candidate_edit_link',
                    forms=step1_forms,
                    template='backoffice/wizard/politician_profile/step1.html',)
        scenario_tree = step1
        #default template is the base, each step can override it as needed (for buttons)
        template = 'backoffice/wizard/politician_profile/base.html',
        super(PoliticianProfileInterestWizard, self).__init__(scenario_tree, template)

    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0

    @transaction.commit_manually
    def done(self, request, form_dict):
        try:
            for path, forms in form_dict.iteritems():
                for name, form in forms.iteritems():
                    if name == 'interest':
                        self.candidate_interest_data = form.cleaned_data
        except Exception, e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()

        if request.POST.get('next', 'overview') == 'overview':
            return redirect(reverse('backoffice.politician_profile_interest', kwargs={'user_id':1}))
        raise NotImplementedError('Implement a redirect to the council edit wizard here.')

class PoliticianProfileEducationWizard(MultiPathFormWizard):
    """
        Wizard for a candidate to editing their own profiles links
    """
    def __init__(self, *args, **kwargs):
        step1_forms = dict(education=EducationForm,)
        step1 = Step('candidate_edit_education',
                    forms=step1_forms,
                    template='backoffice/wizard/politician_profile/step1.html',)
        scenario_tree = step1
        #default template is the base, each step can override it as needed (for buttons)
        template = 'backoffice/wizard/politician_profile/base.html',
        super(PoliticianProfileEducationWizard, self).__init__(scenario_tree, template)

    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0

    @transaction.commit_manually
    def done(self, request, form_dict):
        try:
            for path, forms in form_dict.iteritems():
                for name, form in forms.iteritems():
                    if name == 'link':
                        self.candidate_education_data = form.cleaned_data
        except Exception, e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()

        if request.POST.get('next', 'overview') == 'overview':
            return redirect(reverse('backoffice.politician_profile_education', kwargs={'user_id':1}))
        raise NotImplementedError('Implement a redirect to the council edit wizard here.')


class PoliticianProfileLinkWizard(MultiPathFormWizard):
    """
        Wizard for a candidate to editing their own profiles links
    """
    def __init__(self, *args, **kwargs):
        step1_forms = dict(link=LinkForm,)
        step1 = Step('candidate_edit_link',
                    forms=step1_forms,
                    template='backoffice/wizard/politician_profile/step1.html',)
        scenario_tree = step1
        #default template is the base, each step can override it as needed (for buttons)
        template = 'backoffice/wizard/politician_profile/base.html',
        super(PoliticianProfileLinkWizard, self).__init__(scenario_tree, template)

    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0

    @transaction.commit_manually
    def done(self, request, form_dict):
        try:
            for path, forms in form_dict.iteritems():
                for name, form in forms.iteritems():
                    if name == 'link':
                        self.candidate_link_data = form.cleaned_data
        except Exception, e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()

        if request.POST.get('next', 'overview') == 'overview':
            return redirect(reverse('backoffice.politician_profile_link', kwargs={'user_id':1}))
        raise NotImplementedError('Implement a redirect to the council edit wizard here.')


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


        step1 = Step('candidate_edit',
                    forms=step1_forms,
                    template='backoffice/wizard/politician_profile/step1.html',)

        scenario_tree = step1
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
                    if name == 'link':
                        self.link = form.cleaned_data
        except Exception, e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()

        if request.POST.get('next', 'overview') == 'overview':
            return redirect(reverse('backoffice.politician_profile_link', kwargs={'user_id':1}))
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

        return redirect('backoffice.election_party_view', args=self.election_instance_party_id)
