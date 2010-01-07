#!/usr/env python
#-*- coding: utf-8 -*-
#
#Copyright 2009 Accepté. All Rights Reserved.
from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('',
   url(r'^login/$', 'utils.views.login', {'template_name': 'frontoffice/login.html'}, name='fo.login'),
   url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'frontoffice/logged_out.html'}, name='fo.logout'),
   url(r'^account/', include('frontoffice.registration_backend.urls')),
   
)

urlpatterns += patterns('frontoffice.views',
    url(r'^politician/(?P<id>\d+)/$', 'politician_profile', name='fo.politician_profile'),
    url(r'^politician/(?P<id>\d+)/(?P<tab>\w+)/$', 'politician_profile', name='fo.politician_profile'),
    url(r'^politicians/$', 'politician_profile_filter', name='fo.politician_profile_filter'),
)