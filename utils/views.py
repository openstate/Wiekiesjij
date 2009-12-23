from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.decorators.cache import never_cache
from django.template import RequestContext
from django.contrib.sites.models import Site, RequestSite

from forms import EmailAuthForm

def login(request,
        template_name='registration/login.html',    
        redirect_field_name=REDIRECT_FIELD_NAME):
    '''
    Displays the login form and handles the login action.
    
    Rewrite of django.contrib.auth.views.login to use custom
    form to enable email / password login instead of username / password.
    '''

    redirect_to = request.REQUEST.get(redirect_field_name, '')
    # Light security check -- make sure redirect_to isn't garbage.
    if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
        redirect_to = settings.LOGIN_REDIRECT_URL
    if settings.EMAIL_AUTH_REDIRECT and request.user.is_authenticated():
        return HttpResponseRedirect(redirect_to)
        
    if request.method == "POST":
        form = EmailAuthForm(data = request.POST)
        if form.is_valid():

            from django.contrib.auth import login
            login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return HttpResponseRedirect(redirect_to)
    else:
        form = EmailAuthForm(request)

    request.session.set_test_cookie()
    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)
    return render_to_response(template_name, {
        'form': form,
        redirect_field_name: redirect_to,
        'site_name': current_site.name,
    }, context_instance=RequestContext(request))
login = never_cache(login)
