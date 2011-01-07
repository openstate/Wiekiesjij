"""
    This app extends the standard Django Comments Framework,
    but uses any logged in user as commenter.
    If no user is logged in, no comments can be made.
"""

__author__="jan.harkema@getlogic.nl" #Little ego trippin'

from authorized_comments.models import AuthorizedComment
from authorized_comments.forms import AuthorizedCommentForm

def get_model():
    return AuthorizedComment

def get_form():
    return AuthorizedCommentForm
