from django import forms
from django.utils.translation import ugettext_lazy as _
from political_profiles.models import MOTIVATION, CHURCH, DIET, LIFE_STANCE, MARITAL_STATUS, GENDERS, NEWSPAPER, TRANSPORT, CHARITY, MEDIA, SPORT, HOBBIES , CLUBS, PETS
from political_profiles.models import EducationLevel, PoliticianProfile
from utils.widgets import AutoCompleter
from form_utils.forms import BetterModelForm, BetterForm
from utils.fields import NameField
from utils.formutils import TemplateForm

class PoliticianFilterForm(BetterForm, TemplateForm):
    '''
    PoliticianFilter Form - used in the filtering and searching of candidates.
    '''
    GENDERS = (
        ('Male',_('Male')),
        ('Female', _('Female')),
        ('Either', _('Either')),
        )

    name = forms.CharField(label=_('Name'), required=False)

    region = forms.ChoiceField(choices=CHURCH, label=_('Regions'), required=False)
    
    start_age = forms.IntegerField(label=_('Lowest Age'), required=False)
    end_age = forms.IntegerField(label=_('Oldest Age'), required=False)
    gender = forms.CharField(label=_('Gender'), widget=forms.widgets.RadioSelect(choices=GENDERS), required=False)
    children = forms.NullBooleanField(label=_('Children'), widget=forms.widgets.NullBooleanSelect(), required=False )
    political_exp_years = forms.IntegerField(label=_('Years of political experience'), required=False)
    smoker = forms.BooleanField(label=_('Smoker'), widget=forms.widgets.NullBooleanSelect(), required=False)
    #smoker = forms.BooleanField(label=_('Smoker'), widget=forms.widgets.RadioSelect(choices=[(1, _('Yes')), (2, _('No'))]), required=False )
    diet = forms.ChoiceField(choices=DIET, label=_('Diet'), required=False)
    religion = forms.ChoiceField(choices=CHURCH, label=_('Religon'), required=False)
    education = forms.ModelChoiceField(queryset=EducationLevel.objects, label=_('Level'), required=False)