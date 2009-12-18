from form_utils.forms import BetterForm, BetterModelForm

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from utils.widgets import AutoCompleter, ColorPicker, DatePicker, HiddenDateTimePicker, DateTimePicker
from utils.fields import AddressField
from utils.forms import TemplateForm

from elections.models import Party

#from utils.validators import 
#from utils.fields import ZipCodeField, PhoneField
from elections.models import Candidacy, Council, ElectionEvent, ElectionInstance, ElectionInstanceQuestion, Party
from elections.models import ElectionInstanceParty, ElectionInstanceModule

class ElectionInstanceSelectPartiesForm(BetterForm, TemplateForm):
    '''
    Select a list of parties that are in your election from a list of hardcoded partys in the netherlands.
    '''

    parties = forms.MultipleChoiceField(label=_('Parties'), widget=forms.CheckboxSelectMultiple,
                                        choices=settings.COMMON_PARTIES, required=False)

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
        fields = ('name', 'house_num', 'street', 'postcode', 'town', 'email', 'phone', 'website' )

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
    
    seats = forms.IntegerField(label=_('Seats'), required=False, help_text=_('How many seats does the council hold?'))
	
    def __init__(self, *args, **kwargs):
        super(CouncilForm, self).__init__(*args, **kwargs)
        self.fields['history'].widget = forms.widgets.Textarea()
    
    class Meta:
        model = Council
        fields = ('seats', 'history', )

class CouncilContactInformationForm(BetterForm, TemplateForm):
    '''
    Council information form (used in 2. Election overview)
    '''

    name = forms.CharField(label=_('Name'), help_text=_('Specify the name of your council here.'))
    address = AddressField(label=_('Address of the Council'))
    email = forms.EmailField(label=_('E-Mail'))
    website = forms.URLField(label=_('Website of the Council'), required=False)


    class Meta:
        fields = ('name', 'address', 'website',)

class CouncilStylingSetupForm(BetterModelForm, TemplateForm):
    '''
    Council styling setup form (used in 2. Election overview)
    '''

    def __init__(self, *args, **kwargs):
        super(CouncilStylingSetupForm, self).__init__(*args, **kwargs)
        self.fields['background_color'].widget = ColorPicker()
        self.fields['foreground_color'].widget = ColorPicker()
        self.fields['another_color'].widget = ColorPicker()
	
	background_color = forms.CharField(label=_('Background color'), required=False, help_text=_('blah'))

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

    modules = forms.ModelMultipleChoiceField(required=False,
                            label=_('Which modules do you want to enable for this instance?'), 

                            queryset=ElectionInstanceModule.objects,
                            widget=forms.widgets.CheckboxSelectMultiple)

    name = forms.CharField(help_text=_('Insert the name of the municipality here.'))
    region = forms.CharField(label=_('Region'), widget=AutoCompleter(model=Council, field='region'), help_text=_('Probably the same as the name of your municipality.'))
    level = forms.CharField(label=_('Level'), widget=AutoCompleter(model=Council, field='level'), help_text=_('For example for a municipality election, the level would be Municipality.'))
    num_lists = forms.IntegerField(label=_('Number of Parties'))
    
    class Meta:
        model = ElectionInstance
        fields = ('name', 'region', 'level', 'num_lists', 'modules')

class ElectionInstanceForm(BetterModelForm, TemplateForm):
    '''
     ElectionInstance admin
    '''

    start_date = forms.DateTimeField(
        label=_('When does this election take place?'), 
        help_text=_('[Date] is the default date for [Election Event Name].'),
        widget=DateTimePicker)
    start_date.hidden_widget = HiddenDateTimePicker
    website = forms.URLField(label=_('Election Website'), required=False, initial='http://', help_text=_('If your council has a website dedicated to this election, you can specify the URL here.'))
    num_lists = forms.IntegerField(label=_('Number of parties in this election.'), required=False, help_text=_('How many parties are taking part in this election?'))

    class Meta:
        model = ElectionInstance
        fields = ('start_date', 'website', 'num_lists')

class EditElectionInstanceForm(BetterModelForm, TemplateForm):
    """
    EditElectionInstanceForm
    """
    modules = forms.ModelMultipleChoiceField(required=False,
                            label=_('Modules'), 
                            queryset=ElectionInstanceModule.objects,
                            widget=forms.widgets.CheckboxSelectMultiple)
    class Meta:
        model = ElectionInstance
        fields = ('name', 'num_lists', 'modules')

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
        
class InitialElectionPartyForm(BetterForm, TemplateForm):
    name = forms.CharField(label=_('Full party name'), help_text=_('What is the full name of the party?'))
    abbreviation = forms.CharField(label=_('Abbreviated Party Name'), help_text=_('E.g. PvdA or CDA'))
    list_length = forms.IntegerField(label=_('Number of candidates in this election'), min_value=1, max_value=100, help_text=_('The number of positions available for this election'))
    position = forms.IntegerField(widget=forms.widgets.HiddenInput())
    
    
class ElectionPartyContactForm(BetterForm, TemplateForm):
    name = forms.CharField(label=_('Full party name'), widget=AutoCompleter(model=Party, field='name'), help_text=_('What is the full name of your party?'))
    abbreviation = forms.CharField(label=_('Abbreviated party name'), help_text=_('E.g. PvdA or CDA'))
    address = AddressField(label=_('Address'))
    email = forms.EmailField(label=_('E-mail address'))
    telephone = forms.CharField(label=_('Phone number'))
    website = forms.URLField(label=_('Party website'))

class ElectionPartyAdditionalForm(BetterForm, TemplateForm):
    list_length = forms.IntegerField(label=_('Number of candidates in this election'), min_value=0, help_text=_('How many candidates are representing this party in this election?'))
    slogan = forms.CharField(label=_('Slogan'))
    #logo = forms.FileField(_('Logo'))
    num_seats = forms.IntegerField(label=_('Current number of seats'), min_value=0, help_text=_('How many seats does your party currently have in this council?'))


class ElectionPartyDescriptionForm(BetterForm, TemplateForm):
    description = forms.CharField(label=_('Short description'))
    history = forms.CharField(label=_('Short history'))
    manifesto_summary = forms.CharField(label=_('Manifesto Summary'), widget=forms.Textarea())
    manifesto = forms.URLField(label=_('Link to the manifesto'))
    
