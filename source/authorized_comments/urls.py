#!/usr/env python
#-*- coding: utf-8 -*-
#
#Copyright 2009 Accepté. All Rights Reserved.
from django.conf.urls.defaults import patterns, url, include
from django.conf import settings

urlpatterns = patterns('authorized_comments.views',

    url(r'^flag/(?P<id>\d+)/$', 'flag', name='comments.flag'),
    url(r'^delete/(?P<id>\d+)/$', 'delete', name='comments.delete'),

)