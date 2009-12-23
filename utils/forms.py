from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.template import loader, Context

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

class TemplateForm(object):
    """
    Mixin to render forms from a predefined template
    
    Give the form a _template_name property for the name of the template_name to use
    
    Example template:
    
    ``utils/forms/_form.html``:
        {% if form.errors or form.non_field_errors %}
        <tr>
            <td colspan="2" class="error">
                <div class="form-errors">
                    <span class="cross"></span>
                    <div>
                        <h1>Error</h1>
                        <ul>
                        {% for error in form.non_field_errors %}
                            <li>{{ error }}</li>
                        {% endfor %}
                        {% for field in form %}{% for error in field.errors %}
                            <li>{{ field.label }}: {{ error }}</li>
                        {% endfor %}{% endfor %}
                        </ul>        
                    </div>
                </div>
            </td>
        </tr>
        {% endif %}
        {% for field in form %}
            {% include "utils/forms/_form_field.html" %}
        {% endfor %}
    
    ``utils/forms/_form_field.html``:
        <tr {% if field.errors %}class="error"{% endif %}>
            <th {% if field.field.required %}class="required"{% endif %}>
                <label for="{{ field.auto_id }}">{{ field.label.title }}</label>
            </th>
            <td class="input">
                {{ field }}
                <div class="help">
                    {{ field.help_text }}
                </div>
            </td>
        </tr>
    """
    
    @property
    def form_class_name(self):
        return '.'.join([self.__module__, self.__class__.__name__.lower()])

    def as_template(self):
        """
        Renders a form from a template
        """
        
        template_name = getattr(self, '_template_name', 'utils/forms/_form.html')            
        self.tpl = loader.get_template(template_name)

        context_dict = dict(
            form=self,
            field_template = getattr(self, '_field_template_name', 'utils/forms/_form_field.html'),
        )

        if getattr(self, 'initial', None):
            context_dict.update(dict(initial=self.initial))
        if getattr(self, 'instance', None):
            context_dict.update(dict(instance=self.instance))
        if getattr(self, 'cleaned_data', None):
            context_dict.update(dict(cleaned_data=self.cleaned_data))

        return self.tpl.render(
            Context(context_dict)
        )