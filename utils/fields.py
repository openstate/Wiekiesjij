"""
Holds fields
"""
import re

from django.utils.translation import ugettext_lazy as _
from django.forms.fields import CharField, RegexField, URLField
from django.forms.fields import MultiValueField, EMPTY_VALUES
from django.forms.util import ErrorList
from django.forms import ValidationError

from utils.validators import validate_dutchbanknumber, validate_postcode
from utils.widgets import AddressWidget, NameWidget, HiddenAddressWidget, HiddenNameWidget, ClearableFileInput

from django import forms

class FakeEmptyFieldFile(object):
    """
    A fake FieldFile that will convice a FileField model field to
    actually replace an existing file name with an empty string.
    
    FileField.save_form_data only overwrites its instance data if the
    incoming form data evaluates to True in a boolean context (because
    an empty file input is assumed to mean "no change"). We want to be
    able to clear it without requiring the use of a model FileField
    subclass (keeping things at the form level only). In order to do
    this we need our form field to return a value that evaluates to
    True in a boolean context, but to the empty string when coerced to
    unicode. This object fulfills that requirement.

    It also needs the _committed attribute to satisfy the test in
    FileField.pre_save.

    This is, of course, hacky and fragile, and depends on internal
    knowledge of the FileField and FieldFile classes. But it will
    serve until Django FileFields acquire a native ability to be
    cleared (ticket 7048).

    """
    def __unicode__(self):
        return u''
    _committed = True

