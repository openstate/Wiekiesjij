import datetime
import mimetypes
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as __
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget

from form_utils.forms import BetterModelForm, BetterForm
from utils.formutils import TemplateForm

from utils.widgets import DateTimePicker, HiddenDateTimePicker, DateSelectPicker

from utils.fields import NameField, AddressField

from political_profiles.models import MOTIVATION, CHURCH, DIET, LIFE_STANCE, MARITAL_STATUS, GENDERS, NEWSPAPER, TRANSPORT, CHARITY, MEDIA, SPORT, HOBBIES , CLUBS, PETS
from political_profiles.models import EducationLevel, WorkExperienceSector, PoliticalExperienceType
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
    initials        = forms.CharField(label=_('Initials'))
    dateofbirth     = forms.DateField(label=_('Date Of Birth'), widget=DateSelectPicker(years=range(1910, datetime.date.today().year)) )
    introduction    = forms.CharField(label=_('Introduction'), widget=forms.Textarea(), required=False)
    motivation      = forms.ChoiceField(label=_('Motivation'), choices=MOTIVATION, required=False)
    gender          = forms.CharField(label=_('Gender'), widget=forms.widgets.RadioSelect(choices=GENDERS))
    #picture         = forms.ImageField(label=_('Picture'), required=False)
    movie           = forms.URLField(label=_('Movie'), help_text=_('Link to YouTube video'))

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)



class PoliticianProfileLifeForm(BetterForm, TemplateForm):
    '''
    PoliticianProfile admin
    '''

    marital_status  = forms.ChoiceField(label=_('Marital Status'),choices=MARITAL_STATUS)
    num_children    = forms.IntegerField(_('Number of Children'))
    life_stance     = forms.ChoiceField(label=_('Life Stance'),choices=LIFE_STANCE)
    church          = forms.ChoiceField(label=_('Church'),choices=CHURCH)
    smoker          = forms.BooleanField(label=_('Do you Smoke?'), widget=forms.widgets.RadioSelect(choices=[(1, 'Yes'), (2, 'No')]) )
    diet            = forms.ChoiceField(label=_('Diet'),choices=DIET)

class PoliticianProfileExtraForm(BetterForm, TemplateForm):
    '''
    PoliticianProfile admin
    '''
    fav_news        = forms.ChoiceField(label=_('Favourite Newspaper'),choices=NEWSPAPER)
    transport       = forms.ChoiceField(label=_('What is your regular method of transport'),choices=TRANSPORT  )
    charity         = forms.ChoiceField(label=_('What charity do you care for most?'),choices=CHARITY )
    fav_media       = forms.ChoiceField(label=_('What is your favourite media chanel?'),choices=MEDIA )
    fav_sport       = forms.ChoiceField(label=_('What is your favourite sport?'),choices=SPORT )
    hobby           = forms.ChoiceField(label=_('What is your hobby'),choices=HOBBIES )
    fav_club        = forms.ChoiceField(label=_('What is your favourite club'),choices=CLUBS  )
    fav_pet         = forms.ChoiceField(label=_('What is your favourite pet'),choices=PETS )
      
#
#
class InitialPoliticianProfileForm(BetterForm, TemplateForm):
    '''
    ChanceryProfile admin
    '''
    name = NameField(label=_('Name'))
    email = forms.EmailField(label=_('E-mail'), help_text=__('De uitnodiging wordt verzonden naar dit adres.'), max_length=30)
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
    name = NameField(label=_('Name'), help_text=__('Vul hier uw contactinformatie in.'))
    gender = forms.CharField(label=_('Gender'), widget=forms.widgets.RadioSelect(choices=GENDERS))
    telephone = forms.CharField(label=_('Telephone'), help_text=__('Vul hier uw telefoonnummer in (formaat: 010-1234567).'))
    workingdays = forms.MultipleChoiceField(label=_('Working days'), widget=forms.CheckboxSelectMultiple(), choices=DAYS, help_text=__('Vul hier de dagen in wanneer wij u telefonische kunnen bereiken.'), required=False)

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
    name            = NameField(label=_('Name'), help_text=__('Vul hier uw contactinformatie in.'))
    telephone       = forms.CharField(label=_('Phone Number'), help_text=__('Vul hier uw telefoonnummer in (formaat: 010-1234567).'))
    gender          = forms.CharField(label=_('Gender'), widget=forms.widgets.RadioSelect(choices=GENDERS))
    workingdays     = forms.MultipleChoiceField(label=_('Working days'), widget=forms.CheckboxSelectMultiple, choices=DAYS, help_text=__('Vul hier de dagen in wanneer wij u telefonische kunnen bereiken.'))


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
    url         = forms.URLField(label=_('URL'), required=True)
    datetime    = forms.DateTimeField(label=_('Date and Time of Appearance'), widget=DateTimePicker(), required=True)
    description = forms.CharField(label=_('Description'), widget=forms.Textarea())

