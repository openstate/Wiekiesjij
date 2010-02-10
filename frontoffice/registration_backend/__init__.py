from random import seed, choice
import string

from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from registration.backends.default import DefaultBackend
from registration import signals
from registration.models import RegistrationProfile

from frontoffice.registration_backend.forms import RegistrationForm
from utils.emails import send_email
from elections.functions import get_profile_model

class VisitorBackend(DefaultBackend):
    """
        Extends the default registration backend to use the data
    """
    
    def _generate_username(self):
        """ Generate a random username """
        seed()
        chars = string.letters + string.digits
        return ''.join([choice(chars) for i in range(29)])
    
    def register(self, request, **kwargs):
        email, password = kwargs['email'], kwargs['password']
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        username = self._generate_username()
        new_user = RegistrationProfile.objects.create_inactive_user(username, email, password, site, send_email=False)


        send_email(
                _('Wiekiesjij - User Registration'),
                'bmcmahon@gmail.com',
                email,
                {'site': site, 'activation_key': new_user.activation_key },
                {'plain': 'frontoffice/registration/activation_email.txt','html': 'frontoffice/registration/_activation_email.html'},
        )

 
        ProfileModel = get_profile_model('visitor')
        
        ProfileModel.objects.create(
            first_name=kwargs['first_name'],
            middle_name=kwargs['middle_name'],
            last_name=kwargs['last_name'],
            user=new_user,
        )
        
        signals.user_registered.send(sender=self.__class__, user=new_user, request=request)
        
        return new_user
    
    def get_form_class(self, request):
        """
            Return the default form class used for user registration.

        """
        return RegistrationForm