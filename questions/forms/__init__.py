import copy

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import widgets
from django.template.loader import render_to_string

from political_profiles.models import RELIGION, GENDERS
from form_utils.forms import BetterModelForm, BetterForm
from utils.formutils import TemplateForm



# TODO make better imports
from questions.exceptions import ModelAnswerFormError
from questions.models import Question, Answer
from questions.settings import MULTIPLE_ANSWER_TYPES, QTYPE_NORM_POLONECHOICE_VISONECHOICE_RANGE, QTYPE_MODEL_POLITICAL_EXPERIENCE_YEARS, QTYPE_MODEL_EDUCATION_LEVEL, QTYPE_MODEL_PROFILE_RELIGION, QTYPE_MODEL_PROFILE_AGE, QTYPE_MODEL_PROFILE_GENDER, QTYPE_NORM_POLONECHOICE_VISONECHOICE, QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE, QTYPE_NORM_POLBOOL_VISBOOL, QUESTION_TYPE_CHOICES

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
            #if question_instance.has_no_preference:
            #choices.append(('no_pref', _('Geen voorkeur')))
            if question_instance.question_type in MULTIPLE_ANSWER_TYPES:
                self.base_fields.update({'value': forms.MultipleChoiceField(label=_('Answer'), widget=widgets.CheckboxSelectMultiple(choices=choices), choices=choices)})
            elif QTYPE_NORM_POLONECHOICE_VISONECHOICE == question_instance.question_type:
                self.base_fields.update({'value': forms.ChoiceField(label=_('Answer'), widget=widgets.RadioSelect(choices=choices), choices=choices)})
            elif QTYPE_NORM_POLBOOL_VISBOOL == question_instance.question_type:
                self.base_fields.update({'value': forms.ChoiceField(label=_('Answer'), widget=widgets.RadioSelect(choices=choices), choices=choices)}) #RadioBoolean() #widgets.NullBooleanSelect()
            elif QTYPE_NORM_POLONECHOICE_VISONECHOICE_RANGE == question_instance.question_type:
                self.base_fields.update({'value': forms.ChoiceField(label=_('Answer'), widget=widgets.RadioSelect(choices=choices), choices=choices)})
            elif QTYPE_MODEL_EDUCATION_LEVEL == question_instance.question_type:
                self.base_fields.update({'value': forms.ChoiceField(label=_('Answer'), widget=widgets.RadioSelect(choices=choices), choices=choices)})

            else:
                #print "This question type doenst know what type of form to show"
                #print question_instance.question_type
                pass #TODO raise error

        else:
            #print "This question type isnt in question type choices"
            pass #TODO raise error
    
        super(AnswerQuestionForm, self).__init__(*args, **kwargs)
        
        
        
    class Meta:
        fields = ('value',)

class PartyMultipleModelChoiceField(forms.ModelMultipleChoiceField):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        return render_to_string('questions/_party_item.html', {'party': obj})
        
