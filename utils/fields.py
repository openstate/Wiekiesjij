from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson as json

class JsonField(models.TextField):
    """JsonField is a generic textfield that neatly serializes/unserializes
    JSON objects seamlessly"""

    # Used so to_python() is called
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""

        if value == "":
            return None

        try:
            if isinstance(value, basestring):
                return json.loads(value)
        except ValueError:
            pass

        return value

    def get_db_prep_save(self, value):
        """Convert our JSON object to a string before we save"""

        if value == "":
            return None

        if isinstance(value, dict):
            value = json.dumps(value, cls=DjangoJSONEncoder)

        return super(JsonField, self).get_db_prep_save(value)

class CurrencyField (forms.RegexField):
    """ Formfield for currencies."""
    currency_re = re.compile(r'^[0-9]{1,5}(.[0-9][0-9])?$')

    def __init__(self, *args, **kwargs):
        super(CurrencyField, self).__init__(self.currency_re, None, None, *args, **kwargs)

    def clean(self, value):
        value = super(CurrencyField, self).clean(value)
        return float(value)

class MultiEmailField(forms.Field):
    """Formfield for multiple email addresses."""
    widget = forms.Textarea(attrs={'rows': 2})

    def clean(self, value):
        """
        Check that the field contains one or more comma-separated emails
        and normalize the data to a list of the email strings.
        """
        if not value:
            raise forms.ValidationError(_('Enter at least one e-mail address.'))
        emails = value.split(',')
        emails = [email.strip() for email in emails]
        if len(emails) > settings.MAX_INVITE_MAIL_RECIPIENTS:
            raise forms.ValidationError(_('Max. {0} addresses.'.format(settings.MAX_INVITE_MAIL_RECIPIENTS)))
        for email in emails:
            if not is_valid_email(email):
                raise forms.ValidationError(_('%s is not a valid e-mail address.') % email)
        return ','.join(emails)

class ZipCodeField (forms.CharField):
    """ Formfield for Zip Codes."""
    def __init__(self, *args, **kwargs):
        super(ZipCodeField, self).__init__(*args, **kwargs)

    def clean(self, value):
        zip = value.upper()
        if not is_valid_zipcode(zip):
            raise forms.ValidationError(_('Please enter a valid zip code'))
        return zip

class PhoneField (forms.CharField):
    """ Formfield for Phone numbers, also check apps.core.formfields"""
    def __init__(self, *args, **kwargs):
        super(PhoneField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if not is_valid_phonenumber(value):
            raise forms.ValidationError(_('Please enter a valid phone number. Use 00 for a +'))
        return value

class EmailField(forms.CharField):

    def __init__(self, *args, **kwargs):
        super(GroupnameField, self).__init__(*args, **kwargs)
    def clean(self, value):
        """
        Check that the field contains one or more comma-separated emails
        and normalize the data to a list of the email strings.
        """
        if not value:
            raise forms.ValidationError(_('Enter at least one e-mail address.'))
        email = value

        if not is_valid_email(email):
            raise forms.ValidationError(_('%s is not a valid e-mail address.') % email)
        return email

