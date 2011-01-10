#!/usr/env python
#-*- coding: utf-8 -*-
#
#Copyright 2009 Accepté. All Rights Reserved.
from django.conf.urls.defaults import patterns, url, include
from django.conf import settings
urlpatterns = patterns('elections.views',

    url(r'^council/events/(?P<council_id>\d+)/$', 'events', name='elections.events'),

)
