from form_utils.forms import BetterModelForm
from utils.forms import TemplateForm
from utils.widgets import AutoCompleter
from utils.fields import NameField
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from political_profiles.models import PoliticalExperience, Education, WorkExperience, Link, Interest, Appearence, PoliticianProfile, ChanceryProfile, ContactProfile, VisitorProfile

class PoliticianProfileForm(BetterModelForm, TemplateForm):
    '''
    PoliticianProfile admin
    '''

    def __init__(self, *args, **kwargs):
        super(PoliticianProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget = AutoCompleter(model = PoliticianProfile, field = 'first_name')

    class Meta:
        model = PoliticianProfile


class InitialPoliticianProfileForm(BetterModelForm, TemplateForm):
    '''
    ChanceryProfile admin
    '''
    class Meta:
        model = PoliticianProfile
        fields = ('first_name','middle_name','last_name','email','gender' )
        exclude = ('user')

class InitialChanceryProfileForm(BetterModelForm, TemplateForm):
    '''
    ChanceryProfile admin
    '''
    
    name = NameField(_('Name'))
    email = forms.EmailField(_('Email'))
    
    def __init__(self, *args, **kwargs):
        super(InitialChanceryProfileForm, self).__init__(*args, **kwargs)
        self.fields['gender'].widget = forms.widgets.RadioSelect(choices=self.fields['gender'].choices[1:])
    
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

    def __init__(self, *args, **kwargs):
        super(ChanceryProfileForm, self).__init__(*args, **kwargs)
        self.fields['workingdays'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=self.DAYS,)

    class Meta:
        model = ChanceryProfile
        exclude = ('user', 'street', 'house_num', 'postcode', 'town', 'website', 'description')



class LastChanceryProfileForm(BetterModelForm, TemplateForm):
    '''
    ChanceryProfile admin
    '''
    councils_address = forms.BooleanField(label=_('Use Councils Address'), help_text=_('Select if you want to use the same address as the councils address'))

    class Meta:
        model = ChanceryProfile
        fields = ('house_num', 'street', 'postcode', 'town', 'website', 'description')

class InitialContactProfileForm(BetterModelForm, TemplateForm):
    '''
    ChanceryProfile admin
    '''
    class Meta:
        model = ContactProfile
        fields = ('first_name','middle_name','last_name','email','gender' )
        exclude = ('user')

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