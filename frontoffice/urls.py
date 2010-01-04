#!/usr/env python
#-*- coding: utf-8 -*-
#
#Copyright 2009 Accepté. All Rights Reserved.
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
   url(r'^login/$', 'utils.views.login', {'template_name': 'frontoffice/login.html'}, name='fo.login'),
   url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'frontoffice/logged_out.html'}, name='fo.logout'),
)

urlpatterns += patterns('frontoffice.views',
    
)