# -*- coding: utf-8 -*-

import datetime
import copy

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.util import ErrorList
from django.contrib.auth.models import User

from form_utils.forms import BetterModelForm, BetterForm

from utils.formutils import TemplateForm
from utils.widgets import DateTimePicker, HiddenDateTimePicker, DateSelectPicker, ImageWidget
from utils.fields import NameField, AddressField, YoutubeURLField, ClearableImageField

from political_profiles.models import RELIGION, DIET, MARITAL_STATUS, GENDERS, NEWSPAPER, TRANSPORT, MEDIA, PETS, CHARITIES, SMOKER, PROVINCES
from political_profiles.models import EducationLevel, WorkExperienceSector, PoliticalExperienceType, PoliticalGoal
from political_profiles.models import Connection, Appearance, PoliticalExperience, Education, WorkExperience, Link, Interest, ChanceryProfile, ContactProfile

DAYS =  (('Monday',_('Monday')),
             ('Tuesday', _('Tuesday')),
             ('Wednesday', _('Wednesday')),
             ('Thursday', _('Thursday')),
             ('Friday', _('Friday')),
             ('Saturday', _('Saturday')),
             ('Sunday', _('Sunday')),
            )



class PoliticianProfileForm(BetterForm, TemplateForm):
    '''
    PoliticianProfile admin
    '''
    name            = NameField(label=_('Name'))
    initials        = forms.CharField(label=_('Initials'), max_length=15)
    dateofbirth     = forms.DateField(label=_('Date Of Birth'), widget=DateSelectPicker(years=range(1910, datetime.date.today().year)) )
    gender          = forms.CharField(label=_('Gender'), widget=forms.widgets.RadioSelect(choices=GENDERS))
    

class PoliticianProfileLifeForm(BetterForm, TemplateForm):
    '''
    PoliticianProfile admin
    '''
    EMPTY_OPT = ('', '------')
    OPT_MARITAL = copy.deepcopy(MARITAL_STATUS)
    OPT_MARITAL.insert(0, EMPTY_OPT)
    OPT_RELIGION = copy.deepcopy(RELIGION)
    OPT_RELIGION.insert(0, EMPTY_OPT)
    OPT_SMOKER = copy.deepcopy(SMOKER)
    OPT_SMOKER.insert(0, EMPTY_OPT)
    OPT_DIET = copy.deepcopy(DIET)
    OPT_DIET.insert(0, EMPTY_OPT)
    OPT_PROVINCES = copy.deepcopy(PROVINCES)
    OPT_PROVINCES.insert(0, EMPTY_OPT)
     
    
    marital_status  = forms.ChoiceField(label=_('Marital Status'),choices=OPT_MARITAL, required=False)
    num_children    = forms.IntegerField(label=_('Number of Children'), required=False)
    religion        = forms.ChoiceField(label=_('Religion'),choices=OPT_RELIGION, required=False)
    #religous_group  = forms.CharField(label=_('Geloofsgemeenschap'), max_length=255, required=False)
    smoker          = forms.ChoiceField(label=_('Do you smoke?'), choices=OPT_SMOKER, required=False)
    diet            = forms.ChoiceField(label=_(u'Wat is uw Dieet?'), choices=OPT_DIET, required=False)
    province        = forms.ChoiceField(label=_(u'In welke provincie woont u?'), choices=OPT_PROVINCES, required=False)

