#!/usr/env python
#-*- coding: utf-8 -*-
#
#Copyright 2009 Accepté. All Rights Reserved.
from django.conf.urls.defaults import patterns, url, include


urlpatterns = patterns('opensocial.views',
   url(r'^json/politician/(?P<politician_id>\d+)$', 'get_politician_info', name='opensocial.json.politician.profile'),
   url(r'^json/map/(?P<container>[^/]+)/(?P<openid>[^/]+)$', 'map_openid_to_user', name='opensocial.json.politician.map'),
   url(r'^json/result/(?P<hash>[^/]+)$', 'get_testresult', name='opensocial.json.testresult'),
   url(r'^register/(?P<container>[^/]+)/(?P<openid>[^/]+)$', 'register_openid', name='opensocial.politician.register'),
   url(r'^unregister/(?P<id>\d+)$', 'unregister_openid', name='opensocial.politician.unregister'),
)


