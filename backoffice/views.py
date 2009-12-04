#!/usr/env python
#-*- coding: utf-8 -*-
#
#Copyright 2009 Accepté. All Rights Reserved.
import datetime
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext, ugettext_lazy as _
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
#import utils
from elections.models import ElectionEvent, ElectionInstance, ElectionInstanceParty
#from elections import forms
from utils.multipathform import MultiPathFormWizard, Step
# Even though your IDE (or your brains) might say this is an unused import,
# please do not remove the following Form imports
# FIXME: Remove import * once the test functions can be removed !
from political_profiles.forms import *
from elections.forms import *
from backoffice.wizards import *

def election_instance_view(request, id):
    instance = get_object_or_404(ElectionInstance, pk=id)
    return render_to_response('backoffice/election_instance_view.html', {'instance': instance}, context_instance=RequestContext(request))

def election_party_view(request, id):
    eip = get_object_or_404(ElectionInstanceParty, pk=id)
    return render_to_response('backoffice/election_party_view.html', {'instance': eip.election_instance, 'eip': eip}, context_instance=RequestContext(request))

#@login_required
def election_event(request):
    election_events = ElectionEvent.objects.all()

    return render_to_response('backoffice/election_event_view.html', {'election_events': election_events,},
                              context_instance=RequestContext(request))

def election_instance_add(request):

    step_args = dict(
            forms = dict( #list of forms for this page as name => form_class
                    #i_chancery_form = InitialChanceryProfileForm,
                    #chancery_form = ChanceryProfileForm,
                    l_chancery_form = ElectionInstanceSelectPartiesForm,
                    #council_form       = CouncilForm,
                    
                ),
            prefixes = dict( # name => prefix; if not set, then name is used
                    
                ),
            initial = dict( # initial value (dict, model object, query set etc)
                    #i_chancery_form = None,
                    #chancery_form = None,
                    l_chancery_form = None,
                    #council_form = None,
                    
                ),

            # optional extra content, will be passed to step template
            extra_context = dict(),

            # specific template for this step, optional
            #template = 'foo/bar.html'
        )

    steps = Step('add_election_instance', forms=step_args['forms'], template='backoffice/wizard/step1.html')
    
    add_election_wizard = MultiPathFormWizard(steps)

    return add_election_wizard(request)
    #return render_to_response('backoffice/add_election_instance_view.html', {'add_election_wizard': add_election_wizard},
    #                          context_instance=RequestContext(request))


#TODO: This can probably be neater. I don't see why we would need step_args for example.
def form_view(request, profile_type):
    try:
        formslist = dict(
            generic_form = globals()[profile_type],
        )
    except KeyError:
        raise NameError(profile_type + ' is not an existing form\nHave you checked your imports?')

    steps = Step('add_election_instance', forms=formslist, template='backoffice/wizard/step1.html')
    generic_form = MultiPathFormWizard(steps)
    return generic_form(request)
    
def wizard_view(request, wizard_type):
    try:
        wizard = globals()[wizard_type]
    except KeyError:
        raise NameError('%s is not an existing wizard\nHave you checked your imports?')
        
    return wizard()(request)
