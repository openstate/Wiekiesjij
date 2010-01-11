#!/usr/env python
#-*- coding: utf-8 -*-
#
#Copyright 2009 Accepté. All Rights Reserved.
from django.conf.urls.defaults import patterns, url, include


urlpatterns = patterns('opensocial.views',
   url(r'^json/politician/(?P<id>\d+)$', 'get_politician_info', name='opensocial.json.politician.profile'),

   # get result set info
)


