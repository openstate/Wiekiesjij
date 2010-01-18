from django.contrib.auth import login, authenticate
from django.template.context import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_str

from backoffice.decorators import staff_required
from elections.functions import replace_user
from invitations.models import Invitation
from invitations.forms import AcceptInvitationForm, ExistingUserForm


def index(request, hash):
    try:
        invitation = Invitation.objects.get(hash=hash)
    except Invitation.DoesNotExist:
        return redirect('invitations.notexist')
    
    if invitation.accepted or invitation.user_to.is_active:
        if not request.user.is_authenticated():
            return redirect('%s?next=%s' % (reverse('bo.login'), invitation.view))
        return redirect(invitation.view)
    
    return render_to_response('invitations/index.html', {'invitation': invitation}, context_instance=RequestContext(request))
    
    
def accept(request, hash):
    try:
        invitation = Invitation.objects.get(hash=hash)
    except Invitation.DoesNotExist:
        return redirect('invitations.notexist')
        
    if invitation.accepted or invitation.user_to.is_active:
        if not request.user.is_authenticated():
            return redirect('%s?next=%s' % (reverse('bo.login'), invitation.view))
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
            return redirect('%s?next=%s' % (reverse('bo.login'), invitation.view))
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
    if request.method == 'POST':
        for item, value in request.POST.iteritems():
            if not item.startswith('filter_'):
                continue
            _, key = item.split('_', 2)
            if key == 'accepted':
                key = 'accepted__isnull'
                if value != '':
                    value = (value == 'true')
                else:
                    value = None
            if value and value is not None:
                context.update({item: request.POST.get(item, '')})
                invitations = invitations.filter(**{smart_str(key): value})
    
    context.update({'invs': invitations})
    return render_to_response('invitations/list.html', context, context_instance=RequestContext(request))

@staff_required
def send(request, id):
    invitation = get_object_or_404(Invitation, pk=id)
    
    if request.method == 'POST':
        pass
    else:
        pass
    return render_to_response('invitations/send.html', context, context_instance=RequestContext(request))
    
def notexist(request):
    
    return render_to_response('invitations/notexist.html', {}, context_instance=RequestContext(request))