from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.forms import widgets

from form_utils.forms import BetterModelForm, BetterForm
from utils.forms import TemplateForm

# TODO make better imports
from questions.models import Question, Answer
from questions.settings import QUESTION_TYPE_MULTIPLECHOICE, QUESTION_TYPE_MULTIPLEANSWER, QUESTION_TYPE_BOOLEAN, QUESTION_TYPE_RATING, QUESTION_TYPE_CHOICES

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
    #answer = forms.
    def __init__(self, question_instance=None, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        # Add here?

        question_types = dict(QUESTION_TYPE_CHOICES)

        if question_instance.question_type in question_types:
            choices = map(lambda x: (x.id, x.value), question_instance.answers.all())
            if QUESTION_TYPE_MULTIPLEANSWER == question_instance.question_type:
                self.fields['value'].widget = widgets.CheckboxSelectMultiple(choices=choices)
            elif QUESTION_TYPE_MULTIPLECHOICE == question_instance.question_type:
                self.fields['value'].widget = widgets.CheckboxInput(choices=choices)
            elif QUESTION_TYPE_BOOLEAN == question_instance.question_type:
                self.fields['value'].widget = widgets.NullBooleanSelect()
            else:
                pass

        else:
            pass #TODO raise error

    class Meta:
        model = Answer
        fields = ('value',)