class PartyQuestionForm(BetterForm, TemplateForm):
    value = PartyMultipleModelChoiceField(label=_('Answer'), queryset=None, widget=widgets.CheckboxSelectMultiple)
    
    class Meta:
        fieldsets = (('main', {'fields': ('value',), 'legend': '', 'classes': ('default','party-selection')}),)
    def __init__(self, queryset=None, empty_label=_('Geen voorkeur'), *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

        try:
            self.fields['value'].empty_label = empty_label
            self.fields['value'].queryset = queryset

        except Exception:
            raise ModelAnswerFormError('You need to provide a model to the ModelAnswerForm')
            

class MyNoPrefModelChoiceIterator(object):
    def __init__(self, field):
        self.field = field
        self.queryset = field.queryset

    def __iter__(self):
        if self.field.cache_choices:
            if self.field.choice_cache is None:
                self.field.choice_cache = [
                    self.choice(obj) for obj in self.queryset.all()
                ]
            for choice in self.field.choice_cache:
                yield choice
        else:
            for obj in self.queryset.all():
                yield self.choice(obj)
        
        if self.field.empty_label is not None:
            yield (u"no_pref", self.field.empty_label)

    def choice(self, obj):
        if self.field.to_field_name:
            key = obj.serializable_value(self.field.to_field_name)
        else:
            key = obj.pk
        return (key, self.field.label_from_instance(obj))       
        
            
class WorkExpMultipleModelChoiceField(forms.ModelMultipleChoiceField):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        return obj.sector
        
    def _get_choices(self):
        # If self._choices is set, then somebody must have manually set
        # the property self.choices. In this case, just return self._choices.
        if hasattr(self, '_choices'):
            return self._choices
                
        # Otherwise, execute the QuerySet in self.queryset to determine the
        # choices dynamically. Return a fresh QuerySetIterator that has not been
        # consumed. Note that we're instantiating a new QuerySetIterator *each*
        # time _get_choices() is called (and, thus, each time self.choices is
        # accessed) so that we can ensure the QuerySet has not been consumed. This
        # construct might look complicated but it allows for lazy evaluation of
        # the queryset.
        return MyNoPrefModelChoiceIterator(self)
        
    def clean(self, value):
        if 'no_pref' in value:
            return ['no_pref']
        else:
            return super(self.__class__, self).clean(value)

    choices = property(_get_choices, forms.ChoiceField._set_choices)

class WorkTypeQuestionForm(BetterForm, TemplateForm):
    value = WorkExpMultipleModelChoiceField(label=_('Answer'), queryset=None, widget=widgets.CheckboxSelectMultiple)

    class Meta:
        fieldsets = (('main', {'fields': ('value',), 'legend': '', 'classes': ('default','party-selection')}),)
    def __init__(self, queryset=None, empty_label=_('Geen voorkeur'), *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

        try:
            self.fields['value'].empty_label = empty_label
            self.fields['value'].queryset = queryset

        except Exception:
            raise ModelAnswerFormError('You need to provide a model to the ModelAnswerForm')


class PolExpMultipleModelChoiceField(forms.ModelMultipleChoiceField):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        return obj.type
        
    def _get_choices(self):
        # If self._choices is set, then somebody must have manually set
        # the property self.choices. In this case, just return self._choices.
        if hasattr(self, '_choices'):
            return self._choices

        # Otherwise, execute the QuerySet in self.queryset to determine the
        # choices dynamically. Return a fresh QuerySetIterator that has not been
        # consumed. Note that we're instantiating a new QuerySetIterator *each*
        # time _get_choices() is called (and, thus, each time self.choices is
        # accessed) so that we can ensure the QuerySet has not been consumed. This
        # construct might look complicated but it allows for lazy evaluation of
        # the queryset.
        return MyNoPrefModelChoiceIterator(self)
        
    def clean(self, value):
        if 'no_pref' in value:
            return ['no_pref']
        else:
            return super(self.__class__, self).clean(value)
            
    choices = property(_get_choices, forms.ChoiceField._set_choices)

class PolTypeQuestionForm(BetterForm, TemplateForm):
    value = PolExpMultipleModelChoiceField(label=_('Answer'), queryset=None, widget=widgets.CheckboxSelectMultiple)

    class Meta:
        fieldsets = (('main', {'fields': ('value',), 'legend': '', 'classes': ('default','party-selection')}),)
    def __init__(self, queryset=None, empty_label=_('Geen voorkeur'), *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

        try:
            self.fields['value'].empty_label = empty_label
            self.fields['value'].queryset = queryset

        except Exception:
            raise ModelAnswerFormError('You need to provide a model to the ModelAnswerForm')

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
            if QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE == question_instance.question_type:
                self.base_fields.update({'value': forms.MultipleChoiceField(label=_('Answer'), widget=widgets.CheckboxSelectMultiple(choices=choices), choices=choices)})
            elif QTYPE_NORM_POLONECHOICE_VISONECHOICE == question_instance.question_type:
                self.base_fields.update({'value': forms.ChoiceField(label=_('Answer'), widget=widgets.RadioSelect(choices=choices), choices=choices)})
            elif QTYPE_NORM_POLONECHOICE_VISONECHOICE_RANGE == question_instance.question_type:
                self.base_fields.update({'value': forms.ChoiceField(label=_('Answer'), widget=widgets.RadioSelect(choices=choices), choices=choices)})
            elif QTYPE_NORM_POLBOOL_VISBOOL == question_instance.question_type:
                self.base_fields.update({'value': forms.ChoiceField(label=_('Answer'), widget=widgets.RadioSelect(choices=choices), choices=choices)}) #RadioBoolean() #widgets.NullBooleanSelect()
            elif QTYPE_MODEL_POLITICAL_EXPERIENCE_YEARS == question_instance.question_type:
                self.base_fields.update({'value': forms.ChoiceField(label=_('Answer'), widget=widgets.RadioSelect(choices=choices), choices=choices)})
            elif QTYPE_MODEL_PROFILE_RELIGION == question_instance.question_type:
                RELIGION_A = copy.deepcopy(RELIGION)
                RELIGION_A.append(('no_pref', _('Geen voorkeur')))
                self.base_fields.update({'value': forms.MultipleChoiceField(label=_('Answer'), widget=widgets.CheckboxSelectMultiple(choices=RELIGION_A), choices=RELIGION_A)})
            elif QTYPE_MODEL_PROFILE_AGE == question_instance.question_type:
                self.base_fields.update({'value': forms.ChoiceField(label=_('Answer'), widget=widgets.RadioSelect(choices=choices), choices=choices)})
            elif QTYPE_MODEL_PROFILE_GENDER == question_instance.question_type:
                GENDERS_A = copy.deepcopy(GENDERS)
                GENDERS_A.append(('no_pref', _('Geen voorkeur')))
                self.base_fields.update({'value': forms.ChoiceField(label=_('Answer'), widget=widgets.RadioSelect(choices=GENDERS_A), choices=GENDERS_A)})
            elif QTYPE_MODEL_EDUCATION_LEVEL == question_instance.question_type:
                self.base_fields.update({'value': forms.ChoiceField(label=_('Answer'), widget=widgets.RadioSelect(choices=choices), choices=choices)})
            else:
                pass #TODO raise error

        else:
            pass #TODO raise error

        super(VisitorAnswerQuestionForm, self).__init__(*args, **kwargs)



    class Meta:
        fields = ('value',)