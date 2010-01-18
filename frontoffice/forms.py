from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _

from political_profiles.models import RELIGION, DIET, MARITAL_STATUS, GENDERS
from political_profiles.models import EducationLevel
import copy
from form_utils.forms import BetterForm
from utils.formutils import TemplateForm
from utils.fields import NameField

from elections.models import ElectionInstance

class RegionChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.council.region

class MobilePhoneField(forms.CharField):

    def clean(self, data):
        phone = super(MobilePhoneField, self).clean(data)
        phone = phone.strip()
        if not phone[:2] == '06':
            raise forms.ValidationError(_('Mobile phone numbers should start with 06'))
        if not len(phone) == 10:
            raise forms.ValidationError(_('Mobile phone numbers should have 10 digits'))
        if not phone.isdigit():
            raise forms.ValidationError(_('Mobile phone numbers should only have digits'))
        return phone

    def __init__(self, *args, **kwargs):
        super(MobilePhoneField, self).__init__(*args, **kwargs)


class PoliticianFilterForm(BetterForm, TemplateForm):
    '''
    PoliticianFilter Form - used in the filtering and searching of candidates.
    '''
    either = ('---------', _('---------'))
    GENDERS_A = copy.deepcopy(GENDERS)
    GENDERS_A.insert(0,('All', _('All')),)
    DIET_A = DIET
    DIET_A.insert(0,either,)
    RELIGION_A = copy.deepcopy(RELIGION)
    RELIGION_A.insert(0,either,)
    MARITAL_STATUS_A = copy.deepcopy(MARITAL_STATUS)
    MARITAL_STATUS_A.insert(0,either,)


    name = forms.CharField(label=_('Name'), required=False)
    election_instances = ElectionInstance.objects.filter(election_event = settings.ELECTIONS_ELECTION_EVENT_ID)
    region = RegionChoiceField(queryset=election_instances, label=_('Region'), required=False)
    gender = forms.CharField(label=_('Gender'), widget=forms.widgets.RadioSelect(choices=GENDERS), required=False)
    start_age = forms.IntegerField(label=_('Lowest Age'), required=False)
    end_age = forms.IntegerField(label=_('Oldest Age'), required=False)
    marital_status = forms.ChoiceField(label=_('Marital Status'), choices=MARITAL_STATUS, required=False)
    #children = forms.NullBooleanField(label=_('Children'), widget=forms.widgets.NullBooleanSelect(), required=False )
    children = forms.ChoiceField(label=_('Children'), choices=[('---------', _('---------')), (1, _('Yes')), (2, _('No')),], required=False )
    religion = forms.ChoiceField(choices=RELIGION_A, label=_('Religon'), required=False)
    education = forms.ModelChoiceField(queryset=EducationLevel.objects, label=_('Education Level'), required=False)
    political_exp_years = forms.IntegerField(label=_('Years of political experience'), required=False)
    work_exp_years = forms.IntegerField(label=_('Years of work experience'), required=False)
    #smoker = forms.BooleanField(label=_('Smoker'), widget=forms.widgets.NullBooleanSelect(), required=False)
    smoker = forms.ChoiceField(label=_('Smoker'), choices=[('---------', _('---------')), (1, _('Yes')), (2, _('No')),], required=False )
    diet = forms.ChoiceField(choices=DIET, label=_('Diet'), required=False)
    goals = forms.CharField(label=_('Goals'), required=False)


class VisitorProfileForm(BetterForm, TemplateForm):
    name        = NameField(label=_('Name'))
    phone       = MobilePhoneField(label=_('Mobile phone number'))
    send_text   = forms.BooleanField(label=_('Receive text messages?'), required=False)
    