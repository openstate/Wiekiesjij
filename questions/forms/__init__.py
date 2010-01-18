from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.forms import widgets
from utils.widgets import RadioRating, RadioBoolean
from political_profiles.models import RELIGION, GENDERS
from form_utils.forms import BetterModelForm, BetterForm
from utils.formutils import TemplateForm
import copy
# TODO make better imports
from questions.models import Question, Answer
from questions.settings import QTYPE_MODEL_WORK_EXPERIENCE_YEARS, QTYPE_MODEL_EDUCATION_LEVEL, QTYPE_MODEL_PROFILE_RELIGION, QTYPE_MODEL_PROFILE_HOBBY, QTYPE_MODEL_PROFILE_AGE, QTYPE_MODEL_PROFILE_GENDER, QTYPE_NORM_POLMULTICHOICE_VISONECHOICE, QTYPE_NORM_POLONECHOICE_VISMULTICHOICE, QTYPE_NORM_POLONECHOICE_VISONECHOICE, QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE, QTYPE_NORM_POLBOOL_VISBOOL, QTYPE_MODEL_POLMULTICHOICE_VISONECHOICE, QTYPE_MODEL_POLONECHOICE_VISMULTICHOICE, QTYPE_SYSTEM_POLMULTICHOICE_VISONECHOICE, QUESTION_TYPE_CHOICES 

class SelectQuestionForm(BetterModelForm, TemplateForm):
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


class AnswerQuestionForm(BetterForm, TemplateForm):
    '''
        Form which displays possible answers, coupled to the question given. It makes sure the answer has the
        right widget, which depends on the question type.
    '''
    def __init__(self, question_instance_id, *args, **kwargs):
        
        question_types = dict(QUESTION_TYPE_CHOICES)

        question_instance = Question.objects.get(id=question_instance_id)

        if not question_instance:
            return

        if question_instance.question_type in question_types:
            choices = map(lambda x: (x.id, x.value), question_instance.answers.all())

            if QTYPE_NORM_POLONECHOICE_VISMULTICHOICE == question_instance.question_type:
                self.base_fields.update({'value': forms.MultipleChoiceField(label=_('Answer'), widget=widgets.CheckboxSelectMultiple(choices=choices), choices=choices)})
            elif QTYPE_NORM_POLMULTICHOICE_VISONECHOICE == question_instance.question_type:
                self.base_fields.update({'value': forms.ChoiceField(label=_('Answer'), widget=widgets.RadioSelect(choices=choices), choices=choices)})
            elif QTYPE_NORM_POLBOOL_VISBOOL == question_instance.question_type:
                self.base_fields.update({'value': forms.ChoiceField(label=_('Answer'), widget=widgets.RadioSelect(choices=choices), choices=choices)}) #RadioBoolean() #widgets.NullBooleanSelect()
            else:
                pass #TODO raise error

        else:
            pass #TODO raise error
    
        super(AnswerQuestionForm, self).__init__(*args, **kwargs)
        
        
        
    class Meta:
        fields = ('value',)



class VisitorAnswerQuestionForm(BetterForm, TemplateForm):
    '''
        Form which displays possible answers, coupled to the question given (for Vistiors). It makes sure the answer has the
        right widget, which depends on the question type.
    '''
    def __init__(self, question_instance_id, *args, **kwargs):

        question_types = dict(QUESTION_TYPE_CHOICES)

        question_instance = Question.objects.get(id=question_instance_id)
        
        if not question_instance:
            return

        if question_instance.question_type in question_types:
            choices = map(lambda x: (x.id, x.get_frontoffice_value()), question_instance.answers.all())
            if question_instance.has_no_preference:
                choices.append(('no_pref', _('Geen voorkeur')))
            if QTYPE_NORM_POLONECHOICE_VISMULTICHOICE == question_instance.question_type:
                self.base_fields.update({'value': forms.MultipleChoiceField(label=_('Answer'), widget=widgets.CheckboxSelectMultiple(choices=choices), choices=choices)})
            elif QTYPE_NORM_POLMULTICHOICE_VISONECHOICE == question_instance.question_type:
                self.base_fields.update({'value': forms.ChoiceField(label=_('Answer'), widget=widgets.RadioSelect(choices=choices), choices=choices)})
            elif QTYPE_NORM_POLBOOL_VISBOOL == question_instance.question_type:
                self.base_fields.update({'value': forms.ChoiceField(label=_('Answer'), widget=widgets.RadioSelect(choices=choices), choices=choices)}) #RadioBoolean() #widgets.NullBooleanSelect()
            elif QTYPE_MODEL_WORK_EXPERIENCE_YEARS == question_instance.question_type:
                self.base_fields.update({'value': forms.ChoiceField(label=_('Answer'), widget=widgets.RadioSelect(choices=choices), choices=choices)})
            elif QTYPE_MODEL_PROFILE_RELIGION == question_instance.question_type:
                RELIGION_A = copy.deepcopy(RELIGION)
                RELIGION_A.append(('no_pref', _('Geen voorkeur')))
                self.base_fields.update({'value': forms.MultipleChoiceField(label=_('Answer'), widget=widgets.CheckboxSelectMultiple(choices=RELIGION), choices=RELIGION_A)})
            elif QTYPE_MODEL_PROFILE_AGE == question_instance.question_type:
                self.base_fields.update({'value': forms.ChoiceField(label=_('Answer'), widget=widgets.RadioSelect(choices=choices), choices=choices)})
            elif QTYPE_MODEL_PROFILE_GENDER == question_instance.question_type:
                GENDERS_A = copy.deepcopy(GENDERS)
                GENDERS_A.append(('no_pref', _('Geen voorkeur')))
                self.base_fields.update({'value': forms.ChoiceField(label=_('Answer'), widget=widgets.RadioSelect(choices=GENDERS), choices=GENDERS_A)})

            else:
                pass #TODO raise error

        else:
            pass #TODO raise error

        super(VisitorAnswerQuestionForm, self).__init__(*args, **kwargs)



    class Meta:
        fields = ('value',)