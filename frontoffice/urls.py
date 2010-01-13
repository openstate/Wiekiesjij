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
    #politician profile pages
    url(r'^politician/(?P<id>\d+)/$', 'politician_profile', name='fo.politician_profile'),
    url(r'^politician/(?P<id>\d+)/comments/$', 'politician_comments', name='fo.politician_comments'),
    url(r'^politician/(?P<id>\d+)/(?P<tab>\w+)/$', 'politician_profile', name='fo.politician_profile'),

    #politician filter
    url(r'^politicians/$', 'politician_profile_filter', name='fo.politician_profile_filter'),

    #party profile page
    url(r'^party/(?P<eip_id>\d+)/$', 'party_profile', name='fo.party_profile'),

    #politician browser
    url(r'^election/$', 'election', name='fo.election'),
    url(r'^election/(?P<id>\d+)/$', 'election', name='fo.election'),

    # visitor profile page
    url(r'^visitor/become_fan/(?P<politician_id>\d+)/$', 'fan_add', name='fo.visitor.add_fan'),
    url(r'^visitor/leave_fan/(?P<politician_id>\d+)/$', 'fan_remove', name='fo.visitor.remove_fan'),

    #goals
    url(r'^goal/(?P<id>\d+)/$', 'goal', name='fo.goal'),
)