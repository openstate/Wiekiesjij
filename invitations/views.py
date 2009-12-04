from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django import forms

from invitations.models import CandidateInvitation
from django.contrib.auth.models import User

from random import seed, choice
import string

SUBJECT = "Uitnodiging Wiekiesjij"

MESSAGE = """
Geachte %s %s,

U bent uitgenodigd door %s op de website 'Wie Kies Jij'.

Om uw uitnodiging te accepteren en uw profiel te activeren gebruik de onderstaande link:
http://localhost:8000/invitations/activate/%s
"""

RECIPIENT = 'harrie.bos@accepte.nl'

#TODO: fix this when the auth system is ready
USER_TEST = "Harrie"

#a class to define the form
class InvitationForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

class InvitationActivationForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    password_again = forms.CharField(widget=forms.PasswordInput)
    
def index(request):
    """
    This method will load at the URI /invitation/
    If the request not is 'POST' than a form will be created and parsed to the template
    If the request is 'POST' than it will check if the form is valid.
    If the form is valid the data will be saved in the database for the contact profile wich the receiver has to activate.
    """
    if request.method == 'POST':
        form = InvitationForm(request.POST)
        #checks if form is valid
        if form.is_valid():
            #clean all the data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            #we make a hash
            try:
                hash = generate_hash()
            except KeyError, ValueError:
                return KeyError + ValueError
            #setting up the email message
            msg = MESSAGE % (first_name, last_name, USER_TEST, hash)

            user_from = User.objects.get(username='polichism')
            
            if not User.objects.filter(username=email):
                user_object = User.objects.create_user(email, email, generate_hash())
                user_object.is_staff = False
                user_object.save()
                user_to = user_object
            else:
                user_to = User.objects.get(username=email)
            #TODO: input the view, for instance: chancery, politician, contact
            profile = CandidateInvitation(user_from=user_from, user_to=user_to, hash=hash, accepted=False, text=message, email=email)
            profile.save()
            
            #we need this libary to send mail
            from utils.emails import send_email
            send_email(SUBJECT, RECIPIENT, email, msg, {"plain": ""})

            #if all is successful, the browser wil be redirected to /
            #TODO: set a proper URI
            return HttpResponseRedirect('/invitations/sent/')
    else:
        form = InvitationForm()
    return render_to_response('invitations/invitation.html', {
        'form': form,
        })

def sent(request):
    return render_to_response('invitations/sent.html')

def activate(request, hash):
    if not hash:
        return HttpResponseRedirect('/')

    try:
        profile = CandidateInvitation.objects.get(hash=hash, accepted=False)
    except:
        raise Exception(_("No entry found in the database with this hash. (Hash is not valid, or hash is allready used"))

    if request.method == 'POST':
        form = ''
        password = forms.cleaned_data['password']
        password_again = forms.clean_data['password']

    return render_to_response('invitations/activate.html', {
        'hash' : hash,
        'profile' : profile
    })

def generate_hash():
    """
    Generates a 32 characters hash with [a-zA-Z0-9]
    """
    seed()
    chars = string.letters + string.digits
    return ''.join([choice(chars) for i in range(32)])