class ClearableFileField(forms.MultiValueField):
    default_file_field_class = forms.FileField
    widget = ClearableFileInput
    
    def __init__(self, file_field=None, template=None, *args, **kwargs):
        file_field = file_field or self.default_file_field_class(*args,
                                                                  **kwargs)
        fields = (file_field, forms.BooleanField(required=False))
        kwargs['required'] = file_field.required
        kwargs['widget'] = self.widget(file_widget=file_field.widget,
                                       template=template)
        super(ClearableFileField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list[1] and not data_list[0]:
            return FakeEmptyFieldFile()
        return data_list[0]

class ClearableImageField(ClearableFileField):
    default_file_field_class = forms.ImageField

class PartialRequiredMultiValueField(MultiValueField):
    """
        Overwrites the default django multivalue field.
        Instead of checking the required for ALL fields we don't throw errors
    """
    
    fields_required = []
    
    def __init__(self, fields=(), *args, **kwargs):
        for f in fields:
            self.fields_required.append(bool(f.required))
        self.fields = fields
        super(MultiValueField, self).__init__(fields, *args, **kwargs)
        
    def clean(self, value):
        """
        Validates every value in the given list. A value is validated against
        the corresponding Field in self.fields.

        For example, if this MultiValueField was instantiated with
        fields=(DateField(), TimeField()), clean() would call
        DateField.clean(value[0]) and TimeField.clean(value[1]).
        
        Added the field specific required check
        """
        clean_data = []
        errors = ErrorList()
        if not value or isinstance(value, (list, tuple)):
            if not value or not [v for v in value if v not in EMPTY_VALUES]:
                if self.required:
                    raise ValidationError(self.error_messages['required'])
                else:
                    return self.compress([])
        else:
            raise ValidationError(self.error_messages['invalid'])
        for i, field in enumerate(self.fields):
            try:
                field_value = value[i]
            except IndexError:
                field_value = None
            if self.required and field_value in EMPTY_VALUES and self.fields_required[i]:
                raise ValidationError(self.error_messages['required'])
            try:
                clean_data.append(field.clean(field_value))
            except ValidationError, e:
                # Collect all validation errors in a single list, which we'll
                # raise at the end of clean(), rather than raising a single
                # exception for the first error we encounter.
                errors.extend(e.messages)
        if errors:
            raise ValidationError(errors)
        return self.compress(clean_data)
    

class DutchBankAccountField(CharField):
    """
    Validates input for valid dutch bank account numbers
    """
    
    def __init__(self, *args, **kwargs):
        if not 'max_length' in kwargs.keys():
            kwargs.update({'max_length': 9})
        if not 'help_text' in kwargs.keys():
            kwargs.update({'help_text': _("Postbank numbers should be prefixed with a 'P'")})
        super(DutchBankAccountField, self).__init__(*args, **kwargs)

    def clean(self, value):
        return validate_dutchbanknumber(value)
        
class DutchPostcodeField(CharField):
    """
    Validates input for valid dutch postcode
    """
    
    default_error_messages = {
        'invalid_postalcode': _(u'%(value)s is not a valid postalcode'),
    }
    
    def __init__(self, *args, **kwargs):
        if not 'min_length' in kwargs.keys():
            kwargs.update({'min_length': 6})
        if not 'max_length' in kwargs.keys():
            kwargs.update({'max_length': 7})
        if not 'help_text' in kwargs.keys():
            kwargs.update({'help_text': _('For example 1234 AA')})
        super(DutchPostcodeField, self).__init__(*args, **kwargs)
    
    def clean(self, value):
        return validate_postcode(value, self.error_messages['invalid_postalcode'])

class AddressField(MultiValueField):
    """
        Multi widget for the address and the house number
    """
    widget = AddressWidget
    hidden_widget = HiddenAddressWidget
    default_error_messages = {
        'required': _(u'The address fields are (all) required')
    }
    
    def __init__(self, *args, **kwargs):
        postal_code_errors_messages = {
            'max_length': _(u'Ensure the postalcode has at most %(max)d characters (it has %(length)d).'),
            'min_length': _(u'Ensure the postalcode has at least %(min)d characters (it has %(length)d).'),
            'invalid_postalcode': _(u'%(value)s is not a valid postalcode'),
        }
        fields = (
            CharField(),
            RegexField(regex='^\d+.*$', error_message=_(u'Housenumber should start with a number')),
            DutchPostcodeField(error_messages=postal_code_errors_messages),
            CharField(),
        )
        super(AddressField, self).__init__(fields, *args, **kwargs)
        
        
    def compress(self, data_list):
        """
            returns a dict with the values
        """
        return {
            'street': data_list[0],
            'number': data_list[1],
            'postalcode': data_list[2],
            'city': data_list[3],
        }
        
        
class NameField(PartialRequiredMultiValueField):
    """
        Multi widget for filling in your name
    """
    widget = NameWidget
    hidden_widget = HiddenNameWidget
    default_error_messages = {
        'required': _(u'The first and last name field are required')
    }
    
    def __init__(self, *args, **kwargs):        
        fields = (
            CharField(**kwargs.get('first_name_kwargs', {})),
            CharField(**kwargs.get('last_name_kwargs', {})),
            CharField(**kwargs.get('middle_name_kwargs', {'required': False})),
        )
        super(NameField, self).__init__(fields, *args, **kwargs)
        
    def compress(self, data_list):
        """
            Returns a dict with the values
        """
        return {
            'first_name': data_list[0],
            'middle_name': data_list[2],
            'last_name': data_list[1],
        }
    
    
class YoutubeURLField(URLField):
    """
        Does an extra regex check on the url to see if it's a valid youtube url
    """
    default_error_messages = {
        'invalid': _(u'Enter a valid URL.'),
        'invalid_link': _(u'This URL appears to be a broken link.'),
        'invalid_youtube_link': _(u'This does not appear to be an valid youtube url.'),
    }
    

    def clean(self, value):
        value = super(YoutubeURLField, self).clean(value)
        regex = re.compile(r"^(http://)?(www\.)?(youtube\.com/watch\?v=)?([A-Za-z0-9\-=_]{11})")
        match = regex.match(value)
        if value and not match: 
            raise ValidationError(self.error_messages['invalid_youtube_link'])
            
        return value