from django.db import transaction
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from utils.multipathform import Step, MultiPathFormWizard
from utils.graphformwizard import GraphFormWizard
from utils.graphformwizard import Step as GStep
from elections.models import Candidacy, ElectionInstanceParty
from elections.functions import get_profile_forms, create_profile, profile_invite_email_templates
from django.utils.translation import ugettext_lazy as _

from political_profiles.forms import PoliticianProfileForm, LinkForm, InterestForm, AppearanceForm, WorkExperienceForm
from political_profiles.forms import EducationForm, PoliticalExperienceForm

from invitations.models import Invitation

class PoliticianProfileAppearanceWizard1(GraphFormWizard):

    # init action reloads the data
    fast_actions = frozenset(['init'])
    # wizard scenario
    scenario = GStep("appearance_wizard", header = _("Enter your Appearances"), title = _("Appearances")) \
                .forms(dict(appearance=AppearanceForm,)) \
                .data(help = _("You can add/edit appearances.")) \
                .data(next_button = _("Add/Edit")) \
              


    def __init__(self, name = None, template = 'backoffice/wizard/election_setup/base.html'):
        super(type(self), self).__init__(name, template)


    def done(self, request, wizard_data, meta, *args, **kwargs):
        # OK, I'm to tired to finish this thing
        # The wizard data contains dicts with all the data
        # meta contains user_id and election_instance_id
        # we should save the data here and redirecto "done" location
        print wizard_data
        print meta
        return
        #return redirect(reverse('backoffice.politician_profile_appearance', kwargs={'user_id': meta.user_id, 'election_instance_id': meta.election_instance_id }))


    def wizard_fast_action(self, request, action, step, step_path, url_step, url_action, *args, **kwargs):
        """Loads correct models"""

        if action == "init":
            if 'election_instance_id' not in kwargs:
                raise
            if 'user_id' not in kwargs:
                raise
            if 'appearance_id' not in kwargs:
                appearance_id = None
            else:
                appearance_id = kwargs['appearance_id']
            user_id = kwargs['user_id']
            election_instance_id = kwargs['election_instance_id']
   

            # Checking if user really exists and if election_instanc exists. Getting those and passing it to the wizard.
            election_instance = get_object_or_404(ElectionInstance, id = election_instance_id)
            user = get_object_or_404(User, id = user_id)
            if appearance_id:
                appearance = get_object_or_404(Appearance, pk = appearance_id)
            else:
                appearance = None

            PoliticianProfileClass = get_profile_model('council_admin')
            if user.profile.__class__ is not PoliticianProfileClass:
                raise HttpResponseForbidden("Wrong user profile")

            # reload data
            data = {}
            # [FIXME: adress field should be prefixed in data, automatic prefixing will not work]
            # will be fixed later

            form = GStep.new_form(form = AppearanceForm, initial = appearance)
            data['appearance'] = {'appearance' : getattr(form, 'cleaned_data', {})}
            import ipdb; ipdb.set_trace()
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




class PoliticianProfileAppearanceWizard(MultiPathFormWizard):
    """
        Wizard for a candidate to editing their own profiles Appearances
    """
    def __init__(self, *args, **kwargs):
        # Getting "user_id"
        try:
            self.user_id = kwargs['user_id']
            self.appearance_id = kwargs['appearance_id']
            self.election_instance_id =  kwargs['election_instance_id']
            # Checking if user really exists and if election_instanc exists. Getting those and passing it to the wizard.
            self.user = User.objects.get(pk=self.user_id)
            if self.appearance_id:
                self.appearance = self.user.profile.appearances.get(pk=self.appearance_id)
            else:
                self.appearance = None

        except Exception, e:
            raise e
        step1_forms = dict(appearance=AppearanceForm,)
        step1 = Step('candidate_edit_appearance',
                    forms=step1_forms,
                    template='backoffice/wizard/politician_profile/step1.html',
                    initial={'appearance': self.appearance })
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
            if self.appearance_id:
                appearance = self.appearance
            else:
                appearance = self.user.profile.appearances.create(
                    politician=self.user.profile,
                )

            for (key, value) in self.candidate_appearance_data.items():
                setattr(appearance, key, value)
            appearance.save(force_update=True)

        except Exception, e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()

        if request.POST.get('next', 'overview') == 'overview':
            return redirect('bo.politician_profile_appearance', user_id=self.user_id, election_instance_id=self.election_instance_id)
        raise NotImplementedError('Implement a redirect to the council edit wizard here.')

