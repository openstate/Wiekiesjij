#!/usr/env python
#-*- coding: utf-8 -*-
#
#Copyright 2009 Accepté. All Rights Reserved.
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^/$', 'backoffice.views.election_event',name='backoffice.election_event'),
    url(r'^/add_election_instance/$', 'backoffice.views.election_instance_add', name='backoffice.add_election_instance'),
    url(r'^/(?P<profile_type>[-\w]+)/', 'backoffice.views.form_view', name='backoffice.show_forms'),

)