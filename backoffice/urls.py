#!/usr/env python
#-*- coding: utf-8 -*-
#
#Copyright 2009 Accepté. All Rights Reserved.
from django.conf.urls.defaults import *

urlpatterns = patterns('',
   url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'backoffice/login.html'}, name='backoffice.login'),
   url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'backoffice/logged_out.html'}, name='backoffice.logout'),
)

urlpatterns += patterns('backoffice.views',
    url(r'^$', 'election_event',name='backoffice.election_event'),
    url(r'^add/$', 'add_election_instance', name='backoffice.add_election_instance'),
    url(r'^setup/(?P<election_instance_id>\d+)/((?P<user_id>\d+)/)?$', 'election_setup', name='backoffice.election_setup'),
    url(r'^setup/done$', 'election_setup_done', name='backoffice.election_setup_done'),
    
    url(r'^election_instance/(?P<id>\d+)/$', 'election_instance_view', name='backoffice.election_instance_view'),
    url(r'^election_instance/(?P<id>\d+)/edit/$', 'edit_election_instance', name='backoffice.edit_election_instance'),
    url(r'^election_instance/(?P<id>\d+)/edit_council/$', 'council_edit', name='backoffice.edit_council'),
    url(r'^election_instance/(?P<id>\d+)/add_party/(?P<position>\d+)/$', 'election_party_create', name='backoffice.election_party_create'),
    url(r'^election_party/(?P<id>\d+)/$', 'election_party_view', name='backoffice.election_party_view'),
    url(r'^election_party/(?P<id>\d+)/edit/$', 'election_party_edit', name='backoffice.election_party_edit'),
    url(r'^csv_candidates_1/$', 'csv_import_candidates_step1', name='backoffice.csv_candidates_step1'),
    url(r'^csv_candidates_2/$', 'csv_import_candidates_step2', name='backoffice.csv_candidates_step2'),
    
    #TODO: Debug views remove at some point 
    url(r'^wizard/(?P<wizard_type>[-\w]+)/$', 'wizard_view', name='backoffice.show_wizard'),
    url(r'^(?P<form_type>[-\w]+)/$', 'form_view', name='backoffice.show_forms'),
)