from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import widgets

from form_utils.forms import BetterForm
from utils.formutils import TemplateForm
from questions.exceptions import ModelAnswerFormError
from questions.settings import PROFILE_QUESTION_WEIGHT_OPTIONS
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


class GenerateModelChoiceField(forms.ModelChoiceField):
    def __init__(self, attribute=None, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.attribute = attribute

    def label_from_instance(self, obj):
        if self.attribute:
            return getattr(obj, self.attribute)
        return obj


class GenerateMultipleModelChoiceField(forms.ModelMultipleChoiceField):
    def __init__(self, attribute=None, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.attribute = attribute

    def label_from_instance(self, obj):
        if self.attribute:
            return getattr(obj, self.attribute)
        return obj

class ModelMultiAnswerForm(BetterForm, TemplateForm):
    value = GenerateMultipleModelChoiceField(queryset=None, widget=widgets.CheckboxSelectMultiple)
    
    def __init__(self, queryset=None, attribute=None, empty_label=_('Geen voorkeur'), *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

        try:
            self.fields['value'].attribute=attribute
            self.fields['value'].empty_label = empty_label
            self.fields['value'].queryset = queryset

        except Exception:
            raise ModelAnswerFormError(_('You need to provide a model to the ModelMiltiAnswerForm'))

class ModelAnswerForm(BetterForm, TemplateForm):
    value = GenerateModelChoiceField(queryset=None, widget=widgets.RadioSelect)

    def __init__(self, queryset=None, attribute=None, empty_label=_('Geen voorkeur'), *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


        try:
            self.fields['value'].attribute=attribute
            self.fields['value'].empty_label = empty_label
            self.fields['value'].queryset = queryset

        except Exception:
            raise ModelAnswerFormError(_('You need to provide a model to the ModelAnswerForm'))


class ThemeAnswerForm(BetterForm, TemplateForm):
    value = forms.MultipleChoiceField(widget=widgets.CheckboxSelectMultiple)

    def __init__(self, queryset=None, attribute=None, empty_label=_('Geen voorkeur'), *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        choices = []
        if queryset:
            choices = []
            for object in queryset:
                for choice in PROFILE_QUESTION_WEIGHT_OPTIONS:
                    if object.theme == choice[0]:
                        if choice not in choices:
                            choices.append(choice)
        
        self.fields['value'].widget=widgets.CheckboxSelectMultiple(choices=choices)
        self.fields['value'].choices = choices
        self.fields['value'].label=_('Answer')
        self.fields['value'].required = False

class BooleanForm(BetterForm, TemplateForm):
    answer = forms.BooleanField()

class MultipleChoiceForm(BetterForm, TemplateForm):
    answer = forms.MultipleChoiceField()

class RatingForm(BetterForm, TemplateForm):
    def __init__(self):
        raise NotImplementedError('RatingForm answer is not implemented')