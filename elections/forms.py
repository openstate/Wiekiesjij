from form_utils.forms import BetterModelForm
from utils.forms import TemplateForm
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


from utils.validators import is_valid_zipcode, is_valid_phonenumber
from utils.fields import ZipCodeField, PhoneField
from elections.models import Candidacy, Council, ElectionEvent, ElectionInstance, ElectionInstanceQuestion, Party


class CandidacyForm(BetterModelForm, TemplateForm):
    '''
    PoliticianProfile admin
    '''

    class Meta:
        model = Candidacy



class CouncilForm(BetterModelForm, TemplateForm):
    '''
    ChanceryProfile admin
    '''

    class Meta:
        model = Council


class ElectionEventForm(BetterModelForm, TemplateForm):
    '''
    Contact Profile admin
    '''

    class Meta:
        model = ElectionEvent

class ElectionInstanceForm(BetterModelForm, TemplateForm):
    '''
    Link admin
    '''

    class Meta:
        model = ElectionInstance

class ElectionInstanceQuestionForm(BetterModelForm, TemplateForm):
    '''
    Interest admin
    '''

    class Meta:
        model = ElectionInstanceQuestion

class PartyForm(BetterModelForm, TemplateForm):
    '''
    Appearence admin
    '''

    class Meta:
        model = Party
