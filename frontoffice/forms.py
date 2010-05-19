#-*- coding: utf-8 -*-
from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _

from political_profiles.models import RELIGION, DIET, MARITAL_STATUS, GENDERS
from political_profiles.models import EducationLevel
import copy
from form_utils.forms import BetterForm
from utils.formutils import TemplateForm
from utils.fields import NameField, DutchMobilePhoneField
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from elections.models import ElectionInstance
from django.contrib.sites.models import Site
from django.utils.http import int_to_base36

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("E-mail"), max_length=75)

    def clean_email(self):
        """
        Validates that a user exists with the given e-mail address.
        """
        email = self.cleaned_data["email"]
        self.users_cache = User.objects.filter(email__iexact=email)
        if len(self.users_cache) == 0:
            raise forms.ValidationError(_("That e-mail address doesn't have an associated user account. Are you sure you've registered?"))
        return email

    def save(self, domain_override=None, email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator):
        """
        Generates a one-use only link for resetting password and sends to the user
        """
        from utils.emails import send_email
        for user in self.users_cache:
            if not domain_override:
                current_site = Site.objects.get_current()
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            #t = loader.get_template(email_template_name)


            send_email(
                    _("Password reset on %s") % site_name,
                    'info@wiekiesjij.nl',
                    user.email,
                    {
                        'email': user.email,
                        'domain': domain,
                        'site_name': site_name,
                        'uid': int_to_base36(user.id),
                        'user': user,
                        'token': token_generator.make_token(user),
                        'protocol': use_https and 'https' or 'http', },
                    {'plain': 'registration/email/forgot_password.txt','html': email_template_name},
                )

class RegionChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

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
    election_instances = ElectionInstance.objects.filter(election_event = settings.ELECTIONS_ELECTION_EVENT_ID).order_by('name')
    #region = RegionChoiceField(queryset=election_instances, label=_('Region'), required=False)
    gender = forms.CharField(label=_('Gender'), widget=forms.widgets.RadioSelect(choices=GENDERS), required=False)
    start_age = forms.IntegerField(label=_('Lowest Age'), required=False)
    end_age = forms.IntegerField(label=_('Oldest Age'), required=False)
    marital_status = forms.ChoiceField(label=_('Marital Status'), choices=MARITAL_STATUS_A, required=False)
    #children = forms.NullBooleanField(label=_('Children'), widget=forms.widgets.NullBooleanSelect(), required=False )
    children = forms.ChoiceField(label=_('Children'), choices=[('---------', _('---------')), (1, _('Yes')), (2, _('No')),], required=False )
    religion = forms.ChoiceField(choices=RELIGION_A, label=_('Religon'), required=False)
    education = forms.ModelChoiceField(queryset=EducationLevel.objects, label=_('Education Level'), required=False)
    political_exp_years = forms.IntegerField(label=_('Minimum years of political experience'), required=False)
    work_exp_years = forms.IntegerField(label=_('Mimimum years of work experience'), required=False)
    #smoker = forms.BooleanField(label=_('Smoker'), widget=forms.widgets.NullBooleanSelect(), required=False)
    smoker = forms.ChoiceField(label=_('Smoker'), choices=[('---------', _('---------')), (1, _('Yes')), (2, _('No')),], required=False )
    diet = forms.ChoiceField(choices=DIET, label=_(u'Vegitariër'), required=False)
    goals = forms.CharField(label=_('Goals'), required=False)


class VisitorProfileForm(BetterForm, TemplateForm):
    name        = NameField(label=_('Name'))
    phone       = MobilePhoneField(label=_('Mobile phone number'))
    send_text   = forms.BooleanField(label=_('Voting reminder on the day of the election'), help_text=_('I would like to receive a reminder (text message) for voting on the day of election.'), required=False)

class RegionSelectForm(BetterForm, TemplateForm):
    region  = RegionChoiceField(queryset=ElectionInstance.objects.filter(election_event = settings.ELECTIONS_ELECTION_EVENT_ID).order_by('name'), required=True, empty_label=_('Select your region'))

class SmsForm(BetterForm, TemplateForm):
    phone       = DutchMobilePhoneField(label=_('Mobile phone number'), required=False)
