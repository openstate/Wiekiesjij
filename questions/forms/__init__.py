from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.forms import widgets

from form_utils.forms import BetterModelForm, BetterForm
from utils.forms import TemplateForm

# TODO make better imports
from questions.models import Question, Answer

class AnswerForm(BetterModelForm, TemplateForm):
    pass

    class Meta:
        model = Answer


class AnswerSelectQuestionForm(BetterModelForm, TemplateForm):
    '''
    Step 1 - we first select a question, then fill the answer.

    Based on the type of the question, we are able to add one or more answers to the question.

    For example, if we try to add more answer to the BooleanField question type, we shall get an exception, because it
    should not be possible.

    For MultipleChoice and MultipleAnswer fields choices shall be unlimited.
    '''
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        #self.fields['value'].widget = widgets.CheckboxSelectMultiple

    class Meta:
        model = Answer
        fields = ('question',)


class AnswerChooseAnswerQuestionForm(BetterModelForm, TemplateForm):
    '''
    Step 2 (see sescription of AnswerSelectQuestionForm).
    '''

    class Meta:
        model = Answer
        fields = ('value',)

