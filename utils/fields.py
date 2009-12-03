"""
Holds fields
"""
import re
from django.utils.translation import ugettext_lazy as _
from django.forms.fields import CharField, MultiValueField, RegexField

from utils.validators import validate_dutchbanknumber, validate_postcode
from utils.widgets import AddressWidget

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
        return " ".join(data_list)
    