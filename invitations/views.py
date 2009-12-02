from django.shortcuts import render_to_response

from random import seed, choice
import string


def index(request):
    return render_to_response('invitations/invitation.html')

def generate_hash(self):
    """
    Generates a 32 characters hash with [a-zA-Z0-9]
    """
    seed()
    chars = string.letters + string.digits
    return ''.join([choice(chars) for i in range(15)])
