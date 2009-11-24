"""
Holds widgets
"""
import re
from utils.validators import validate_dutchbanknumber
from django.forms.field import CharField

class DutchBankAccountField(CharField):
    """
    Validates input against elfproof check.
    """

    def clean(self, value):
        return validate_dutchbanknumber(value)