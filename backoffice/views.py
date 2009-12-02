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
from elections.models import ElectionEvent
#from elections import forms
from utils.multipathform import MultiPathFormWizard, Step
from elections.forms import ElectionInstanceForm, CouncilForm
from political_profiles.forms import ChanceryProfileForm


#@login_required
def election_event(request):
    election_events = ElectionEvent.objects.all()

    return render_to_response('backoffice/election_event_view.html', {'election_events': election_events,},
                              context_instance=RequestContext(request))

def election_instance_add(request):

    step_args = dict(
            forms = dict( #list of forms for this page as name => form_class
                    chancery_form = ChanceryProfileForm,
                    election_instance_form        = ElectionInstanceForm,
                    council_form       = CouncilForm,
                    
                ),
            prefixes = dict( # name => prefix; if not set, then name is used
                    
                ),
            initial = dict( # initial value (dict, model object, query set etc)
                    chancery_form = None,
                    election_instance_form     = None,
                    council_form = None,
                    
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

