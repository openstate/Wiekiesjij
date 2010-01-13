from django.db import transaction
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from utils.multipathform import Step, MultiPathFormWizard
from elections.models import Candidacy, ElectionInstanceParty
from elections.functions import get_profile_forms, create_profile, profile_invite_email_templates
from utils.exceptions import PermissionDeniedException

from political_profiles.forms import PoliticianProfileLifeForm, PoliticianProfileExtraForm, PoliticianProfileForm, LinkForm, InterestForm, AppearanceForm, WorkExperienceForm
from political_profiles.forms import ConnectionForm, EducationForm, PoliticalExperienceForm, PoliticianProfilePoliticalForm, GoalForm

from questions.functions import get_question_count

from invitations.models import Invitation


class PoliticianProfileAppearanceWizard(MultiPathFormWizard):
    """
        Wizard for a candidate to editing their own profiles Appearances
    """
    def __init__(self, *args, **kwargs):
        # Getting "user_id"
        try:
            self.user_id = kwargs['user_id']
            self.appearance_id = kwargs['appearance_id']
            self.eip_id =  kwargs['eip_id']
            self.election_instance_party = get_object_or_404(ElectionInstanceParty, pk=self.eip_id)
            self.user = get_object_or_404(self.election_instance_party.candidates, candidate__pk=self.user_id).candidate
            
            if self.appearance_id:
                self.appearance = self.user.profile.appearances.get(pk=self.appearance_id)
            else:
                self.appearance = None

        except Exception:
            raise
        step1_forms = dict(appearance=AppearanceForm,)
        step1 = Step('candidate_edit_appearance',
                    forms=step1_forms,
                    template='backoffice/wizard/politician_profile/appearances-add.html',
                    initial={'appearance': self.appearance },
                    extra_context={'questions': range(0, get_question_count(self.election_instance_party)),
                    'eip_id': self.eip_id, 'user_id': self.user_id},
                    )
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

        except Exception:
            transaction.rollback()
            raise
        else:
            transaction.commit()

        return redirect('bo.politician_profile_appearance', user_id=self.user_id, eip_id=self.eip_id)


class PoliticianProfilePoliticalWizard(MultiPathFormWizard):
    """
        Wizard for a candidate to editing their own profiles Work
    """
    def __init__(self, *args, **kwargs):
        # Getting "user_id"
        try:
            self.user_id = kwargs['user_id']
            self.political_id = kwargs['political_id']
            self.eip_id =  kwargs['eip_id']
            self.election_instance_party = get_object_or_404(ElectionInstanceParty, pk=self.eip_id)
            self.user = get_object_or_404(self.election_instance_party.candidates, candidate__pk=self.user_id).candidate
            
            if self.political_id:
                self.political = self.user.profile.political.get(pk=self.political_id)
            else:
                self.political = None
            
        except Exception:
            raise
        step1_forms = dict(political=PoliticalExperienceForm,)
        step1 = Step('candidate_edit_political',
                    forms=step1_forms,
                    template='backoffice/wizard/politician_profile/political-add.html',
                    initial={'political': self.political },
                    extra_context={'questions': range(0, get_question_count(self.election_instance_party)),
                    'eip_id': self.eip_id, 'user_id': self.user_id},
                    )
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

        except Exception:
            transaction.rollback()
            raise
        else:
            transaction.commit()


        return redirect('bo.politician_profile_political', user_id=self.user_id, eip_id=self.eip_id )


class PoliticianProfileWorkWizard(MultiPathFormWizard):
    """
        Wizard for a candidate to editing their own profiles Work
    """
    def __init__(self, *args, **kwargs):
        # Getting "user_id"
        try:
            self.user_id = kwargs['user_id']
            self.work_id = kwargs['work_id']
            self.eip_id =  kwargs['eip_id']
            self.election_instance_party = get_object_or_404(ElectionInstanceParty, pk=self.eip_id)
            self.user = get_object_or_404(self.election_instance_party.candidates, candidate__pk=self.user_id).candidate
            
            if self.work_id:
                self.work = self.user.profile.work.get(pk=self.work_id)
            else:
                self.work = None
            
        except Exception:
            raise
        step1_forms = dict(work=WorkExperienceForm,)
        step1 = Step('candidate_edit_work',
                    forms=step1_forms,
                    template='backoffice/wizard/politician_profile/work-add.html',
                    initial={'work': self.work },
                    extra_context={'questions': range(0, get_question_count(self.election_instance_party)),
                    'eip_id': self.eip_id, 'user_id': self.user_id},
                    )
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

        except Exception:
            transaction.rollback()
            raise
        else:
            transaction.commit()


        return redirect('bo.politician_profile_work', user_id=self.user_id, eip_id=self.eip_id )