class PoliticianProfileExtraForm(BetterForm, TemplateForm):
    '''
    PoliticianProfile admin
    '''
    EMPTY_OPT = ('', '------')
    OPT_NEWSPAPERS = copy.deepcopy(NEWSPAPER)
    OPT_NEWSPAPERS.insert(0, EMPTY_OPT)
    OPT_TRANSPORT = copy.deepcopy(TRANSPORT)
    OPT_TRANSPORT.insert(0, EMPTY_OPT)
    OPT_CHARITIES = copy.deepcopy(CHARITIES)
    OPT_CHARITIES.insert(0, EMPTY_OPT)
    OPT_MEDIA = copy.deepcopy(MEDIA)
    OPT_MEDIA.insert(0, EMPTY_OPT)
    OPT_PETS = copy.deepcopy(PETS)
    OPT_PETS.insert(0, EMPTY_OPT)
    
    fav_news        = forms.ChoiceField(label=_('... Newspaper?'),choices=OPT_NEWSPAPERS, required=False)
    transport       = forms.ChoiceField(label=_('... Method of transport?'), help_text=_('What is your regular method of transport?'), required=False, choices=OPT_TRANSPORT)
    charity         = forms.ChoiceField(label=_('... Charity?'),help_text=_('What charity do you care for most?'), required=False, choices=OPT_CHARITIES )
    fav_media       = forms.ChoiceField(label=_('... TV channel?'),choices=OPT_MEDIA, required=False)
    fav_pet         = forms.ChoiceField(label=_('... Pet?'),choices=OPT_PETS, required=False)
    hobby           = forms.CharField(label=_('... Hobby?'),max_length=255, required=False )
    fav_sport       = forms.CharField(label=_('... Sport?'), max_length=255, required=False )
    fav_club        = forms.CharField(label=_('... Voetbal Club?'), max_length=255, required=False)
    

class PoliticianProfilePoliticalForm(BetterForm, TemplateForm):
    """
        Political related forms
    """
    introduction    = forms.CharField(label=_('Introduction'), widget=forms.Textarea(), required=False, help_text=_('Hier kunt u een korte toelichting geven over uzelf, waarom u zich kandidaat stelt en wat uw plannen zijn.'))
    picture         = ClearableImageField(label=_('Picture'), required=False, widget=ImageWidget(), help_text=_('Deze foto zal getoond worden op uw profiel en in het kandidatenoverzicht bij uw partij. Wij willen u verzoeken om een staande foto (verticaal) te gebruiken.\n De foto mag niet groter zijn dan 500KB. Met een iPad is het niet mogelijk een foto toe te voegen. Indien u op een iPad werkt graag deze stap overslaan en waar mogelijk via een PC een foto toevoegen.'))
    movie           = YoutubeURLField(label=_('Movie'), required=False, help_text=_(u'Link naar een persoonlijke YouTube video. Deze vindt u rechts in het grijze vlak onder URL op de website van YouTube.'))
      
#
#
class InitialPoliticianProfileForm(BetterForm, TemplateForm):
    '''
    ChanceryProfile admin
    '''
    name = NameField(label=_('Name'))
    email = forms.EmailField(label=_('E-mail'), help_text=_('De uitnodiging wordt verzonden naar dit adres.'))
    gender = forms.CharField(label=_('Gender'), widget=forms.widgets.RadioSelect(choices=GENDERS))
        
    
    def clean_email(self):
        """
           We have to check of the user exists and if it's the propper type of user
        """
        email = self.cleaned_data['email']
        try:
           user = User.objects.get(email=email)
           if not user.profile or user.profile.type != 'candidate':
               del self.cleaned_data['email']
               raise forms.ValidationError(_('A user with the email address %(email)s exists but has access as a differend type of user, you need to use a differend email adres to invite this person') % {'email': email})
        except User.DoesNotExist:
           pass
        except User.MultipleObjectsReturned:
            raise Exception('Multiple users with the same e-mail address exist, fix this in the database asap !')
        return self.cleaned_data['email']

