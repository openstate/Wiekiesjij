from django import forms
from django.contrib.auth.models import User
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _


from form_utils.forms import BetterForm
from utils.formutils import TemplateForm
from utils.fields import NameField

class RegistrationForm(BetterForm, TemplateForm):
    """
        Form for visitor registration
    """
    email = forms.EmailField(label=_('Email address'))
    password = forms.CharField(label=_('Password'), widget=forms.widgets.PasswordInput(render_value=False))
    password_again = forms.CharField(label=_('Password again'), widget=forms.widgets.PasswordInput(render_value=False))
    
    
    name = NameField(label=_('Name'))
        
    tos = forms.BooleanField(widget=forms.CheckboxInput(),
                                 label=_(u'Servicevoorwaarden'),
                                 help_text=_('I have read and agree to the <a href="%(url)s">Terms of Service</a>' % {'url': '/algemene-voorwaarden/'}),
                                 error_messages={ 'required': _("You must agree to the terms to register") })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if email:
            if User.objects.filter(email__iexact=self.cleaned_data['email']):
                raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
                
        return email
        
    def clean(self):
        password = self.cleaned_data.get('password')
        password_again = self.cleaned_data.get('password_again')
        
        if password and password_again and password != password_again:
            # Assigning the error to the password_again field
            self._errors['password_again'] = ErrorList([_('Passwords did not match')])

            #Remove the field from the cleaned data
            del self.cleaned_data['password']
            del self.cleaned_data['password_again']
            
        #Split up name
        name = self.cleaned_data.get('name')
        
        if name:
            self.cleaned_data['first_name'] = name['first_name']
            self.cleaned_data['middle_name'] = name['middle_name']
            self.cleaned_data['last_name'] = name['last_name']
            
        return self.cleaned_data
        
    
    
    