class PoliticianProfileInterestWizard(MultiPathFormWizard):
    """
        Wizard for a candidate to editing their own profiles links
    """
    def __init__(self, *args, **kwargs):
        # Getting "user_id"
        try:
            self.user_id = kwargs['user_id']
            self.interest_id = kwargs['interest_id']
            self.eip_id =  kwargs['eip_id']
            self.election_instance_party = get_object_or_404(ElectionInstanceParty, pk=self.eip_id)
            self.user = get_object_or_404(self.election_instance_party.candidates, candidate__pk=self.user_id).candidate
            
            if self.interest_id:
                self.interest = self.user.profile.interests.get(pk=self.interest_id)
            else:
                self.interest = None
            
        except Exception:
            raise
        step1_forms = dict(interest=InterestForm,)
        step1 = Step('candidate_edit_interest',
                    forms=step1_forms,
                    template='backoffice/wizard/politician_profile/interest-add.html',
                    initial={'interest': self.interest },
                    extra_context={'questions': range(0, get_question_count(self.election_instance_party)),
                    'eip_id': self.eip_id, 'user_id': self.user_id},
                    )
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

        except Exception:
            transaction.rollback()
            raise
        else:
            transaction.commit()


        return redirect('bo.politician_profile_interest', user_id=self.user_id, eip_id=self.eip_id )


class PoliticianProfileEducationWizard(MultiPathFormWizard):
    """
        Wizard for a candidate to editing their own profiles links
    """
    def __init__(self, *args, **kwargs):
        # Getting "user_id"
        try:
            self.user_id = kwargs['user_id']
            self.education_id = kwargs['education_id']
            self.eip_id =  kwargs['eip_id']
            self.election_instance_party = get_object_or_404(ElectionInstanceParty, pk=self.eip_id)
            self.user = get_object_or_404(self.election_instance_party.candidates, candidate__pk=self.user_id).candidate
            
            if self.education_id:
                self.education = self.user.profile.education.get(pk=self.education_id)
            else:
                self.education = None
            
        except Exception:
            raise

        step1_forms = dict(education=EducationForm,)
        step1 = Step('candidate_edit_education',
                    forms=step1_forms,
                    template='backoffice/wizard/politician_profile/education-add.html',
                    initial={'education': self.education },
                    extra_context={'questions': range(0, get_question_count(self.election_instance_party)),
                    'eip_id': self.eip_id, 'user_id': self.user_id},
                    )
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

        except Exception:
            transaction.rollback()
            raise
        else:
            transaction.commit()


        return redirect('bo.politician_profile_education', user_id=self.user_id, eip_id=self.eip_id )



class PoliticianProfileLinkWizard(MultiPathFormWizard):
    """
        Wizard for a candidate to editing their own profiles links
    """
    def __init__(self, *args, **kwargs):
        # Getting "user_id"
        try:
            self.user_id = kwargs['user_id']
            self.link_id = kwargs['link_id']
            self.eip_id =  kwargs['eip_id']
            self.election_instance_party = get_object_or_404(ElectionInstanceParty, pk=self.eip_id)
            self.user = get_object_or_404(self.election_instance_party.candidates, candidate__pk=self.user_id).candidate
            
            if self.link_id:
                self.link = self.user.profile.links.get(pk=self.link_id)
            else:
                self.link = None
            
        except Exception:
            raise
        
        step1_forms = dict(link=LinkForm,)
        step1 = Step('candidate_edit_link',
                    forms=step1_forms,
                    template='backoffice/wizard/politician_profile/links-add.html',
                    initial={'link': self.link },
                    extra_context={'questions': range(0, get_question_count(self.election_instance_party)),
                    'eip_id': self.eip_id, 'user_id': self.user_id},
                    )
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

        except Exception:
            transaction.rollback()
            raise
        else:
            transaction.commit()


        return redirect('bo.politician_profile_link', user_id=self.user_id, eip_id=self.eip_id)

