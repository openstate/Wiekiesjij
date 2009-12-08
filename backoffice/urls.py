#!/usr/env python
#-*- coding: utf-8 -*-
#
#Copyright 2009 Accepté. All Rights Reserved.
from django.conf.urls.defaults import *
#from backoffice.decorators import staff_required, council_admin_required
from backoffice.wizards import AddElectionInstanceWizard

add_election_instance = AddElectionInstanceWizard() #staff_required(AddElectionInstanceWizard())


urlpatterns = patterns('',
    url(r'^$', 'backoffice.views.election_event',name='backoffice.election_event'),
    url(r'^add/$', add_election_instance, name='backoffice.add_election_instance'),
    url(r'^setup/(?P<election_instance_id>\d+)/(?P<user_id>\d+)/$', 'backoffice.views.election_setup', name='backoffice.election_setup'),
    url(r'^election_instance/(?P<id>\d+)/$', 'backoffice.views.election_instance_view', name='backoffice.election_instance_view'),
    url(r'^election_party/(?P<id>\d+)/$', 'backoffice.views.election_party_view', name='backoffice.election_party_view'),
    
    
    #TODO: Debug views remove at some point 
    url(r'^wizard/(?P<wizard_type>[-\w]+)/$', 'backoffice.views.wizard_view', name='backoffice.show_wizard'),
    url(r'^(?P<form_type>[-\w]+)/$', 'backoffice.views.form_view', name='backoffice.show_forms'),
)