from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.forms import widgets

from form_utils.forms import BetterModelForm, BetterForm
from utils.formutils import TemplateForm

class MultipleAnswerForm(BetterForm, TemplateForm):
    answer = forms.MultipleChoiceField(widget=widgets.CheckboxSelectMultiple)
    
    def __init__(self, choices=None, *args, **kwargs):
        default_choices =  (('1', '1-def'),
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
        if not choices:
            super(self.__class__, self).__init__(*args, **kwargs)
            self.fields['answer'].choices = default_choices
        else:
            super(self.__class__, self).__init__(*args, **kwargs)
            self.fields['answer'].choices = choices

class BooleanForm(BetterForm, TemplateForm):
    answer = forms.BooleanField()

class MultipleChoiceForm(BetterForm, TemplateForm):
    answer = forms.MultipleChoiceField()

class RatingForm(BetterForm, TemplateForm):
    def __init__(self):
        raise NotImplementedError('RatingForm answer is not implemented')