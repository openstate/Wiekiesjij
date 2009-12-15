from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from form_utils.forms import BetterModelForm, BetterForm
from utils.forms import TemplateForm
from utils.widgets import AutoCompleter, ColorPicker
from utils.fields import NameField, AddressField
from political_profiles.models import GENDERS
from political_profiles.models import EducationLevel, WorkExperienceSector, PoliticalExperienceType
from political_profiles.models import Appearance, PoliticalExperience, Education, WorkExperience, Link, Interest, PoliticianProfile, ChanceryProfile, ContactProfile, VisitorProfile

GENDERS = (
        ('Male',_('Male')),
        ('Female', _('Female')),
        )


class PoliticianProfileForm(BetterForm, TemplateForm):
    '''
    PoliticianProfile admin
    '''
    name            = NameField(label=_('Name'))
    initials        = forms.CharField(label=_('Initials'))
    email           = forms.EmailField(label=_('E-Mail'))
    dateofbirth     = forms.DateField(label=_('Date Of Birth'))
    introduction    = forms.CharField(label=_('introduction'), widget=forms.Textarea() )
    motivation      = forms.CharField(label=_('motivation'), widget=forms.Textarea())
    gender          = forms.CharField(label=_('gender'), widget=forms.widgets.RadioSelect(choices=GENDERS))
    picture         = forms.ImageField(label=_('Picture'), required=False)
    movie           = forms.URLField(label=_('Movie'), help_text=_('Link to YouTube video'))

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

class InitialChanceryProfileForm(BetterForm, TemplateForm):
    '''
    ChanceryProfile admin
    '''
    
    name = NameField(label=_('Name'))
    email = forms.EmailField(_('Email'))
    gender = forms.CharField(_('Gender'), widget=forms.widgets.RadioSelect(choices=GENDERS))
        
    class Meta:
        fieldsets = (
                        ('main', {
                            'fields': ('name','email','gender'), 
							'legend': 'Invite',
                            'classes': ('sub-form','invite',)
                        }
                    ),
                )
        
        
        
class ChanceryProfileForm(BetterForm, TemplateForm):
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
    name = NameField(label=_('Name'))
    gender = forms.CharField(_('Gender'), widget=forms.widgets.RadioSelect(choices=GENDERS))
    telephone = forms.CharField(_('Telepgone'))
    workingdays = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=DAYS, required=False)

    class Meta:
        fields = ('name', 'gender', 'telephone', 'workingdays',)

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
        fieldsets = (
                        ('main', {
                            'fields': ('name','email','gender'), 
							'legend': 'Invite the administrative contact for this party:',
							'description': 'This contact will be invited to complete further setup for this party.',
                            'classes': ('sub-form','invite')
                        }
                    ),
                )

class ContactProfileForm(BetterModelForm, TemplateForm):
    '''
    Contact Profile admin
    '''

    class Meta:
        model = ContactProfile
        exclude = ('user')


class ContactProfileContactInformationForm(BetterModelForm, TemplateForm):
    '''
    ContactProfile admin for editing contact information. Chapter 3.1.5 of interaction design.
    '''
    DAYS =  (('Monday',_('Monday')),
             ('Tuesday', _('Tuesday')),
             ('Wednesday', _('Wednesday')),
             ('Thursday', _('Thursday')),
             ('Friday', _('Friday')),
             ('Saturday', _('Saturday')),
             ('Sunday', _('Sunday')),
            )

    name = NameField(label=_('Name'))
    
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['workingdays'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=self.DAYS,)

    class Meta:
        model = ContactProfile
        fields = ('name', 'gender', 'telephone', 'workingdays', 'picture')


class LinkFormNew(BetterForm, TemplateForm):
    '''
    Link admin
    '''
    name        = forms.CharField(label=_('Name'))
    url         = forms.URLField(label=_('URL'))
    description	= forms.CharField(label=_('Description'), widget=forms.Textarea())


class InterestFormNew(BetterForm, TemplateForm):
    '''
    Interest admin
    '''
    organization    = forms.CharField(label=_('Organisation Name'))
    url             = forms.URLField(label=_('URL'))
    description     = forms.CharField(label=_('Description'), widget=forms.Textarea())

class AppearanceFormNew(BetterForm, TemplateForm):
    '''
    Appearance admin
    '''
    name        = forms.CharField(label=_('Affiliated Organisation Name'))
    location	= forms.CharField(label=_('Location'))
    url         = forms.URLField(label=_('URL'))
    description = forms.CharField(label=_('Description'), widget=forms.Textarea())
    datetime    = forms.DateTimeField(label=_('Date and Time of Appearance'))


class WorkExperienceFormNew(BetterForm, TemplateForm):
    '''
    WorkExperience admin
    '''
    company_name    = forms.CharField(label=_('Company Name'))
    sector          = forms.ModelChoiceField(queryset=WorkExperienceSector.objects, label=_('sector'))
    position        = forms.CharField(label=_('Position'))
    startdate       = forms.DateField(label=_('Start Date'))
    enddate         = forms.DateField(label=_('End Date'))
    current         = forms.BooleanField(label=_('Currently Employed'))
    description     = forms.CharField(label=_('Description'), widget=forms.Textarea() )

class EducationFormNew(BetterForm, TemplateForm):
    '''
    Education admin
    '''
    institute   = forms.CharField(label=_('Institute Name'))
    level       = forms.ModelChoiceField(queryset=EducationLevel.objects, label=_('level'))
    field       = forms.CharField(label=_('Field'))
    startdate   = forms.DateField(label=_('Start Date'))
    enddate     = forms.DateField(label=_('End Date'))
    description = forms.CharField(label=_('Description'), widget=forms.Textarea())

class PoliticalExperienceFormNew(BetterForm, TemplateForm):
    '''
    PoliticalExperience admin
    '''
    organisation    = forms.CharField(label=_('Organisation'))
    type            = forms.ModelChoiceField(queryset=PoliticalExperienceType.objects, label=_('type'))
    position        = forms.CharField(label=_('Position'))
    startdate       = forms.DateField(label=_('Start Date'))
    enddate         = forms.DateField(label=_('End Date'))
    description     = forms.CharField(label=_('Description'), widget=forms.Textarea())

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

class AppearanceForm(BetterModelForm, TemplateForm):
    '''
    Appearance admin
    '''
    class Meta:
        model = Appearance
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

class CsvUploadForm(BetterForm, TemplateForm):
    '''
    CsvUpload admin
    '''

    file = forms.FileField(required = True)

    def clean_file(self):
        if not self.cleaned_data['file'].content_type == 'text/csv':
            raise forms.ValidationError('The file you tried to submit is not a CSV file')
    
class CsvConfirmForm(BetterForm, TemplateForm):
    '''
    CsvConfirm admin
    '''

    confirm = forms.BooleanField(required = True, help_text='I confirm that this information is correct. Any trouble or problems that occur because I submitted wrong data are for my account and not for WKJ, HNS or GL.')
