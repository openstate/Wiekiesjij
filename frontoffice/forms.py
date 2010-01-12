from django import forms
from django.utils.translation import ugettext_lazy as _
from political_profiles.models import MOTIVATION, CHURCH, DIET, LIFE_STANCE, MARITAL_STATUS, GENDERS, NEWSPAPER, TRANSPORT, CHARITY, MEDIA, SPORT, HOBBIES , CLUBS, PETS
from political_profiles.models import EducationLevel, PoliticianProfile
from utils.widgets import AutoCompleter
from form_utils.forms import BetterModelForm, BetterForm
from utils.fields import NameField
from utils.formutils import TemplateForm
from django.conf import settings
from django.contrib.comments.forms import CommentForm
from elections.models import ElectionInstance

class RegionChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.council.region

class PoliticianFilterForm(BetterForm, TemplateForm):
    '''
    PoliticianFilter Form - used in the filtering and searching of candidates.
    '''
    either = ('---------', _('---------'))
    GENDERS_A = GENDERS
    GENDERS_A.insert(0,('All', _('All')),)
    DIET_A = DIET
    DIET_A.insert(0,either,)
    CHURCH_A = CHURCH
    CHURCH_A.insert(0,either,)
    MARITAL_STATUS_A =MARITAL_STATUS
    MARITAL_STATUS_A.insert(0,either,)
    LIFE_STANCE_A = LIFE_STANCE
    LIFE_STANCE_A.insert(0, either,)

    name = forms.CharField(label=_('Name'), required=False)
    election_instances = ElectionInstance.objects.filter(election_event = settings.ELECTIONS_ELECTION_EVENT_ID)
    region = RegionChoiceField(queryset=election_instances, label=_('Level'), required=False)
    gender = forms.CharField(label=_('Gender'), widget=forms.widgets.RadioSelect(choices=GENDERS_A), required=False)
    start_age = forms.IntegerField(label=_('Lowest Age'), required=False)
    end_age = forms.IntegerField(label=_('Oldest Age'), required=False)
    marital_status = forms.ChoiceField(label=_('Marital Sataus'), choices=MARITAL_STATUS, required=False)
    #children = forms.NullBooleanField(label=_('Children'), widget=forms.widgets.NullBooleanSelect(), required=False )
    children = forms.ChoiceField(label=_('Children'), choices=[('---------', _('---------')), (1, _('Yes')), (2, _('No')),], required=False )
    life_stance = forms.ChoiceField(label=_('Life Stance'), choices=LIFE_STANCE, required=False)
    religion = forms.ChoiceField(choices=CHURCH, label=_('Religon'), required=False)
    education = forms.ModelChoiceField(queryset=EducationLevel.objects, label=_('Education Level'), required=False)
    political_exp_years = forms.IntegerField(label=_('Years of political experience'), required=False)
    work_exp_years = forms.IntegerField(label=_('Years of work experience'), required=False)
    #smoker = forms.BooleanField(label=_('Smoker'), widget=forms.widgets.NullBooleanSelect(), required=False)
    smoker = forms.ChoiceField(label=_('Smoker'), choices=[('---------', _('---------')), (1, _('Yes')), (2, _('No')),], required=False )
    diet = forms.ChoiceField(choices=DIET, label=_('Diet'), required=False)
    goals = forms.CharField(label=_('Goals'), required=False)
