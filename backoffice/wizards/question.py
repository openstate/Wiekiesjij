import datetime

from django.db import transaction
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404

from utils.multipathform import Step, MultiPathFormWizard

from questions.forms.types import MultipleAnswerForm, BooleanForm, MultipleChoiceForm
from questions.forms import SelectQuestionForm, AnswerQuestionForm
from questions.models import Question

from elections.models import ElectionInstance, ElectionInstanceQuestionAnswer
from elections.functions import get_profile_forms, create_profile, profile_invite_email_templates, get_profile_model

class AnswerQuestion(MultiPathFormWizard):
    def __init__(self, *args, **kwargs):
        self.user_id, self.election_instance_id = kwargs['user_id'], kwargs['election_instance_id']
        self.election_instance = ElectionInstance.objects.get(id=self.election_instance_id)

        self.user = User.objects.get(id=self.user_id)

        self.candidate_profile = self.user.profile

        CandidateProfileClass = get_profile_model('candidate')
        if CandidateProfileClass.__name__ != self.user.profile.__class__.__name__:
            raise Exception

        questions = self.election_instance.questions.all()

        steps_tree = list()
        for question in questions:
            step = Step(str(question.id),
                     forms={str(question.id): AnswerQuestionForm},
                     template='backoffice/wizard/council/edit/step1.html',
                     initial={'some_var': ''},
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
                for name, form in forms.iteritems():
                    # Name is here equal to the question.id
                    # form.cleaned_data.items() is posted data
                    print 'form.cleaned_data.items(): ', form.cleaned_data.items()
        except Exception, e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()
            
        return redirect(reverse(''))



