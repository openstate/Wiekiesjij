import os.path
import os
#!/usr/env python
#-*- coding: utf-8 -*-
#
#Copyright 2009 Accepte. All Rights Reserved.
import datetime
import time
import csv
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext, ugettext_lazy as _
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required

from elections.settings import ELECTION_EVENT_ID
from elections.models import ElectionEvent, ElectionInstance, ElectionInstanceParty
from political_profiles import functions
from utils.multipathform import MultiPathFormWizard, Step
from backoffice.decorators import staff_required, council_admin_required

from backoffice.wizards import AddElectionInstanceWizard, ElectionSetupWizard, EditElectionInstanceWizard
# Even though your IDE (or your brains) might say this is an unused import,
# please do not remove the following Form imports
# FIXME: Remove import * once the test functions can be removed !
from backoffice.wizards import *
from political_profiles.forms import *
from elections.forms import *


def election_instance_view(request, id):
    instance = get_object_or_404(ElectionInstance, pk=id)
    return render_to_response('backoffice/election_instance_view.html', {'instance': instance}, context_instance=RequestContext(request))

def election_party_view(request, id):
    eip = get_object_or_404(ElectionInstanceParty, pk=id)
    return render_to_response('backoffice/election_party_view.html', {'instance': eip.election_instance, 'eip': eip}, context_instance=RequestContext(request))

def election_party_create(request, id, position):
    instance = get_object_or_404(ElectionInstance, pk=id)
    wizard = AddElectionPartyWizard(instance, position)
    return wizard(request)

def election_party_edit(request, id):
    eip = get_object_or_404(ElectionInstanceParty, pk=id)
    wizard = ElectionPartySetupWizard(eip)
    return wizard(request)

#@login_required
def election_event(request):
    election_instances = ElectionInstance.objects.filter(election_event__pk=ELECTION_EVENT_ID)
    return render_to_response('backoffice/election_event_view.html', {'election_instances': election_instances,},
                              context_instance=RequestContext(request))


@staff_required
def add_election_instance(request):
    wizard = AddElectionInstanceWizard()
    return wizard(request)
    
@staff_required
def edit_election_instance(request, id):
    wizard = EditElectionInstanceWizard(id)
    return wizard(request)


#TODO: This can probably be neater. I don't see why we would need step_args for example.
def form_view(request, form_type):
    try:
        formslist = dict(
            generic_form = globals()[form_type],
        )
    except KeyError:
        raise NameError('%s is not an existing form\nHave you checked your imports?' % (form_type))

    steps = Step('add_election_instance', forms=formslist, template='backoffice/wizard/step1.html')
    generic_form = MultiPathFormWizard(steps)
    return generic_form(request)

def wizard_view(request, wizard_type):
    try:
        wizard = globals()[wizard_type]
    except KeyError:
        raise NameError('%s is not an existing wizard\nHave you checked your imports?' % (wizard_type))
        
    return wizard()(request)

def election_setup(request, election_instance_id, user_id=None):
    '''
    Election setup wizard.
    @param int election_instance_id
    @param int user_id

    Both parameters are required. It's obvious what they mean.
    '''
    if not user_id:
        user_id = request.user.id

    return ElectionSetupWizard(election_instance_id=election_instance_id, user_id=user_id)(request)

def election_setup_done(request):
    '''
    Election setup wizard success page.
    '''
    return render_to_response('backoffice/wizard/election_setup/done.html',
                              context_instance=RequestContext(request))

def politician_welcome(request):
    return render_to_response('backoffice/wizard/politician_profile/welcome.html',
                              context_instance=RequestContext(request))

def politician_profile_setup(request, user_id):
    return PoliticianProfileWizard(user_id=user_id)(request)

def politician_profile_setup_done(request, user_id):
    return render_to_response('backoffice/wizard/politician_profile/done.html',
                              {'user_id': user_id},
                              context_instance=RequestContext(request))

def politician_profile_interest(request, user_id):
    return render_to_response('backoffice/wizard/politician_profile/interest.html',
                              {'user_id': user_id},
                              context_instance=RequestContext(request))

def politician_profile_interest_wizard(request, user_id):
    return PoliticianProfileInterestWizard(user_id=user_id)(request)

def politician_profile_work(request, user_id):
    return render_to_response('backoffice/wizard/politician_profile/work.html',
                              {'user_id': user_id},
                              context_instance=RequestContext(request))

def politician_profile_work_wizard(request, user_id):
    return PoliticianProfileWorkWizard(user_id=user_id)(request)


def politician_profile_political(request, user_id):
    return render_to_response('backoffice/wizard/politician_profile/political.html',
                              {'user_id': user_id},
                              context_instance=RequestContext(request))

def politician_profile_political_wizard(request, user_id):
    return PoliticianProfilePoliticalWizard(user_id=user_id)(request)

def politician_profile_education(request, user_id):
    return render_to_response('backoffice/wizard/politician_profile/education.html',
                              {'user_id': user_id},
                              context_instance=RequestContext(request))

def politician_profile_education_wizard(request, user_id):
    return PoliticianProfileEducationWizard(user_id=user_id)(request)

def politician_profile_appearance(request, user_id):
    return render_to_response('backoffice/wizard/politician_profile/appearances.html',
                              {'user_id': user_id},
                              context_instance=RequestContext(request))

def politician_profile_appearance_wizard(request, user_id):
    return PoliticianProfileAppearanceWizard(user_id=user_id)(request)


def politician_profile_link(request, user_id):
    return render_to_response('backoffice/wizard/politician_profile/links.html',
                              {'user_id': user_id},
                              context_instance=RequestContext(request))

def politician_profile_link_wizard(request, user_id):
    return PoliticianProfileLinkWizard(user_id=user_id)(request)

def council_edit(request, id):
    '''
    Council edit wizard.
    @param int id election_instance_id
    '''
    instance = get_object_or_404(ElectionInstance, pk=id)
    return CouncilEditWizard(election_instance=instance)(request)

def csv_import_candidates_step1(request):
    return render_to_response('backoffice/csv_candidates_1.html', context_instance=RequestContext(request))

def csv_import_candidates_step2(request):
    if(request.FILES or request.POST):
        form = CsvUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.files['file']
            filename = str(time.time()) + '.csv' #about 1000 unique filenames per second?
            destination = open(settings.settings.TMP_ROOT + '/' + filename, 'wb+')

            for chunk in file.chunks():
                destination.write(chunk)

            destination.close()
            request.session['csv_filename'] = filename

            candidates = functions.get_candidates_from_csv(request.session)
    else:
        form = CsvUploadForm()

    forms = dict({'csv_upload': form})
    return render_to_response('backoffice/csv_candidates_2.html', {'forms':forms,}, context_instance=RequestContext(request))

def council_edit(request, election_instance_id, user_id):
    '''
    Council edit wizard.
    @param int election_instance_id
    @param int user_id

    Both parameters are required. It's obvious what they mean.
    '''
    return CouncilEditWizard(election_instance_id=election_instance_id, user_id=user_id)(request)

def council_edit_done(request):
    '''
    Council edit wizard success page.
    '''
    return render_to_response('backoffice/wizard/council/edit/done.html',
                              context_instance=RequestContext(request))