class PoliticianProfileGoalWizard(MultiPathFormWizard):
    """
        Wizard for a candidate to editing their own profiles goals
    """
    def __init__(self, *args, **kwargs):
        # Getting "user_id"
        try:
            self.user_id = kwargs['user_id']
            self.goal_id = kwargs['goal_id']
            self.eip_id =  kwargs['eip_id']
            self.election_instance_party = get_object_or_404(ElectionInstanceParty, pk=self.eip_id)
            self.user = get_object_or_404(self.election_instance_party.candidates, candidate__pk=self.user_id).candidate

            if self.goal_id:
                self.goal = self.user.profile.goals.get(pk=self.goal_id)
            else:
                self.goal = None

        except Exception:
            raise

        step1_forms = dict(goal=GoalForm,)
        step1 = Step('candidate_edit_goal',
                    forms=step1_forms,
                    template='backoffice/wizard/politician_profile/goals-add.html',
                    initial={'goal': self.goal },
                    extra_context={'questions': range(0, get_question_count(self.election_instance_party)),
                    'eip_id': self.eip_id, 'user_id': self.user_id},
                    )
        scenario_tree = step1
        #default template is the base, each step can override it as needed (for buttons)
        template = 'backoffice/wizard/politician_profile/base.html',
        super(PoliticianProfileGoalWizard, self).__init__(scenario_tree, template)

    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0

    @transaction.commit_manually
    def done(self, request, form_dict):
        try:
            for path, forms in form_dict.iteritems():
                for name, form in forms.iteritems():
                    if name == 'goal':
                        self.candidate_goal_data = form.cleaned_data

            if self.goal_id:
                goal = self.goal
            else:
                goal = self.user.profile.goals.create(
                    politician=self.user.profile,
                )

            for (key, value) in self.candidate_goal_data.items():
                setattr(goal, key, value)
            goal.save(force_update=True) 

        except Exception:
            transaction.rollback()
            raise
        else:
            transaction.commit()


        return redirect('bo.politician_profile_goal', user_id=self.user_id, eip_id=self.eip_id)

class PoliticianProfileConnectionWizard(MultiPathFormWizard):
    """
        Wizard for a candidate to editing their own profiles links
    """
    def __init__(self, *args, **kwargs):
        # Getting "user_id"
        try:
            self.user_id = kwargs['user_id']
            self.connection_id = kwargs['connection_id']
            self.eip_id =  kwargs['eip_id']
            self.election_instance_party = get_object_or_404(ElectionInstanceParty, pk=self.eip_id)
            self.user = get_object_or_404(self.election_instance_party.candidates, candidate__pk=self.user_id).candidate
            
            if self.connection_id:
                self.connection = self.user.profile.connections.get(pk=self.connection_id)
            else:
                self.connection = None

        except Exception:
            raise

        step1_forms = dict(connection=ConnectionForm,)
        step1 = Step('candidate_edit_connection',
                    forms=step1_forms,
                    template='backoffice/wizard/politician_profile/connections-add.html',
                    initial={'connection': self.connection },
                    extra_context={'questions': range(0, get_question_count(self.election_instance_party)),
                    'eip_id': self.eip_id, 'user_id': self.user_id},
                )
        scenario_tree = step1
        #default template is the base, each step can override it as needed (for buttons)
        template = 'backoffice/wizard/politician_profile/base.html',
        super(PoliticianProfileConnectionWizard, self).__init__(scenario_tree, template)

    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0

    @transaction.commit_manually
    def done(self, request, form_dict):
        try:
            for path, forms in form_dict.iteritems():
                for name, form in forms.iteritems():
                    if name == 'connection':
                        self.candidate_connection_data = form.cleaned_data

            if self.connection_id:
                connection = self.connection
            else:
                connection = self.user.profile.connections.create(
                    politician=self.user.profile,
                )


            for (key, value) in self.candidate_connection_data.items():
                setattr(connection, key, value)
            connection.save(force_update=True)

        except Exception:
            transaction.rollback()
            raise
        else:
            transaction.commit()


        return redirect('bo.politician_profile_connection', user_id=self.user_id, eip_id=self.eip_id)


