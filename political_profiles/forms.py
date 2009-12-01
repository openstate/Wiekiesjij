from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from political_profiles.models import PoliticalExperience, Education, WorkExperience, Link, Interest, Appearence, PoliticianProfile, ChanceryProfile, ContactProfile, VisitorProfile
from django.contrib.formtools.wizard import FormWizard

class PoliticianProfileForm(forms.ModelForm):
    '''
    PoliticianProfile admin
    '''

    class Meta:
        model = PoliticianProfile



class ChanceryProfileForm(forms.ModelForm):
    '''
    ChanceryProfile admin
    '''

    class Meta:
        model = ChanceryProfile


class ContactProfileForm(forms.ModelForm):
    '''
    Contact Profile admin
    '''

    class Meta:
        model = ContactProfile

class LinkForm(forms.ModelForm):
    '''
    Link admin
    '''

    class Meta:
        model = Link

class InterestForm(forms.ModelForm):
    '''
    Interest admin
    '''

    class Meta:
        model = Interest

class AppearenceForm(forms.ModelForm):
    '''
    Appearence admin
    '''

    class Meta:
        model = Appearence

class WorkExperienceForm(forms.ModelForm):
    '''
    WorkExperience admin
    '''

    class Meta:
        model = WorkExperience

class EducationForm(forms.ModelForm):
    '''
    Education admin
    '''

    class Meta:
        model = Education

class PoliticalExperienceForm(forms.ModelForm):
    '''
    PoliticalExperience admin
    '''

    class Meta:
        model = PoliticalExperience