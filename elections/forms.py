from form_utils.forms import BetterModelForm
from utils.forms import TemplateForm
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from utils.widgets import AutoCompleter, ColorPicker
from utils.fields import AddressField

from elections.models import Party

#from utils.validators import 
#from utils.fields import ZipCodeField, PhoneField
from elections.models import Candidacy, Council, ElectionEvent, ElectionInstance, ElectionInstanceQuestion, Party

class ElectionInstanceSelectPartiesForm(BetterModelForm, TemplateForm):
    '''
    Select a list of parties that are in your election from a list of hardcoded partys in the netherlands.
    '''
    parties = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=settings.COMMON_PARTIES,)
    print parties
    class Meta:
        fields = ('parties',)


class CandidacyForm(BetterModelForm, TemplateForm):
    '''
    PoliticianProfile admin
    '''

    class Meta:
        model = Candidacy


class InitialCouncilForm(BetterModelForm, TemplateForm):
    '''
    ChanceryProfile admin
    '''
    
    #address = AddressField(_('Address'))

    class Meta:
        model = Council
        fields = ('name', 'house_num', 'street', 'postcode', 'town', 'website' )

    '''
    def clean_address(self):
        """
            Puts the subfields of the address multivaluefield into separate fields
        """
        fields = ['street', 'number', 'postalcode', 'city']
        for key in fields:
            self.cleaned_data[key] = self.cleaned_data['address'].split(' ')[fields.index(key)]
        return self.cleaned_data['address']
    '''
        
class CouncilForm(BetterModelForm, TemplateForm):
    '''
    ChanceryProfile admin
    '''

    class Meta:
        model = Council
        fields = ('seats', 'picture', 'history' )

class CouncilContactInformationForm(BetterModelForm, TemplateForm):
    '''
    Council information form (used in 2. Election overview)
    '''

    class Meta:
        model = Council
        fields = ('name', 'street', 'house_num', 'postcode', 'town', 'website',)

class CouncilStylingSetupForm(BetterModelForm, TemplateForm):
    '''
    Council styling setup form (used in 2. Election overview)
    '''

    def __init__(self, *args, **kwargs):
        super(CouncilStylingSetupForm, self).__init__(*args, **kwargs)
        self.fields['background_color'].widget = ColorPicker()
        self.fields['foreground_color'].widget = ColorPicker()
        self.fields['another_color'].widget = ColorPicker()

    class Meta:
        model = Council
        fields = ('background_color', 'foreground_color', 'another_color',)

class ElectionEventForm(BetterModelForm, TemplateForm):
    '''
    Contact Profile admin
    '''

    class Meta:
        model = ElectionEvent

class InitialElectionInstanceForm(BetterModelForm, TemplateForm):
    '''
     ElectionInstance admin
    '''
    
    MODULE_CHOICES = (
        ('SMS', 'SMS Module'),
    )
    modules = forms.MultipleChoiceField(
                    label=_('Modules'), 
                    choices=MODULE_CHOICES, 
                    widget=forms.widgets.CheckboxSelectMultiple,
                    required=False)
    region = forms.CharField(_('Region'), widget=AutoCompleter(model=Council, field='region'))
    level = forms.CharField(_('Level'), widget=AutoCompleter(model=Council, field='region'))

    class Meta:
        model = ElectionInstance
        fields = ('name', 'region', 'level', 'modules')

class ElectionInstanceForm(BetterModelForm, TemplateForm):
    '''
     ElectionInstance admin
    '''

    class Meta:
        model = ElectionInstance
        fields = ('start_date', 'website' )

class ElectionInstanceQuestionForm(BetterModelForm, TemplateForm):
    '''
    ElectionInstanceQuestion
    '''

    class Meta:
        model = ElectionInstanceQuestion

class PartyForm(BetterModelForm, TemplateForm):
    '''
    Party admin
    '''

    class Meta:
        model = Party
