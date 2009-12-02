from form_utils.forms import BetterModelForm
from utils.forms import TemplateForm
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from political_profiles.models import PoliticalExperience, Education, WorkExperience, Link, Interest, Appearence, PoliticianProfile, ChanceryProfile, ContactProfile, VisitorProfile


class PoliticianProfileForm(BetterModelForm, TemplateForm):
    '''
    PoliticianProfile admin
    '''

    class Meta:
        model = PoliticianProfile



class ChanceryProfileForm(BetterModelForm, TemplateForm):
    '''
    ChanceryProfile admin
    '''

    class Meta:
        model = ChanceryProfile


class ContactProfileForm(BetterModelForm, TemplateForm):
    '''
    Contact Profile admin
    '''

    class Meta:
        model = ContactProfile

class LinkForm(BetterModelForm, TemplateForm):
    '''
    Link admin
    '''

    class Meta:
        model = Link

class InterestForm(BetterModelForm, TemplateForm):
    '''
    Interest admin
    '''

    class Meta:
        model = Interest

class AppearenceForm(BetterModelForm, TemplateForm):
    '''
    Appearence admin
    '''

    class Meta:
        model = Appearence

class WorkExperienceForm(BetterModelForm, TemplateForm):
    '''
    WorkExperience admin
    '''

    class Meta:
        model = WorkExperience

class EducationForm(BetterModelForm, TemplateForm):
    '''
    Education admin
    '''

    class Meta:
        model = Education

class PoliticalExperienceForm(BetterModelForm, TemplateForm):
    '''
    PoliticalExperience admin
    '''

    class Meta:
        model = PoliticalExperience