class EditPoliticianProfileForm(BetterForm, TemplateForm):
    """
        Politician profile form for editing
    """
    name = NameField(label=_('Name'))
    email = forms.EmailField(label=_('E-mail'), help_text=_('De uitnodiging wordt verzonden naar dit adres.'))
    gender = forms.CharField(label=_('Gender'), widget=forms.widgets.RadioSelect(choices=GENDERS))
        
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EditPoliticianProfileForm, self).__init__(*args, **kwargs)
        
    def clean_email(self):
        """
           We have to check of the user exists and if it's the propper type of user
        """
        email = self.cleaned_data['email']
        try:
           user = User.objects.get(email=email)
           if user.pk != self.user.pk:
               del self.cleaned_data['email']
               raise forms.ValidationError(_('Another user with the email address %(email)s exists') % {'email': email})
           if not user.profile or user.profile.type != 'candidate':
               del self.cleaned_data['email']
               raise forms.ValidationError(_('A user with the email address %(email)s exists but has access as a differend type of user, you need to use a differend email adres to invite this person') % {'email': email})
        except User.DoesNotExist:
           pass
        except User.MultipleObjectsReturned:
            raise Exception('Multiple users with the same e-mail address exist, fix this in the database asap !')
        return self.cleaned_data['email']
    
class InitialChanceryProfileForm(BetterForm, TemplateForm):
    '''
    ChanceryProfile admin
    '''
    
    name = NameField(label=_('Name'))
    email = forms.EmailField(label=_('E-mail'), help_text=_('The invitation will be sent to this address.'))
    gender = forms.CharField(label=_('Gender'), widget=forms.widgets.RadioSelect(choices=GENDERS))

        
    class Meta:
        fieldsets = (
                        ('main', {
                            'fields': ('name','email','gender'), 
							'legend': _('Invite the administrative contact for this council:'),
							'description': _('This contact will be invited to complete further setup for this council.'),
                            'classes': ('sub-form','invite',)
                        }
                    ),
                )

    def clean_email(self):
        """
            We have to check of the user exists and if it's the propper type of user
        """
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            if not user.profile or user.profile.type != 'council_admin':
                del self.cleaned_data['email']
                raise forms.ValidationError(_('A user with the email address %(email)s exists but has access as a differend type of user, you need to use a differend email adres to invite this person') % {'email': email})
        except User.DoesNotExist:
            pass
        except User.MultipleObjectsReturned:
            raise Exception('Multiple users with the same e-mail address exist, fix this in the database asap !')
        return self.cleaned_data['email']
        
        
class ChanceryProfileForm(BetterForm, TemplateForm):
    '''
    ChanceryProfile admin
    '''
    

    #address = AddressField(label=_('Chancery Address'))
    name = NameField(label=_('Name'), help_text=_('Vul hier uw contactinformatie in.'))
    gender = forms.CharField(label=_('Gender'), widget=forms.widgets.RadioSelect(choices=GENDERS))
    telephone = forms.CharField(label=_('Telephone'), help_text=_('Vul hier uw telefoonnummer in (formaat: 010-1234567).'))
    workingdays = forms.MultipleChoiceField(label=_('Working days'), widget=forms.CheckboxSelectMultiple(), choices=DAYS, help_text=_('Vul hier de dagen in wanneer wij u telefonische kunnen bereiken.'), required=False)

class ChanceryContactInformationForm(BetterForm, TemplateForm):
    '''
    Chancery contact information form.
    '''
    website = forms.URLField(label=_('Chancery website'))
    address = AddressField(label=_('Chancery Contact Information'))
    

class LastChanceryProfileForm(BetterModelForm, TemplateForm):
    '''
    ChanceryProfile admin
    '''
    councils_address = forms.BooleanField(label=_('Use Councils Address'), help_text=_('Select if you want to use the same address as the councils address'))

    class Meta:
        model = ChanceryProfile
        fields = ('house_num', 'street', 'postcode', 'town', 'website', 'description')

