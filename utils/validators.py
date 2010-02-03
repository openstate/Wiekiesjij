"""
Holds validation functions
"""

import re
from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError

def validate_postcode(value, error_message=None):
    """
        Test if the given value is a valid postcode
        If valid it returns a cleaned up version
        raises ValidationError if not valid
    """
    if error_message is None:
        error_message = _(u'%(value)s is not a valid postalcode')
    matches = re.match('^(?P<numbers>[1-9]{1}[0-9]{3})\s*(?P<letters>[A-Z]{2})$', value.strip().upper())
    if matches is None:
        raise ValidationError(error_message % {'value': value})
    return '{0}{1}'.format(matches.group('numbers'), matches.group('letters'))

def validate_dutchbanknumber(value):
    """
        Test if the given value is a valid dutch bank account number
        if valid it returns a cleaned up version
        raises ValidationError if not valid
        
        see http://nl.wikipedia.org/wiki/Elfproef
    """
    special_cases = ['000000000', '111111110', '999999999']
    
    value = value.strip().upper()
    # Postbank numbers, we can't really validate these
    if re.match('^P[0-9]{3,7}$', value):
        return value
    
    # We only have numbers
    if re.match('^[0-9]+$', value):
        result = 0
        for position, character in enumerate(value):
            result += int(character) * (9 - position)
        
        if result % 11 == 0 and value not in special_cases:
            return value
        
    raise ValidationError(_('%(value)s is not a valid bank account number, postbank numbers should be prefixed with a P') % {'value': value})
        
        
def validate_dutchmobilephone(value, error_message=None):
    """
        Tests and cleansup a dutch mobile phone number
        We accept anything from 003106123456789 to 06
    """
    if error_message is None:
        error_message = _(u'%(value)s is not a valid mobile phone number')
        
    #Replace starting + with 00
    value = re.sub(r'^+', '00', value)
    #Replace all non numbers with nothing
    value = re.sub(r'\D+', '', value)
    
    #Starting with 06 should be replaced with 00316
    if value.startswith('06'):
        value = re.sub(r'^06', '00316', value)
    #Now validate it
    if not re.match(r'^00316\d{8}$', value):
        raise ValidationError(error_message % {'value': value})
    return value