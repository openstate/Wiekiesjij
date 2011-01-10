from django.contrib.auth import login, authenticate, get_backends
from django.template.context import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_str
from django.utils.translation import ugettext
from django.contrib.auth.models import User
from django.db.models import Q

from backoffice.decorators import staff_required, superuser_required
from elections.functions import replace_user
from invitations.models import Invitation
from invitations.forms import AcceptInvitationForm, ExistingUserForm, ConfirmationForm

from political_profiles.models import ChanceryProfile, ContactProfile, PoliticianProfile


def index(request, hash):
    try:
        invitation = Invitation.objects.get(hash=hash)
    except Invitation.DoesNotExist:
        return redirect('invitations.notexist')
    
    if invitation.accepted or invitation.user_to.is_active:
        if not request.user.is_authenticated():
            return redirect('%s?next=%s' % (reverse('fo.login'), invitation.view))
        return redirect(invitation.view)
    
    return render_to_response('invitations/index.html', {'invitation': invitation}, context_instance=RequestContext(request))
    
    
def accept(request, hash):
    try:
        invitation = Invitation.objects.get(hash=hash)
    except Invitation.DoesNotExist:
        return redirect('invitations.notexist')
        
    if invitation.accepted or invitation.user_to.is_active:
        if not request.user.is_authenticated():
            return redirect('%s?next=%s' % (reverse('fo.login'), invitation.view))
        return redirect(invitation.view)
        
    if request.method == 'POST':
        form = AcceptInvitationForm(data=request.POST)
        if form.is_valid():
            user = invitation.user_to   
            user.set_password(form.cleaned_data['password'])
            user.is_active = True
            if user.profile:
                user.profile.terms_and_conditions = form.cleaned_data['terms_and_conditions']
                user.profile.save()
            user.save()
            
            user = authenticate(username=user.username, password=form.cleaned_data['password'])
            login(request, user) #login the user
                        
            invitation.accepted = True
            invitation.save()
            return redirect(invitation.view)
    else:
        form = AcceptInvitationForm()
        
        
    return render_to_response('invitations/accept.html', {'invitation': invitation, 'form': form}, context_instance=RequestContext(request))
    
def existing(request, hash):
    try:
        invitation = Invitation.objects.get(hash=hash)
    except Invitation.DoesNotExist:
        return redirect('invitations.notexist')
        
    if invitation.accepted or invitation.user_to.is_active:
        if not request.user.is_authenticated():
            return redirect('%s?next=%s' % (reverse('fo.login'), invitation.view))
        return redirect(invitation.view)
        
    if request.method == 'POST':
        form = ExistingUserForm(profile_class=invitation.user_to.profile.__class__.__name__, data=request.POST)
        if form.is_valid():
            login(request, form.user) #login the user
            
            #Replace the user
            replace_user(invitation.user_to, form.user)
            
            invitation.accepted = True
            invitation.save()
            return redirect(invitation.view)
    else:
        form = ExistingUserForm(profile_class=invitation.user_to.profile.__class__.__name__)
        
    return render_to_response('invitations/existing.html', {'invitaiton': invitation, 'form': form}, context_instance=RequestContext(request))

@staff_required
def list(request):
    invitations = Invitation.objects.all()
    context = {}
    name_filter = None
    email_filter = None
    if request.method == 'POST':
        for item, value in request.POST.iteritems():
            if not item.startswith('filter_'):
                continue
            _, key = item.split('_', 2)
            if not value:
                continue
            if key == 'search':
                for part in value.split():
                    if part.find('@') != -1:
                        if email_filter is None:
                            email_filter = Q(user_to__email__icontains=part)
                        else:
                            email_filter = email_filter & Q(user_to__email__icontains=part)
                    else:
                        if name_filter is None:
                            name_filter = (
                                    Q(user_to__chanceryprofile__last_name__icontains=part) | 
                                    Q(user_to__chanceryprofile__first_name__icontains=part) | 
                                    Q(user_to__chanceryprofile__middle_name__icontains=part) |
                                    Q(user_to__contactprofile__last_name__icontains=part) | 
                                    Q(user_to__contactprofile__first_name__icontains=part) | 
                                    Q(user_to__contactprofile__middle_name__icontains=part) |
                                    Q(user_to__politicianprofile__last_name__icontains=part) | 
                                    Q(user_to__politicianprofile__first_name__icontains=part) | 
                                    Q(user_to__politicianprofile__middle_name__icontains=part)
                                )
                        else:
                            name_filter = name_filter & (
                                    Q(user_to__chanceryprofile__last_name__icontains=part) | 
                                    Q(user_to__chanceryprofile__first_name__icontains=part) | 
                                    Q(user_to__chanceryprofile__middle_name__icontains=part) |
                                    Q(user_to__contactprofile__last_name__icontains=part) | 
                                    Q(user_to__contactprofile__first_name__icontains=part) | 
                                    Q(user_to__contactprofile__middle_name__icontains=part) |
                                    Q(user_to__politicianprofile__last_name__icontains=part) | 
                                    Q(user_to__politicianprofile__first_name__icontains=part) | 
                                    Q(user_to__politicianprofile__middle_name__icontains=part)
                                )
                            
                if email_filter is not None:
                    invitations = invitations.filter(email_filter)                
                    
                if name_filter is not None:
                    invitations = invitations.filter(name_filter)
                    
            else:
                if key == 'accepted':
                    if value != 'true':
                        value = 0
                    else:
                        value = 1
                if value != '':
                    invitations = invitations.filter(**{smart_str(key): value})
            context.update({item: request.POST.get(item, '')})
    
    context.update({'invs': invitations})
    return render_to_response('invitations/list.html', context, context_instance=RequestContext(request))

@staff_required
def send(request, id):
    invitation = get_object_or_404(Invitation, pk=id)
    
    context = {'invitation': invitation}
    if request.method == 'POST':
        form = ConfirmationForm(invitation=invitation, data=request.POST)
        if form.is_valid():
            invitation.send()
            request.user.message_set.create(message=ugettext('The invitation has been resend'))
            return redirect(reverse('invitations.list'))
    else:
        form = ConfirmationForm(invitation=invitation)
        
    context.update({'form': form})
    return render_to_response('invitations/send.html', context, context_instance=RequestContext(request))
    
@superuser_required
def hijack_account(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    
    #NOTE: officially we need to go through the login step first, but as we don't know the users password
    # and the user needs to have the backend used to authenticate set we'll just get the first one
    backend = get_backends()[0]
    user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
    if user.is_active:
        login(request, user)
        return redirect('bo.redirect')

    return redirect('invitations.list')
    
def notexist(request):
    
    return render_to_response('invitations/notexist.html', {}, context_instance=RequestContext(request))