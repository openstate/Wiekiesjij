#!/usr/env python
#-*- coding: utf-8 -*-
#
#Copyright 2009 Accepté. All Rights Reserved.
from django.conf.urls.defaults import *
from backoffice.wizards import AddElectionInstanceWizard

urlpatterns = patterns('',
    url(r'^$', 'backoffice.views.election_event',name='backoffice.election_event'),
    url(r'^add/$', AddElectionInstanceWizard(), name='backoffice.add_election_instance'),
    url(r'^setup/(?P<done>[-\w]+/)?$', 'backoffice.views.election_setup', name='backoffice.election_setup'),
    url(r'^election_instance/(?P<id>\d+)/$', 'backoffice.views.election_instance_view', name='backoffice.election_instance_view'),
    url(r'^election_party/(?P<id>\d+)/$', 'backoffice.views.election_party_view', name='backoffice.election_party_view'),
    url(r'^wizard/(?P<wizard_type>[-\w]+)/$', 'backoffice.views.wizard_view', name='backoffice.show_wizard'),
    url(r'^(?P<profile_type>[-\w]+)/$', 'backoffice.views.form_view', name='backoffice.show_forms'),
)