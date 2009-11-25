"""
Holds fields
"""
import re
from django.utils.translation import ugettext_lazy as _

from utils.validators import validate_dutchbanknumber, validate_postcode
from django.forms.fields import CharField

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
    
    def __init__(self, *args, **kwargs):
        if not 'min_length' in kwargs.keys():
            kwargs.update({'min_length': 6})
        if not 'max_length' in kwargs.keys():
            kwargs.update({'max_length': 7})
        if not 'help_text' in kwargs.keys():
            kwargs.update({'help_text': _('For example 1234 AA')})
        super(DutchPostcodeField, self).__init__(*args, **kwargs)
    
    def clear(self, value):
        return validate_postcode(value)
