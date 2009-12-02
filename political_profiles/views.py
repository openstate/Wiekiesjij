from django.shortcuts import render_to_response

from random import seed, choice
import string

def index(request):
    return render_to_response('invitations/invitation.html')

def send_invitation(request, post):
    return render_to_response('invitations/complete.html')

def generate_hash():
    seed()
    chars = string.letters + string.digits
    return ''.join([choice(chars) for i in range(32)])