class InitialContactProfileForm(BetterForm, TemplateForm):
    name = NameField(label=_('Name'))
    email = forms.EmailField(label=_('E-mail'), help_text=_('The invitation will be sent to this address.'))
    gender = forms.CharField(label=_('Gender'), widget=forms.widgets.RadioSelect(choices=GENDERS))
	
    class Meta:
        fieldsets = (
                        ('main', {
                            'fields': ('name','email','gender'), 
                            'legend': _('Invite the administrative contact for this party:'),
                            'description': _('This contact will be invited to complete further setup for this party.'),
                            'classes': ('sub-form','invite')
                        }
                    ),
                )
                
    def clean_email(self):
        """
           We have to check of the user exists and if it's the propper type of user
        """
        email = self.cleaned_data['email']
        try:
           user = User.objects.get(email=email)
           if not user.profile or user.profile.type != 'party_admin':
               del self.cleaned_data['email']
               raise forms.ValidationError(_('A user with the email address %(email)s exists but has access as a differend type of user, you need to use a differend email adres to invite this person') % {'email': email})
        except User.DoesNotExist:
           pass
        except User.MultipleObjectsReturned:
            raise Exception('Multiple users with the same e-mail address exist, fix this in the database asap !')
        return self.cleaned_data['email']

class ContactProfileForm(BetterForm, TemplateForm):
    '''
    Contact Profile admin
    '''
    name            = NameField(label=_('Name'), help_text=_('Vul hier uw contactinformatie in.'))
    telephone       = forms.CharField(label=_('Phone Number'), help_text=_('Vul hier uw telefoonnummer in (formaat: 010-1234567).'))
    gender          = forms.CharField(label=_('Gender'), widget=forms.widgets.RadioSelect(choices=GENDERS))
    workingdays     = forms.MultipleChoiceField(label=_('Working days'), widget=forms.CheckboxSelectMultiple, choices=DAYS, help_text=_('Vul hier de dagen in wanneer wij u telefonische kunnen bereiken.'))


class ContactProfileContactInformationForm(BetterModelForm, TemplateForm):
    '''
    ContactProfile admin for editing contact information. Chapter 3.1.5 of interaction design.
    '''


    name = NameField(label=_('Name'))
    
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['workingdays'] = forms.MultipleChoiceField(label=_('Working days'), widget=forms.CheckboxSelectMultiple, choices=self.DAYS,)

    class Meta:
        model = ContactProfile
        fields = ('name', 'gender', 'telephone', 'workingdays', 'picture')


class LinkFormNew(BetterForm, TemplateForm):
    '''
    Link admin
    '''
    name        = forms.CharField(label=_('Name'))
    url         = forms.URLField(label=_('URL'))
    description = forms.CharField(label=_('Description'), widget=forms.Textarea())


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
    location    = forms.CharField(label=_('Location'))
    url         = forms.URLField(label=_('URL'), required=False)
    datetime    = forms.DateTimeField(label=_('Date and Time of Appearance'), widget=DateTimePicker(), required=True)
    description = forms.CharField(label=_('Description'), widget=forms.Textarea())

class WorkExperienceFormNew(BetterForm, TemplateForm):
    '''
    WorkExperience admin
    '''
    company_name    = forms.CharField(label=_('Company Name'))
    sector          = forms.ModelChoiceField(queryset=WorkExperienceSector.objects, label=_('Sector'))
    position        = forms.CharField(label=_('Position'))
    startdate       = forms.DateField(label=_('Start Date'), widget=DateSelectPicker(years=range(datetime.date.today().year, 1935, -1), fixed_day=1), required=True )
    enddate         = forms.DateField(label=_('End Date'), widget=DateSelectPicker(years=range(datetime.date.today().year, 1935, -1), fixed_day=28), required=False, help_text=_('Leaving this empty will indicate it is ongoing') )
    description     = forms.CharField(label=_('Description'), widget=forms.Textarea() )
    
    def clean(self):
        startdate = self.cleaned_data.get('startdate')
        enddate = self.cleaned_data.get('enddate')

        if startdate and enddate is not None:
            if startdate > enddate:
                self._errors['enddate'] = ErrorList([_('End date should be after the start date')])
                del self.cleaned_data['startdate']
                del self.cleaned_data['enddate']
        return self.cleaned_data