class PoliticianProfilePoliticalWizard(MultiPathFormWizard):
    """
        Wizard for a candidate to editing their own profiles Work
    """
    def __init__(self, *args, **kwargs):
        # Getting "user_id"
        try:
            self.user_id = kwargs['user_id']
            self.political_id = kwargs['political_id']
            self.election_instance_id =  kwargs['election_instance_id']
            # Checking if user really exists and if election_instanc exists. Getting those and passing it to the wizard.
            self.user = User.objects.get(pk=self.user_id)
            if self.political_id:
                self.political = self.user.profile.political.get(pk=self.political_id)
            else:
                self.political = None
            
        except Exception, e:
            raise e
        step1_forms = dict(political=PoliticalExperienceForm,)
        step1 = Step('candidate_edit_political',
                    forms=step1_forms,
                    template='backoffice/wizard/politician_profile/step1.html',
                    initial={'political': self.political })
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

            if self.political_id:
                political = self.political
            else:
                political = self.user.profile.political.create(
                    politician=self.user.profile,
                )


            for (key, value) in self.candidate_political_data.items():
                setattr(political, key, value)
            political.save(force_update=True)

        except Exception, e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()

        if request.POST.get('next', 'overview') == 'overview':
            return redirect('bo.politician_profile_political', kwargs={'user_id': self.user_id, 'election_instance_id': self.election_instance_id, })
        raise NotImplementedError('Implement a redirect to the council edit wizard here.')

class PoliticianProfileWorkWizard(MultiPathFormWizard):
    """
        Wizard for a candidate to editing their own profiles Work
    """
    def __init__(self, *args, **kwargs):
        # Getting "user_id"
        try:
            self.user_id = kwargs['user_id']
            self.work_id = kwargs['work_id']
            self.election_instance_id =  kwargs['election_instance_id']
            # Checking if user really exists and if election_instanc exists. Getting those and passing it to the wizard.
            self.user = User.objects.get(pk=self.user_id)
            if self.work_id:
                self.work = self.user.profile.work.get(pk=self.work_id)
            else:
                self.work = None
            
        except Exception, e:
            raise e
        step1_forms = dict(work=WorkExperienceForm,)
        step1 = Step('candidate_edit_work',
                    forms=step1_forms,
                    template='backoffice/wizard/politician_profile/step1.html',
                    initial={'work': self.work })
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

            if self.work_id:
                work = self.work
            else:
                work = self.user.profile.work.create(
                    politician=self.user.profile,
                )


            for (key, value) in self.candidate_work_data.items():
                setattr(work, key, value)
            work.save(force_update=True)

        except Exception, e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()

        if request.POST.get('next', 'overview') == 'overview':
            return redirect('bo.politician_profile_work', kwargs={'user_id': self.user_id, 'election_instance_id': self.election_instance_id })
        raise NotImplementedError('Implement a redirect to the council edit wizard here.')

class PoliticianProfileInterestWizard(MultiPathFormWizard):
    """
        Wizard for a candidate to editing their own profiles links
    """
    def __init__(self, *args, **kwargs):
        # Getting "user_id"
        try:
            self.user_id = kwargs['user_id']
            self.interest_id = kwargs['interest_id']
            self.election_instance_id =  kwargs['election_instance_id']
            # Checking if user really exists and if election_instanc exists. Getting those and passing it to the wizard.
            self.user = User.objects.get(pk=self.user_id)
            if self.interest_id:
                self.interest = self.user.profile.interests.get(pk=self.interest_id)
            else:
                self.interest = None
            
        except Exception, e:
            raise e
        step1_forms = dict(interest=InterestForm,)
        step1 = Step('candidate_edit_interest',
                    forms=step1_forms,
                    template='backoffice/wizard/politician_profile/step1.html',
                    initial={'interest': self.interest })
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

            if self.interest_id:
                interest = self.interest
            else:
                interest = self.user.profile.interests.create(
                    politician=self.user.profile,
                )


            for (key, value) in self.candidate_interest_data.items():
                setattr(interest, key, value)
            interest.save(force_update=True)

        except Exception, e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()

        if request.POST.get('next', 'overview') == 'overview':
            return redirect('bo.politician_profile_interest', kwargs={'user_id': self.user_id, 'election_instance_id': self.election_instance_id, })
        raise NotImplementedError('Implement a redirect to the council edit wizard here.')

