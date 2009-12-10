from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from form_utils.forms import BetterModelForm
from utils.forms import TemplateForm
from utils.widgets import AutoCompleter, ColorPicker
from utils.fields import NameField, AddressField
from political_profiles.models import PoliticalExperience, Education, WorkExperience, Link, Interest, Appearence, PoliticianProfile, ChanceryProfile, ContactProfile, VisitorProfile

class PoliticianProfileForm(BetterModelForm, TemplateForm):
    '''
    PoliticianProfile admin
    '''

    def __init__(self, *args, **kwargs):
        super(PoliticianProfileForm, self).__init__(*args, **kwargs)
        #self.fields['first_name'].widget = AutoCompleter(model = PoliticianProfile, field='first_name')
        self.fields['introduction'].widget = forms.Textarea()
        self.fields['motivation'].widget = forms.Textarea()
        self.fields['gender'].widget = forms.widgets.RadioSelect(choices=self.fields['gender'].choices)

    class Meta:
        model = PoliticianProfile
        exclude = ('user', 'level', 'picture' )


class InitialPoliticianProfileForm(BetterModelForm, TemplateForm):
    '''
    ChanceryProfile admin
    '''
    name = NameField(label=_('Name'))
    email = forms.EmailField(_('Email'))

    def __init__(self, *args, **kwargs):
        super(InitialPoliticianProfileForm, self).__init__(*args, **kwargs)
        self.fields['gender'].widget = forms.widgets.RadioSelect(choices=self.fields['gender'].choices)
        self.fields['email'].help_text = 'Invitation will be sent to this address'
    
    class Meta:
        model = PoliticianProfile
        fields = ('name', 'email', 'gender' )

class InitialChanceryProfileForm(BetterModelForm, TemplateForm):
    '''
    ChanceryProfile admin
    '''
    
    name = NameField(label=_('Name'))
    email = forms.EmailField(_('Email'))
    
    def __init__(self, *args, **kwargs):
        import ipdb; ipdb.set_trace()
        super(InitialChanceryProfileForm, self).__init__(*args, **kwargs)
        self.fields['gender'].widget = forms.widgets.RadioSelect(choices=self.fields['gender'].choices)
    
    class Meta:
        model = ChanceryProfile
        fields = ('name','email', 'gender' )
        
        
class ChanceryProfileForm(BetterModelForm, TemplateForm):
    '''
    ChanceryProfile admin
    '''
    
    DAYS =  (('Monday',_('Monday')),
             ('Tuesday', _('Tuesday')),
             ('Wednesday', _('Wednesday')),
             ('Thursday', _('Thursday')),
             ('Friday', _('Friday')),
             ('Saturday', _('Saturday')),
             ('Sunday', _('Sunday')),
            )
    #address = AddressField(label=_('Chancery Address'))
    #name = NameField(label=_('Name'))

    def __init__(self, *args, **kwargs):
        super(ChanceryProfileForm, self).__init__(*args, **kwargs)
        self.fields['workingdays'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=self.DAYS,)

    class Meta:
        model = ChanceryProfile
        #fields = ('name', 'gender', 'telephone', 'workingdays',) # 'picture' is temporary excluded
        fields = ('first_name', 'middle_name', 'last_name', 'gender', 'telephone', 'workingdays',)
        #exclude = ('user', 'street', 'house_num', 'postcode', 'town', 'website', 'description', 'picture')
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

class ChanceryContactInformationForm(BetterModelForm, TemplateForm):
    '''
    Chancery contact information form.
    '''
    #address = AddressField(label=_('Chancery Contact Information'))

    class Meta:
        model = ChanceryProfile
        fields = ('website', 'house_num', 'street', 'postcode', 'town',) #'street', 'house_num', 'postcode', 'town',
    '''
    def clean_address(self):
        """
            Puts the subfields of the address multivaluefield into separate fields
        """
        for key in ['street', 'number', 'postalcode', 'city']:
            self.cleaned_data[key] = self.cleaned_data['address'][key]
        return self.cleaned_data['address']
    '''

class LastChanceryProfileForm(BetterModelForm, TemplateForm):
    '''
    ChanceryProfile admin
    '''
    councils_address = forms.BooleanField(label=_('Use Councils Address'), help_text=_('Select if you want to use the same address as the councils address'))

    class Meta:
        model = ChanceryProfile
        fields = ('house_num', 'street', 'postcode', 'town', 'website', 'description')

class InitialContactProfileForm(BetterModelForm, TemplateForm):
    name = NameField(label=_('Name'))
    email = forms.EmailField(_('Email'))
    
    def __init__(self, *args, **kwargs):
        super(InitialContactProfileForm, self).__init__(*args, **kwargs)
        self.fields['gender'].widget = forms.widgets.RadioSelect(choices=self.fields['gender'].choices)
    
    class Meta:
        model = ChanceryProfile
        fields = ('name','email', 'gender' )

class ContactProfileForm(BetterModelForm, TemplateForm):
    '''
    Contact Profile admin
    '''

    class Meta:
        model = ContactProfile
        exclude = ('user')


class LinkForm(BetterModelForm, TemplateForm):
    '''
    Link admin
    '''

    class Meta:
        model = Link
        exclude = ('politician')

class InterestForm(BetterModelForm, TemplateForm):
    '''
    Interest admin
    '''

    class Meta:
        model = Interest
        exclude = ('politician')

class AppearenceForm(BetterModelForm, TemplateForm):
    '''
    Appearence admin
    '''

    class Meta:
        model = Appearence
        exclude = ('politician')

class WorkExperienceForm(BetterModelForm, TemplateForm):
    '''
    WorkExperience admin
    '''

    class Meta:
        model = WorkExperience
        exclude = ('politician')

class EducationForm(BetterModelForm, TemplateForm):
    '''
    Education admin
    '''

    class Meta:
        model = Education
        exclude = ('politician')

class PoliticalExperienceForm(BetterModelForm, TemplateForm):
    '''
    PoliticalExperience admin
    '''

    class Meta:
        model = PoliticalExperience
        exclude = ('politician')

class CsvUploadForm(BetterModelForm, TemplateForm):
    '''
    CsvUpload admin
    '''

    file = forms.FileField(required = True)

class CsvConfirmForm(BetterModelForm, TemplateForm):
    '''
    CsvConfirm admin
    '''

    confirm = forms.BooleanField(required = True, help_text='I confirm that this information is correct [etcetcetc]')

