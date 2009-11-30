from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


from utils.validators import is_valid_zipcode, is_valid_phonenumber
from utils.fields import ZipCodeField, PhoneField
from elections.models import Candidacy, Council, ElectionEvent, ElectionInstance, ElectionInstanceQuestion, Party


class CandidacyForm(forms.ModelForm):
    '''
    PoliticianProfile admin
    '''

    class Meta:
        model = Candidacy



class CouncilForm(forms.ModelForm):
    '''
    ChanceryProfile admin
    '''

    class Meta:
        model = Council


class ElectionEventForm(forms.ModelForm):
    '''
    Contact Profile admin
    '''

    class Meta:
        model = ElectionEvent

class ElectionInstanceForm(forms.ModelForm):
    '''
    Link admin
    '''

    class Meta:
        model = ElectionInstance

class ElectionInstanceQuestionForm(forms.ModelForm):
    '''
    Interest admin
    '''

    class Meta:
        model = ElectionInstanceQuestion

class PartyForm(forms.ModelForm):
    '''
    Appearence admin
    '''

    class Meta:
        model = Party
