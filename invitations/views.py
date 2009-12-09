from django.http import Http404
from django.contrib.auth import login
from django.template.context import RequestContext
from django.shortcuts import render_to_response, redirect

from invitations.models import Invitation
from invitations.forms import AcceptInvitationForm, ExistingUserForm



def index(request, hash):
    try:
        invitation = Invitation.objects.get(hash=hash)
    except Invitation.DoesNotExist:
        #TODO: Redirect to a page
        raise Http404('Invitation does not exist')
        
    if invitation.accepted:
        #TODO: Redirect to view from invitation
        return redirect('invitations.fake')
    
    return render_to_response('invitations/index.html', {'invitation': invitation}, context_instance=RequestContext(request))
    
    
def accept(request, hash):
    try:
        invitation = Invitation.objects.get(hash=hash)
    except Invitation.DoesNotExist:
        #TODO: Redirect to a page
        raise Http404('Invitation does not exist')
        
    if invitation.accepted:
        #TODO: Redirect to view from invitation
        return redirect('invitations.fake')
        
    if request.method == 'POST':
        form = AcceptInvitationForm(data=request.POST)
        if form.is_valid():
            user = invitation.user_to
            
            user.set_password(form.cleaned_data['password'])
            user.is_active = True
            user.save()
            
            invitation.accepted = True
            invitation.save()
            #TODO: Redirect to view from invitation
            return redirect('invitations.fake')
    else:
        form = AcceptInvitationForm()
        
        
    return render_to_response('invitations/accept.html', {'invitation': invitation, 'form': form}, context_instance=RequestContext(request))
    
def existing(request, hash):
    try:
        invitation = Invitation.objects.get(hash=hash)
    except Invitation.DoesNotExist:
        #TODO: Redirect to a page
        raise Http404('Invitation does not exist')
        
    if invitation.accepted:
        #TODO: Redirect to view from invitation
        return redirect('invitations.fake')
        
    if request.method == 'POST':
        form = ExistingUserForm(profile_class=invitation.user_to.profile.__class__.__name__, data=request.POST)
        if form.is_valid():
            login(request, form.user) #login the user
            #TODO: replace the user in the invitation user_to with this one and also update all relations, profile app should handle this?
            
            invitation.accepted = True
            invitation.save()
            #TODO: Redirect to view from invitation
            return redirect('invitations.fake')
    else:
        form = ExistingUserForm(profile_class=invitation.user_to.profile.__class__.__name__)
        
    return render_to_response('invitations/existing.html', {'invitaiton': invitation, 'form': form}, context_instance=RequestContext(request))

def fake(request):
    return render_to_response('invitations/fake.html', {}, context_instance=RequestContext(request))