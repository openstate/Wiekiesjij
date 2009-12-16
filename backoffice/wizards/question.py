import datetime

from django.db import transaction
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404

from utils.multipathform import Step, MultiPathFormWizard

from questions.forms.types import MultipleAnswerForm, BooleanForm, MultipleChoiceForm
from questions.forms import SelectQuestionForm, AnswerQuestionForm
from questions.models import Question
from elections.models import Candidacy
from questions.settings import QUESTION_TYPE_MULTIPLECHOICE, QUESTION_TYPE_MULTIPLEANSWER, QUESTION_TYPE_BOOLEAN, QUESTION_TYPE_RATING, QUESTION_TYPE_CHOICES

from elections.models import ElectionInstance, ElectionInstanceParty, ElectionInstanceQuestion, ElectionInstanceQuestionAnswer
from elections.functions import get_profile_forms, create_profile, profile_invite_email_templates, get_profile_model

class AnswerQuestion(MultiPathFormWizard):
    '''
        AnswerQuestion Wizard.
        Expects two extra obligatory params
        @param int election_instance_party_id - ElectionInstanceParty instance
        @param int user_id - User instance (to couple to Candidate)
    '''
    def __init__(self, *args, **kwargs):
        self.user_id, self.election_instance_party_id = kwargs['user_id'], kwargs['election_instance_party_id']
        self.election_instance_party = ElectionInstanceParty.objects.get(id=self.election_instance_party_id)

        self.user = User.objects.get(id=self.user_id)

        self.candidate_profile = self.user.profile

        # Candidacy to whom the answers are coupled.
        self.candidacy = Candidacy.objects.get(election_party_instance=self.election_instance_party,
                                               candidate=self.user)

        candidate_question_answers = self.candidacy.answers.all()
        candidate_question_answers = map(lambda x: (x.id, x.question_id), candidate_question_answers)

        CandidateProfileClass = get_profile_model('candidate')
        if CandidateProfileClass.__name__ != self.user.profile.__class__.__name__:
            raise Exception

        # Getting all the questions applicable
        questions = self.election_instance_party.election_instance.questions.all()

        steps_tree = []

        # Looping through the questions
        for question in questions:
            try:
                # Here we need to get the answer given for the step
                question_answers = []
                for answer_id, question_id in candidate_question_answers:
                    if question_id == question.id:
                        # I realise that it's kind of stupid loop, 'cause I could use simply filter on the initial list
                        # TODO: rewrite when have time, but it works so as well, although it could be done nicer.
                        # In case of multiple answers we make a list of those.
                        if QUESTION_TYPE_MULTIPLEANSWER == question.question_type:
                            question_answers.append(answer_id)
                        else:
                            question_answers = answer_id
            except Exception, e:
                # Otherwise we shall specify an initial value for it
                question_answers = ''

            step = Step(str(question.id),
                     forms={str(question.id): AnswerQuestionForm},
                     template='backoffice/wizard/question/answer_add/step.html',
                     initial={str(question.id): {'value': question_answers}}, # TODO: Fix this = load the data!
                     extra_context={'question_title': question.title, 'initial': question_answers},
                     form_kwargs={str(question.id): {'question_instance_id': question.id}})
            steps_tree.append(step)

        scenario_tree = None

        for step in steps_tree:
            if None == scenario_tree:
                scenario_tree = step.next()
            else:
                scenario_tree = step.next(scenario_tree)

        template = 'backoffice/wizard/council/edit/base.html',
        super(self.__class__, self).__init__(scenario_tree, template)

    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0

    @transaction.commit_manually
    def done(self, request, form_dict):
        try:
            for path, forms in form_dict.iteritems():
                for question_id, form in forms.iteritems():
                    question = Question.objects.get(id=question_id)
                    answer_value = map(lambda x: x[1], form.cleaned_data.items())[0]

                    # If question type is multiple answers, we need to clean the string list first.
                    if QUESTION_TYPE_MULTIPLEANSWER == question.question_type:
                        answer_values = []
                        for value in answer_value:
                            if value.isdigit():
                                # And we add each answer to the candidacy
                                self.candidacy.answers.add(value)
                    # Otherwise we just add an answer to the candidacy
                    else:
                        self.candidacy.answers.add(answer_value)

        except Exception, e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()
            
        return redirect('bo.answer_question_done')



