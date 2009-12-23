from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

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