class EducationFormNew(BetterForm, TemplateForm):
    '''
    Education admin
    '''
    institute   = forms.CharField(label=_('Institute Name'))
    level       = forms.ModelChoiceField(queryset=EducationLevel.objects, label=_('Level'))
    field       = forms.CharField(label=_('Field'))
    startdate   = forms.DateField(label=_('Start Date'), widget=DateSelectPicker(years=range(datetime.date.today().year, 1935, -1), fixed_day=1), required=True )
    enddate     = forms.DateField(label=_('End Date'), widget=DateSelectPicker(years=range(datetime.date.today().year, 1935, -1), fixed_day=28), required=False, help_text=_('Leaving this empty will indicate it is ongoing') )
    description = forms.CharField(label=_('Description'), widget=forms.Textarea())
    
    
    def clean(self):
        startdate = self.cleaned_data.get('startdate')
        enddate = self.cleaned_data.get('enddate')

        if startdate and enddate is not None:
            if startdate > enddate:
                self._errors['enddate'] = ErrorList([_('End date should be after the start date')])
                del self.cleaned_data['startdate']
                del self.cleaned_data['enddate']
        return self.cleaned_data

class PoliticalExperienceFormNew(BetterForm, TemplateForm):
    '''
    PoliticalExperience admin
    '''
    organisation    = forms.CharField(label=_('Organisation'))
    type            = forms.ModelChoiceField(queryset=PoliticalExperienceType.objects, label=_('Type'))
    position        = forms.CharField(label=_('Position'))
    startdate       = forms.DateField(label=_('Start Date'), widget=DateSelectPicker(years=range(datetime.date.today().year, 1935, -1), fixed_day=1), required=True)
    enddate         = forms.DateField(label=_('End Date'), widget=DateSelectPicker(years=range(datetime.date.today().year, 1935, -1),  fixed_day=28), required=False, help_text=_('Leaving this empty will indicate it is ongoing'))
    description     = forms.CharField(label=_('Description'), widget=forms.Textarea())
    
    
    def clean(self):
        startdate = self.cleaned_data.get('startdate')
        enddate = self.cleaned_data.get('enddate')

        if startdate and enddate is not None:
            if startdate > enddate:
                self._errors['enddate'] = ErrorList([_('End date should be after the start date')])
                del self.cleaned_data['startdate']
                del self.cleaned_data['enddate']
        return self.cleaned_data

class GoalForm(BetterModelForm, TemplateForm):
    """
        Goals
    """
    class Meta:
        model = PoliticalGoal
        exclude = ('politician')
    

class LinkForm(BetterModelForm, TemplateForm):
    '''
    Link admin
    '''
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea()

    class Meta:
        model = Link
        exclude = ('politician')

class ConnectionForm(BetterModelForm, TemplateForm):
    '''
    Connection admin
    '''
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea()

    class Meta:
        model = Connection
        exclude = ('politician')


class InterestForm(BetterModelForm, TemplateForm):
    '''
    Interest admin
    '''
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea()

    class Meta:
        model = Interest
        exclude = ('politician')

class AppearanceForm(BetterModelForm, TemplateForm):
    '''
    Appearance admin
    '''
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea()
        self.fields['datetime'].widget = DateTimePicker()
        self.fields['datetime'].hidden_widget = HiddenDateTimePicker()
        self.fields['datetime'].required=True
        self.fields['url'].required=False

    class Meta:
        model = Appearance
        exclude = ('politician')