class PoliticianProfileEducationWizard(MultiPathFormWizard):
    """
        Wizard for a candidate to editing their own profiles links
    """
    def __init__(self, *args, **kwargs):
        # Getting "user_id"
        try:
            self.user_id = kwargs['user_id']
            self.education_id = kwargs['education_id']
            self.election_instance_id =  kwargs['election_instance_id']
            # Checking if user really exists and if election_instanc exists. Getting those and passing it to the wizard.
            self.user = User.objects.get(pk=self.user_id)
            if self.education_id:
                self.education = self.user.profile.education.get(pk=self.education_id)
            else:
                self.education = None
            
        except Exception, e:
            raise e

        step1_forms = dict(education=EducationForm,)
        step1 = Step('candidate_edit_education',
                    forms=step1_forms,
                    template='backoffice/wizard/politician_profile/step1.html',
                    initial={'education': self.education })
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
                    if name == 'education':
                        self.candidate_education_data = form.cleaned_data

            if self.education_id:
                education = self.education
            else:
                education = self.user.profile.education.create(
                    politician=self.user.profile,
                )


            for (key, value) in self.candidate_education_data.items():
                setattr(education, key, value)
            education.save(force_update=True)

        except Exception, e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()

        if request.POST.get('next', 'overview') == 'overview':
            return redirect('bo.politician_profile_education', kwargs={'user_id': self.user_id, 'election_instance_id': self.election_instance_id })
        raise NotImplementedError('Implement a redirect to the council edit wizard here.')


class PoliticianProfileLinkWizard(MultiPathFormWizard):
    """
        Wizard for a candidate to editing their own profiles links
    """
    def __init__(self, *args, **kwargs):
        # Getting "user_id"
        try:
            self.user_id = kwargs['user_id']
            self.link_id = kwargs['link_id']
            self.election_instance_id =  kwargs['election_instance_id']
            # Checking if user really exists and if election_instanc exists. Getting those and passing it to the wizard.
            self.user = User.objects.get(pk=self.user_id)
            if self.link_id:
                self.link = self.user.profile.links.get(pk=self.link_id)
            else:
                self.link = None
            
        except Exception, e:
            raise e
        
        step1_forms = dict(link=LinkForm,)
        step1 = Step('candidate_edit_link',
                    forms=step1_forms,
                    template='backoffice/wizard/politician_profile/step1.html',
                    initial={'link': self.link })
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

            if self.link_id:
                link = self.link
            else:
                link = self.user.profile.links.create(
                    politician=self.user.profile,
                )


            for (key, value) in self.candidate_link_data.items():
                setattr(link, key, value)
            link.save(force_update=True) 

        except Exception, e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()

        if request.POST.get('next', 'overview') == 'overview':
            return redirect('bo.politician_profile_link', kwargs={'user_id': self.user_id, 'election_instance_id': self.election_instance_id, })
        raise NotImplementedError('Implement a redirect to the council edit wizard here.')


class PoliticianProfileWizard(MultiPathFormWizard):
    """
        Wizard for a candidate to editing their own profile
    """

    
    def __init__(self, *args, **kwargs):
        # Getting "user_id"
        try:
            self.user_id = kwargs['user_id']
            self.election_instance_id =  kwargs['election_instance_id']
            # Checking if user really exists and if election_instanc exists. Getting those and passing it to the wizard.
            self.user = User.objects.get(pk=self.user_id)

            self.user_profile_dict = {
                'name': {'first_name': self.user.profile.first_name, 'middle_name': self.user.profile.middle_name, 'last_name': self.user.profile.last_name, },
                'email': self.user.email,
                'initials': self.user.profile.initials,
                'dateofbirth': self.user.profile.dateofbirth,
                'introduction': self.user.profile.introduction,
                'motivation': self.user.profile.motivation,
                'gender': self.user.profile.gender,
                'picture': self.user.profile.picture,
                'movie': self.user.profile.movie,
            }
            
        except Exception, e:
            raise e

        step1_forms = dict(initial_candidate = PoliticianProfileForm)
        step1 = Step('initial_candidate',
                    forms=step1_forms,
                    template='backoffice/wizard/politician_profile/step1.html',
                    initial={'initial_candidate': self.user_profile_dict })
                
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
                    if name == 'initial_candidate':
                        self.user_profile_dict = form.cleaned_data

            for (key, value) in self.user_profile_dict.items():
                setattr(self.user.profile, key, value)
            self.user.profile.save(force_update=True) # Updating the PoliticianProfile

        except Exception, e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()

        if request.POST.get('next', 'overview') == 'overview':
            return redirect(reverse('bo.politician_profile_link', kwargs={'user_id': self.user_id, 'election_instance_id': self.election_instance_id }))
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

        return redirect('bo.election_party_view', args=self.election_instance_party_id)
