#!/usr/env python
#-*- coding: utf-8 -*-
#
#Copyright 2009 Accepté. All Rights Reserved.
from django.conf.urls.defaults import patterns, url, include
from django.conf import settings

urlpatterns = patterns('',
   url(r'^login/$', 'utils.views.login', {'template_name': 'frontoffice/login.html'}, name='fo.login'),
   url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'frontoffice/logged_out.html'}, name='fo.logout'),
   url(r'^account/', include('frontoffice.registration_backend.urls')),
   
)
#home page
if settings.DEBUG:
    urlpatterns += patterns('frontoffice.view',
        url(r'^$', 'home', name = 'fo.home'),
    )

urlpatterns += patterns('frontoffice.views',
    url(r'^redirect/$', 'redirect_view', name='fo.redirect'),

    

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

    #visitor profile page
    url(r'^visitor/edit_profile/$', 'edit_visitor_profile', name='fo.visitor.edit_profile'),
    url(r'^visitor/become_fan/(?P<politician_id>\d+)/$', 'fan_add', name='fo.visitor.add_fan'),
    url(r'^visitor/leave_fan/(?P<politician_id>\d+)/$', 'fan_remove', name='fo.visitor.remove_fan'),

    #goals
    url(r'^goal/(?P<id>\d+)/$', 'goal', name='fo.goal'),

    #url(r'^test/(?P<id>\d+)/$', 'test', name='fo.test'),
    url(r'^test/(?P<election_instance_party_id>\d+)/$', 'test', name='fo.test'),
    url(r'^goal/(?P<goal_id>\d+)/thumbs_up/$', 'thumbs_up', name='fo.thumbs_up'),
    url(r'^goal/(?P<goal_id>\d+)/thumbs_down/$', 'thumbs_down', name='fo.thumbs_down'),

    #generic profile
    url(r'^dashboard/$', 'dashboard', name='fo.dashboard'),
)