class WorkExperienceForm(BetterModelForm, TemplateForm):
    '''
    WorkExperience admin
    '''
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea()
        self.fields['startdate'].widget = DateSelectPicker(years=range(datetime.date.today().year, 1935, -1), required=True, fixed_day=1)
        self.fields['enddate'].widget = DateSelectPicker(years=range(datetime.date.today().year, 1935, -1), required=False, fixed_day=28)
        self.fields['startdate'].required=True
        self.fields['enddate'].required=False
        self.fields['enddate'].help_text=_('Leaving this empty will indicate it is ongoing')
        self.fields['sector'].required=True
    
    def clean(self):
        startdate = self.cleaned_data.get('startdate')
        enddate = self.cleaned_data.get('enddate')
        
        if startdate and enddate is not None:
            if startdate > enddate:
                self._errors['enddate'] = ErrorList([_('End date should be after the start date')])
                del self.cleaned_data['startdate']
                del self.cleaned_data['enddate']
        return self.cleaned_data
    
    class Meta:
        model = WorkExperience
        exclude = ('politician')

class EducationForm(BetterModelForm, TemplateForm):
    '''
    Education admin
    '''
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea()
        self.fields['startdate'].widget = DateSelectPicker(years=range(datetime.date.today().year, 1935, -1), required=True, fixed_day=1)
        self.fields['enddate'].widget = DateSelectPicker(years=range(datetime.date.today().year, 1935, -1), required=False, fixed_day=28)
        self.fields['startdate'].required=True
        self.fields['enddate'].required=False
        self.fields['enddate'].help_text=_('Leaving this empty will indicate it is ongoing')
        self.fields['level'].required=True

    class Meta:
        model = Education
        exclude = ('politician')
        
    def clean(self):
        startdate = self.cleaned_data.get('startdate')
        enddate = self.cleaned_data.get('enddate')

        if startdate and enddate is not None:
            if startdate > enddate:
                self._errors['enddate'] = ErrorList([_('End date should be after the start date')])
                del self.cleaned_data['startdate']
                del self.cleaned_data['enddate']
        return self.cleaned_data

class PoliticalExperienceForm(BetterModelForm, TemplateForm):
    '''
    PoliticalExperience admin
    '''
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea()
        self.fields['startdate'].widget=DateSelectPicker(years=range(datetime.date.today().year, 1935, -1), required=True, fixed_day=1)
        self.fields['enddate'].widget=DateSelectPicker(years=range(datetime.date.today().year, 1935, -1), required=False, fixed_day=28)
        self.fields['startdate'].required=True
        self.fields['enddate'].required=False
        self.fields['enddate'].help_text=_('Leaving this empty will indicate it is ongoing')
        self.fields['type'].required=True

        
    class Meta:
        model = PoliticalExperience
        exclude = ('politician')
        
    def clean(self):
        startdate = self.cleaned_data.get('startdate')
        enddate = self.cleaned_data.get('enddate')

        if startdate and enddate is not None:
            if startdate > enddate:
                self._errors['enddate'] = ErrorList([_('End date should be after the start date')])
                del self.cleaned_data['startdate']
                del self.cleaned_data['enddate']
        return self.cleaned_data

class CsvUploadForm(BetterForm, TemplateForm):
    '''
    CsvUpload admin
    '''

    file = forms.FileField(required = True)

class CsvConfirmForm(BetterForm, TemplateForm):
    '''
    CsvConfirm admin
    '''

    confirm = forms.BooleanField(required = True, help_text=_('I confirm that this information is correct. Any trouble or problems that occur because I submitted wrong data are for my account and not for WKJ, HNS or GL.'))


class AgreeForm(BetterForm, TemplateForm):
    """
        last form for the politician to agree to some things
    """
    hns_dev = forms.BooleanField(
                            label=_('HNS.DEV'), help_text=_('Bij deze gaat u ermee akkoord dat uw gegevens worden opgeslagen in HNS.dev.'),
                            required=False)
    science = forms.BooleanField(
                            label=_('Science'), help_text=_('Bij deze gaat u ermee akkoord dat uw gegevens <strong>geanonimiseerd</strong> gebruikt kunnen worden voor wetenschappelijk onderzoek.'),
                            required=False)
        
