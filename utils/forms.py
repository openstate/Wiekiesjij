from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from utils.fields import GenerateMultipleModelChoiceField, GenerateModelChoiceField
from form_utils.forms import BetterForm, BetterModelForm
from utils.formutils import TemplateForm
from django.forms import widgets
class EmailAuthForm(AuthenticationForm):	
    """
    Extends to:
    - remove username field [has too-small maxlength, and does not aid autocomplete]
    - add email field
    - rewrite some hard-coded strings	
    """	
    
    def __init__(self, *args, **kwargs):
        super(EmailAuthForm, self).__init__(*args, **kwargs)

        # Remove username field
        del self.fields['username']
        # Add email address field - done this way to ensure it comes first in list of fields
        self.fields.insert(0, 'email', forms.EmailField(label = _("Email Address")))

    def clean(self):
        ''' Overwrite to rewrite hard-coded strings and get the right form data '''

        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_("Please enter a correct email address and password. Note that your password is case-sensitive."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("This account is inactive."))

        # TODO: determine whether this should move to its own method.
        if self.request:
            if not self.request.session.test_cookie_worked():		
                raise forms.ValidationError(_("Your Web browser doesn't appear to have cookies enabled. Cookies are required for logging in."))

        return self.cleaned_data



class ModelMultiAnswerForm(BetterForm, TemplateForm):
    value = GenerateMultipleModelChoiceField(queryset=None, widget=widgets.CheckboxSelectMultiple)

    def __init__(self, queryset=None, attribute=None, empty_label=None, *args, **kwargs):
        super(ModelMultiAnswerForm, self).__init__(*args, **kwargs)

        try:
            self.fields['value'].attribute=attribute
            self.fields['value'].empty_label = empty_label
            self.fields['value'].queryset = queryset

        except Exception:
            raise ModelAnswerFormError(_('You need to provide a model to the ModelMiltiAnswerForm'))

    def clean(self):
        ''' Overwrite to rewrite hard-coded strings and get the right form data '''

        return self.cleaned_data


class ModelAnswerForm(BetterForm, TemplateForm):
    value = GenerateModelChoiceField(queryset=None, widget=widgets.RadioSelect)

    def __init__(self, queryset=None, attribute=None, empty_label=None, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


        try:
            self.fields['value'].attribute=attribute
            self.fields['value'].empty_label = empty_label
            self.fields['value'].queryset = queryset

        except Exception:
            raise ModelAnswerFormError(_('You need to provide a model to the ModelAnswerForm'))

    def clean(self):
        ''' Overwrite to rewrite hard-coded strings and get the right form data '''

        return self.cleaned_data