import datetime

from django.db import transaction
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404

from utils.multipathform import Step, MultiPathFormWizard

from questions.forms.types import MultipleAnswerForm, BooleanForm, MultipleChoiceForm
from questions.forms import AnswerForm, AnswerSelectQuestionForm, AnswerChooseAnswerQuestionForm

class AnswerAddWizard(MultiPathFormWizard):
    def __init__(self, *args, **kwargs):
        step1 = Step('select_question',
                     forms={'answer_add': AnswerSelectQuestionForm},
                     template='backoffice/wizard/council/edit/step1.html',
                     initial={})

        step2 = Step('choose_answer',
                     forms={'answer_add': AnswerChooseAnswerQuestionForm},
                     template='backoffice/wizard/council/edit/step1.html',
                     initial={})

        scenario_tree = step1.next(step2.next())

        template = 'backoffice/wizard/council/edit/base.html',

        super(self.__class__, self).__init__(scenario_tree, template)

    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0


    def done(self, request, form_dict):
        return redirect('')


class QuestionTestWizard(MultiPathFormWizard):
    """
    Wizard to test forms
    """
    def __init__(self, *args, **kwargs):
        step1_choices =  (('1', '1'),
                          ('2', '2'),
                          ('3', '3'),
                          ('4', '4'),
                          ('5', '5'),
                          ('6', '6'),
                          ('7', '7'),
                          ('8', '8'),
                          ('9', '9'),
                          ('10', '10'),
                          ('11', '11'),)
        step1_answers = {}
        # Updates Council contact information
        step1_form = MultipleAnswerForm(choices=step1_choices)
        step1 = Step('test_multiple_answer',
                     forms={'test_multiple_answer': MultipleAnswerForm},
                     template='backoffice/wizard/council/edit/step1.html',
                     initial={'test_multiple_answer': {'answer': step1_answers}})
        # Updates Council additional information
        step2 = Step('test_multiple_choice',
                     forms={'test_multiple_choice': MultipleChoiceForm},
                     template='backoffice/wizard/council/edit/step1.html',
                     initial={'test_multiple_choice': {'answer': step1_answers}})
        # Updates Council styling setup
        step3 = Step('test_boolean',
                     forms={'test_boolean': BooleanForm},
                     template='backoffice/wizard/council/edit/step1.html',
                     initial={'test_boolean': ''})

        scenario_tree = step1.next(step2.next(step3))

        template = 'backoffice/wizard/council/edit/base.html',

        super(self.__class__, self).__init__(scenario_tree, template)

    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0


    def done(self, request, form_dict):
        return redirect('')

