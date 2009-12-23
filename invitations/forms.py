from django import forms
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate


from form_utils.forms import BetterForm
from utils.formutils import TemplateForm


class AcceptInvitationForm(BetterForm, TemplateForm):
    """
        Form for when an invitation is accepted
    """
    
    password = forms.CharField(label=_('Password'), widget=forms.widgets.PasswordInput(render_value=False))
    password_again = forms.CharField(label=_('Password again'), widget=forms.widgets.PasswordInput(render_value=False))
    
    def clean(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        
        if password and password_again and password != password_again:
            # Assigning the error to the password_again field
            self._errors['password_again'] = ErrorList([_('Passwords did not match')])

            #Remove the field from the cleaned data
            del self.cleaned_data['password']
            del self.cleaned_data['password_again']
            
        return self.cleaned_data

class ExistingUserForm(BetterForm, TemplateForm):
    """
        Form for when the user indicates he/she has an existing account
    """
    
    username = forms.CharField(label=_('Email address'))
    password = forms.CharField(label=_('Password'), widget=forms.widgets.PasswordInput(render_value=False))
    
    def __init__(self, profile_class, *args, **kwargs):
        self.profile_class = profile_class
        self.user = None
        super(ExistingUserForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            #Authenticate (Does NOT login the user)
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                self._errors['password'] = ErrorList([_('Username or password incorrect')])
                del self.cleaned_data['username']
                del self.cleaned_data['password']
            elif self.user.profile.__class__.__name__ != self.profile_class:
                self._errors['password'] = ErrorList([_('This is another type of user then the one this invitation is ment for')])
                del self.cleaned_data['username']
                del self.cleaned_data['password']
                self.user = None
                
        return self.cleaned_data