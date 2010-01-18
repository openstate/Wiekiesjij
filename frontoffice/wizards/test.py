import datetime

from django.db import transaction
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from utils.multipathform import Step, MultiPathFormWizard

from questions.forms.types import MultipleAnswerForm, BooleanForm, MultipleChoiceForm
from questions.forms import SelectQuestionForm, VisitorAnswerQuestionForm
from questions.forms.types import ModelMultiAnswerForm
from questions.models import Question
from elections.models import Candidacy, ElectionInstanceParty
from questions.settings import QUESTION_TYPE_CHOICES, QTYPE_MODEL_WORK_EXPERIENCE_YEARS, QTYPE_MODEL_EDUCATION_LEVEL, QTYPE_MODEL_PROFILE_RELIGION, QTYPE_MODEL_PROFILE_HOBBY, QTYPE_MODEL_PROFILE_AGE, QTYPE_MODEL_PROFILE_GENDER, QTYPE_MODEL_PARTY, QTYPE_NORM_POLONECHOICE_VISMULTICHOICE
from questions.settings import FRONTOFFICE_QUESTION_TYPES, BACKOFFICE_QUESTION_TYPES
from political_profiles.models import WorkExperienceSector, EducationLevel, PoliticianProfile 

from elections.models import ElectionInstance, ElectionInstanceParty, ElectionInstanceQuestion, ElectionInstanceQuestionAnswer
from elections.functions import get_profile_forms, create_profile, profile_invite_email_templates, get_profile_model
from types import ListType

class BestCandidate(MultiPathFormWizard):
    '''
        BestCandidate Wizard.
    '''
    def __init__(self, *args, **kwargs):
        self.election_instance_id = kwargs['election_instance_party_id']
        self.election_instance = ElectionInstance.objects.get(id=self.election_instance_id)
        eips = ElectionInstanceParty.objects.filter(election_instance=self.election_instance)  
        elections_candidates = Candidacy.objects.filter(election_party_instance__in=eips)
        users = User.objects.filter(pk__in=elections_candidates)
        candidates = PoliticianProfile.objects.filter(user__in=users)


        questions = self.election_instance.questions.filter(question_type__in=FRONTOFFICE_QUESTION_TYPES).order_by('-electioninstancequestion__position')
        steps_tree = []

        # Looping through the questions
        idx = 1;

        for question in questions:
            
            if question.has_no_preference:
                empty_label = _('Geen voorkeur')
            else:
                empty_label=None
            if question.question_type in BACKOFFICE_QUESTION_TYPES:
                form = {str(question.id): VisitorAnswerQuestionForm}
                fkwargs={str(question.id): {'question_instance_id': question.id}}

            elif QTYPE_MODEL_PARTY == question.question_type:
                form = {str(question.id): ModelMultiAnswerForm}

                fkwargs= {str(question.id): {'queryset': self.election_instance.parties, 'attribute':'name', 'empty_label':empty_label}}

            elif QTYPE_MODEL_WORK_EXPERIENCE_YEARS == question.question_type:
                form = {str(question.id): VisitorAnswerQuestionForm}
                fkwargs={str(question.id): {'question_instance_id': question.id}}

            elif QTYPE_MODEL_EDUCATION_LEVEL == question.question_type:
                form = {str(question.id): ModelMultiAnswerForm}
                fkwargs= {str(question.id): {'queryset': EducationLevel.objects.all(), 'attribute':'level'}}

            elif QTYPE_MODEL_PROFILE_RELIGION == question.question_type:
                form = {str(question.id): VisitorAnswerQuestionForm}
                fkwargs={str(question.id): {'question_instance_id': question.id}}

            elif QTYPE_MODEL_PROFILE_HOBBY == question.question_type:
                form = {str(question.id): ModelMultiAnswerForm}
                fkwargs={str(question.id): {'queryset': candidates, 'attribute':'hobby', 'empty_label':empty_label}}

            elif QTYPE_MODEL_PROFILE_AGE == question.question_type:
                form = {str(question.id): VisitorAnswerQuestionForm}
                fkwargs={str(question.id): {'question_instance_id': question.id}}

            elif QTYPE_MODEL_PROFILE_GENDER == question.question_type:
                form = {str(question.id): VisitorAnswerQuestionForm}
                fkwargs={str(question.id): {'question_instance_id': question.id}}
            else:
                pass
            step = Step(str(question.id),
                     forms=form,
                     template='frontoffice/wizard/test/step1.html',
                     #initial={str(question.id): {'value': question_answers}}, # TODO: Fix this = load the data!
                     extra_context={'questions': range(0, questions.count()), 'current_question': questions.count() - idx, 'question_title': question.get_frontend_title()},
                     form_kwargs=fkwargs)
            steps_tree.append(step)
            idx += 1

        scenario_tree = None
        for step in steps_tree:
            if None == scenario_tree:
                scenario_tree = step.next()
            else:
                scenario_tree = step.next(scenario_tree)

        template = 'frontoffice/wizard/base.html',
        super(BestCandidate, self).__init__(scenario_tree, template)

    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0

    @transaction.commit_manually
    def done(self, request, form_dict):

        for path, forms in form_dict.iteritems():
            for question_id, form in forms.iteritems():
                question = Question.objects.get(id=question_id)
                answer_value = form.cleaned_data['value']
                list(answer_value)
                for value in answer_value:
                    answer = value
                        



            
        return redirect('fo.test', election_instance_id=self.election_instance_id)



