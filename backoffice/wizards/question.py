import datetime

from django.db import transaction
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404

from utils.multipathform import Step, MultiPathFormWizard

from questions.forms.types import MultipleAnswerForm, BooleanForm, MultipleChoiceForm
from questions.forms import SelectQuestionForm, AnswerQuestionForm
from questions.models import Question

from elections.models import ElectionInstance, ElectionInstanceQuestion, ElectionInstanceQuestionAnswer
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
            '''
            TODO: On each step we shall perform a check to see if step was previously filled in. In case if it was -
            we need to populate the form with existing values and make sure the values are updated (vs. inserted).
            It might make sence to move this to a new wizard, but I'm not sure about it yet.
            Also, since we store the answers as text fields (this one is still questionable - how shall we store the
            answers) we will need to bring them into a proper form before passing to the initials.
            '''
            step = Step(str(question.id),
                     forms={str(question.id): AnswerQuestionForm},
                     template='backoffice/wizard/question/answer_add/step.html',
                     initial={'some_var': ''},
                     extra_context={'question_title': question.title},
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
                    '''
                    question_id is here equal to the question.id
                    form.cleaned_data.items() is posted data
                    self.user_id is user who answers
                    self.election_instance election instance it belongs to
                    So we simply have all the data needed to save it. The only question is where do we save it.
                    '''
                    #import ipdb; ipdb.set_trace()
                    eiq = ElectionInstanceQuestion.objects.get(election_instance=self.election_instance, question=question_id)
                    eiqa = ElectionInstanceQuestionAnswer(election_instance_question=eiq, candidate=self.user,
                                                          answer_value=map(lambda x: x[1], form.cleaned_data.items())[0])
                    eiqa.save()
                    print 'eiq: ', eiq
                    
                    print 'form.cleaned_data.items(): ', form.cleaned_data.items()
        except Exception, e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()
            
        return redirect('bo.answer_question_done')



