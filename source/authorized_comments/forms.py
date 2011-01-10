from django import forms
from django.contrib.comments.forms import CommentForm
from authorized_comments.models import AuthorizedComment

class AuthorizedCommentForm(CommentForm):
    name = forms.CharField(max_length=50, widget=forms.HiddenInput)
    email = forms.CharField(widget=forms.HiddenInput)
    url = forms.CharField(widget=forms.HiddenInput, required=False)

    def get_comment_model(self):
        # Use our custom comment model instead of the built-in one.
        return AuthorizedComment

    def get_comment_create_data(self):
        # Use the data of the superclass, and add in the title field
        data = super(AuthorizedCommentForm, self).get_comment_create_data()
        return data
    