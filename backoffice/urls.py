#!/usr/env python
#-*- coding: utf-8 -*-
#
#Copyright 2009 Accepté. All Rights Reserved.
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^$', 'backoffice.views.election_event',name='backoffice.election_event'),
    url(r'^election_instance/(?P<id>\d+)/$', 'backoffice.views.election_instance_view', name='backoffice.election_instance_view'),
    url(r'^election_party/(?P<id>\d+)/$', 'backoffice.views.election_party_view', name='backoffice.election_party_view'),
    url(r'^add_election_instance/$', 'backoffice.views.election_instance_add', name='backoffice.add_election_instance'),
    url(r'^wizard/(?P<wizard_type>[-\w]+)/$', 'backoffice.views.wizard_view', name='backoffice.show_wizard'),
    url(r'^(?P<profile_type>[-\w]+)/$', 'backoffice.views.form_view', name='backoffice.show_forms'),
)