class PoliticianProfileWizard(MultiPathFormWizard):
    """
        Wizard for a candidate to editing their own profile
    """

    
    def __init__(self, *args, **kwargs):
        # Getting "user_id"
        try:
            self.user_id = kwargs['user_id']
            self.eip_id =  kwargs['eip_id']
            
            self.election_instance_party = get_object_or_404(ElectionInstanceParty, pk=self.eip_id)
            self.user = get_object_or_404(self.election_instance_party.candidates, candidate__pk=self.user_id).candidate

            if self.user.profile is None or self.user.profile.type != 'candidate':
                raise PermissionDeniedException('Wrong profile type')

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

                'marital_status': self.user.profile.marital_status,
                'num_children': self.user.profile.num_children,
                'religion': self.user.profile.religion,
                'religious_group': self.user.profile.religious_group,
                'smoker': 'true' if self.user.profile.smoker == True else 'false',
                'diet': self.user.profile.diet,
                'fav_news': self.user.profile.fav_news,
                'transport': self.user.profile.transport,
                'charity': self.user.profile.charity,
                'fav_media': self.user.profile.fav_media,
                'fav_sport': self.user.profile.fav_sport,
                'hobby': self.user.profile.hobby,
                'fav_club': self.user.profile.fav_club,
                'fav_pet': self.user.profile.fav_pet,

            }
            
        except Exception:
            raise

        step1_forms = dict(initial_candidate = PoliticianProfileForm)
        step2_forms = dict(life_candidate = PoliticianProfileLifeForm)
        step3_forms = dict(extra_candidate = PoliticianProfileExtraForm)
        step4_forms = dict(political_candidate = PoliticianProfilePoliticalForm)
        step1 = Step('initial_candidate',
                    forms=step1_forms,
                    template='backoffice/wizard/politician_profile/step1.html',
                    initial={'initial_candidate': self.user_profile_dict },
                    extra_context={'questions': range(0, get_question_count(self.election_instance_party)),
                    'eip_id': self.eip_id, 'user_id': self.user_id},
                    )
        step2 = Step('life_candidate',
                    forms=step2_forms,
                    template='backoffice/wizard/politician_profile/step2.html',
                    initial={'life_candidate': self.user_profile_dict },
                    extra_context={'questions': range(0, get_question_count(self.election_instance_party)),
                    'eip_id': self.eip_id, 'user_id': self.user_id},
                    )
        step3 = Step('extra_candidate',
                    forms=step3_forms,
                    template='backoffice/wizard/politician_profile/step3.html',
                    initial={'extra_candidate': self.user_profile_dict },
                    extra_context={'questions': range(0, get_question_count(self.election_instance_party)),
                    'eip_id': self.eip_id, 'user_id': self.user_id},
                    )
        step4 = Step('political_candidate',
                    forms=step4_forms,
                    template='backoffice/wizard/politician_profile/step4.html',
                    initial={'political_candidate': self.user_profile_dict },
                    extra_context={'questions': range(0, get_question_count(self.election_instance_party)),
                    'eip_id': self.eip_id, 'user_id': self.user_id},
                    )
                
        scenario_tree = step1.next(step2.next(step3.next(step4)))
        #default template is the base, each step can override it as needed (for buttons)

        template = 'backoffice/wizard/politician_profile/base.html',
        super(PoliticianProfileWizard, self).__init__(scenario_tree, template)


    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0
    
    @transaction.commit_manually
    def done(self, request, form_dict):
        try:
            self.user_profile_dict = {}
            for path, forms in form_dict.iteritems():
                for name, form in forms.iteritems():
                    #if name == 'initial_candidate':
                    self.user_profile_dict.update(form.cleaned_data)
            
            for (key, value) in self.user_profile_dict.items():
                if key == 'smoker':
                    value = (value == 'true')
                setattr(self.user.profile, key, value)
            if self.user.profile.num_children is None:
                self.user.profile.num_children = 0
                
            self.user.profile.save(force_update=True) # Updating the PoliticianProfile

        except Exception, e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()

        return redirect('bo.politician_profile_goal', user_id=self.user_id, eip_id=self.eip_id )

        
        
class AddCandidateWizard(MultiPathFormWizard):
    """
        Wizard for adding a Candidate
    """

    def __init__(self, id, pos, *args, **kwargs):
        self.election_instance_party_id = id
        self.position = pos
        self.eip = get_object_or_404(ElectionInstanceParty, pk=self.election_instance_party_id)

        step1_forms = dict()
        idx = 0;
        for profile_form in get_profile_forms('candidate', 'invite'):
            step1_forms.update({'invite_contact_%s' % idx : profile_form})
            idx += 1

        step1 = Step('candidate',
            forms = step1_forms,
            template = 'backoffice/wizard/addcandidate/step1.html',
            extra_context={'instance':self.eip.election_instance, }
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
            created, self.candidate = create_profile('candidate', tmp_data)

            #Link candidate to party
            candidacy = Candidacy(
                election_party_instance = get_object_or_404(ElectionInstanceParty, pk=self.election_instance_party_id),
                candidate = self.candidate.user,
                position = self.position,
            )
            candidacy.save()

            #Create invitation
            templates = profile_invite_email_templates('candidate')
            
            #TODO: change invitation text based on created
            
            Invitation.create(
                user_from = request.user,
                user_to = self.candidate.user,
                view = reverse('bo.politician_welcome', kwargs={'eip_id': self.eip.id}),
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

        return redirect('bo.election_party_view', self.election_instance_party_id)