class WorkExperienceFormNew(BetterForm, TemplateForm):
    '''
    WorkExperience admin
    '''
    company_name    = forms.CharField(label=_('Company Name'))
    sector          = forms.ModelChoiceField(queryset=WorkExperienceSector.objects, label=_('Sector'))
    position        = forms.CharField(label=_('Position'))
    startdate       = forms.DateField(label=_('Start Date'), widget=DateSelectPicker(years=range(1925, datetime.date.today().year), fixed_day=1), required=True )
    enddate         = forms.DateField(label=_('End Date'), widget=DateSelectPicker(years=range(1925, datetime.date.today().year), fixed_day=28), required=True )
    current         = forms.BooleanField(label=_('Currently Employed'))
    description     = forms.CharField(label=_('Description'), widget=forms.Textarea() )

class EducationFormNew(BetterForm, TemplateForm):
    '''
    Education admin
    '''
    institute   = forms.CharField(label=_('Institute Name'))
    level       = forms.ModelChoiceField(queryset=EducationLevel.objects, label=_('Level'))
    field       = forms.CharField(label=_('Field'))
    startdate   = forms.DateField(label=_('Start Date'), widget=DateSelectPicker(years=range(1925, datetime.date.today().year), fixed_day=1), required=True )
    enddate     = forms.DateField(label=_('End Date'), widget=DateSelectPicker(years=range(1925, datetime.date.today().year), fixed_day=28), required=True )
    description = forms.CharField(label=_('Description'), widget=forms.Textarea())

class PoliticalExperienceFormNew(BetterForm, TemplateForm):
    '''
    PoliticalExperience admin
    '''
    organisation    = forms.CharField(label=_('Organisation'))
    type            = forms.ModelChoiceField(queryset=PoliticalExperienceType.objects, label=_('Type'))
    position        = forms.CharField(label=_('Position'))
    startdate       = forms.DateField(label=_('Start Date'), widget=DateSelectPicker(years=range(1935, datetime.date.today().year), fixed_day=1), required=True)
    enddate         = forms.DateField(label=_('End Date'), widget=DateSelectPicker(years=range(1935, datetime.date.today().year),  fixed_day=28), required=True)
    description     = forms.CharField(label=_('Description'), widget=forms.Textarea())

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
        self.fields['url'].required=True

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
        self.fields['startdate'].widget = DateSelectPicker(years=range(1925, datetime.date.today().year), required=True, fixed_day=1)
        self.fields['enddate'].widget = DateSelectPicker(years=range(1925, datetime.date.today().year), required=True, fixed_day=28)
        self.fields['startdate'].required=True
        self.fields['enddate'].required=True
        self.fields['sector'].required=True

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
        self.fields['startdate'].widget = DateSelectPicker(years=range(1925, datetime.date.today().year), required=True, fixed_day=1)
        self.fields['enddate'].widget = DateSelectPicker(years=range(1925, datetime.date.today().year), required=True, fixed_day=28)
        self.fields['startdate'].required=True
        self.fields['enddate'].required=True
        self.fields['level'].required=True

    class Meta:
        model = Education
        exclude = ('politician')

class PoliticalExperienceForm(BetterModelForm, TemplateForm):
    '''
    PoliticalExperience admin
    '''
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea()
        self.fields['startdate'].widget=DateSelectPicker(years=range(1935, datetime.date.today().year), required=True, fixed_day=1)
        self.fields['enddate'].widget=DateSelectPicker(years=range(1935, datetime.date.today().year), required=True, fixed_day=28)
        self.fields['startdate'].required=True
        self.fields['enddate'].required=True
        self.fields['type'].required=True

        
    class Meta:
        model = PoliticalExperience
        exclude = ('politician')

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
