#!/usr/env python
#-*- coding: utf-8 -*-
#
#Copyright 2009 Accepté. All Rights Reserved.
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
   url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'backoffice/login.html'}, name='backoffice.login'),
   url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'backoffice/logged_out.html'}, name='backoffice.logout'),
)


urlpatterns += patterns('backoffice.views',
    url(r'^$', 'election_event',name='backoffice.election_event'),
    url(r'^add/$', 'add_election_instance', name='backoffice.add_election_instance'),
    url(r'^setup/(?P<election_instance_id>\d+)/((?P<user_id>\d+)/)?$', 'election_setup', name='backoffice.election_setup'),
    url(r'^setup/done$', 'election_setup_done', name='backoffice.election_setup_done'),

    url(r'^election_instance/(?P<id>\d+)/$', 'election_instance_view', name='backoffice.election_instance_view'),
    url(r'^election_instance/(?P<id>\d+)/edit/$', 'edit_election_instance', name='backoffice.edit_election_instance'),
    url(r'^election_instance/(?P<id>\d+)/edit_council/$', 'council_edit', name='backoffice.edit_council'),
    url(r'^election_instance/(?P<id>\d+)/add_party/(?P<position>\d+)/$', 'election_party_create', name='backoffice.election_party_create'),
    url(r'^election_instance/(?P<id>\d+)/shrink/$', 'election_instance_shrink', name='backoffice.election_instance_shrink'),
    url(r'^election_instance/(?P<id>\d+)/grow/$', 'election_instance_grow', name='backoffice.election_instance_grow'),

    url(r'^election_party/(?P<id>\d+)/$', 'election_party_view', name='backoffice.election_party_view'),
    url(r'^election_party/(?P<id>\d+)/edit/$', 'election_party_edit', name='backoffice.election_party_edit'),
    url(r'^election_party/(?P<id>\d+)/up/$', 'election_party_up', name='backoffice.election_party_up'),
    url(r'^election_party/(?P<id>\d+)/down/$', 'election_party_down', name='backoffice.election_party_down'),
    url(r'^election_party/(?P<id>\d+)/shrink/$', 'election_party_shrink', name='backoffice.election_party_shrink'),
    url(r'^election_party/(?P<id>\d+)/grow/$', 'election_party_grow', name='backoffice.election_party_grow'),

    url(r'^candidate/(?P<id>\d+)/up/$', 'candidate_up', name='backoffice.candidate_up'),
    url(r'^candidate/(?P<id>\d+)/down/$', 'candidate_down', name='backoffice.candidate_down'),

    url(r'^csv_candidates_1/(?P<ep_id>\d+)/$', 'csv_import_candidates_step1', name='backoffice.csv_candidates_step1'),
    url(r'^csv_candidates_2/(?P<ep_id>\d+)/$', 'csv_import_candidates_step2', {'error': 'false'}, name='backoffice.csv_candidates_step2'),
    url(r'^csv_candidates_2/(?P<ep_id>\d+)/(?P<error>[-\w]+)/$', 'csv_import_candidates_step2', name='backoffice.csv_candidates_step2'),
    url(r'^csv_candidates_3/(?P<ep_id>\d+)/$', 'csv_import_candidates_step3', name='backoffice.csv_candidates_step3'),

    url(r'^csv_parties_1/(?P<ei_id>\d+)/$', 'csv_import_parties_step1', name='backoffice.csv_parties_step1'),
    url(r'^csv_parties_2/(?P<ei_id>\d+)/$', 'csv_import_parties_step2', {'error': 'false'}, name='backoffice.csv_parties_step2'),
    url(r'^csv_parties_2/(?P<ei_id>\d+)/(?P<error>[-\w]+)/$', 'csv_import_parties_step2', name='backoffice.csv_parties_step2'),
    url(r'^csv_parties_3/(?P<ei_id>\d+)/$', 'csv_import_parties_step3', name='backoffice.csv_parties_step3'),

    url(r'^welcome/(?P<election_instance_id>\d+)/$', 'politician_welcome', name='backoffice.politician_welcome'),
    url(r'^welcome/(?P<election_instance_id>\d+)/(?P<user_id>\d+)/$', 'politician_profile_setup', name='backoffice.politician_profile_setup'),
    url(r'^welcome/(?P<election_instance_id>\d+)/(?P<user_id>\d+)/done$', 'politician_profile_setup_done', name='backoffice.politician_profile_setup_done'),

    url(r'^welcome/(?P<election_instance_id>\d+)/(?P<user_id>\d+)/work$', 'politician_profile_work', name='backoffice.politician_profile_work'),
    url(r'^welcome/(?P<election_instance_id>\d+)/(?P<user_id>\d+)/work/add/$', 'politician_profile_work_wizard', name='backoffice.politician_profile_work_wizard'),

    url(r'^welcome/(?P<election_instance_id>\d+)/(?P<user_id>\d+)/political$', 'politician_profile_political', name='backoffice.politician_profile_political'),
    url(r'^welcome/(?P<election_instance_id>\d+)/(?P<user_id>\d+)/political/add/$', 'politician_profile_political_wizard', name='backoffice.politician_profile_political_wizard'),
    url(r'^welcome/(?P<election_instance_id>\d+)/(?P<user_id>\d+)/political/edit/(?P<political_id>\d+)$', 'politician_profile_political_wizard', name='backoffice.politician_profile_political_wizard_edit'),

    url(r'^welcome/(?P<election_instance_id>\d+)/(?P<user_id>\d+)/interest/$', 'politician_profile_interest', name='backoffice.politician_profile_interest'),
    url(r'^welcome/(?P<election_instance_id>\d+)/(?P<user_id>\d+)/interest/add/$', 'politician_profile_interest_wizard', name='backoffice.politician_profile_interest_wizard'),
    url(r'^welcome/(?P<election_instance_id>\d+)/(?P<user_id>\d+)/interest/edit/(?P<interest_id>\d+)$', 'politician_profile_interest_wizard', name='backoffice.politician_profile_interest_wizard_edit'),

    url(r'^welcome/(?P<election_instance_id>\d+)/(?P<user_id>\d+)/appearance/$', 'politician_profile_appearance', name='backoffice.politician_profile_appearance'),
    url(r'^welcome/(?P<election_instance_id>\d+)/(?P<user_id>\d+)/appearance/add/$', 'politician_profile_appearance_wizard', name='backoffice.politician_profile_appearance_wizard'),
    url(r'^welcome/(?P<election_instance_id>\d+)/(?P<user_id>\d+)/appearance/edit/(?P<appearance_id>\d+)$', 'politician_profile_appearance_wizard', name='backoffice.politician_profile_appearance_wizard_edit'),

    url(r'^welcome/(?P<election_instance_id>\d+)/(?P<user_id>\d+)/education/$', 'politician_profile_education', name='backoffice.politician_profile_education'),
    url(r'^welcome/(?P<election_instance_id>\d+)/(?P<user_id>\d+)/education/add/$', 'politician_profile_education_wizard', name='backoffice.politician_profile_education_wizard'),
    url(r'^welcome/(?P<election_instance_id>\d+)/(?P<user_id>\d+)/education/edit/(?P<education_id>\d+)$', 'politician_profile_education_wizard', name='backoffice.politician_profile_education_wizard_edit'),

    url(r'^welcome/(?P<election_instance_id>\d+)/(?P<user_id>\d+)/links/$', 'politician_profile_link', name='backoffice.politician_profile_link'),
    url(r'^welcome/(?P<election_instance_id>\d+)/(?P<user_id>\d+)/links/add/$', 'politician_profile_link_wizard', name='backoffice.politician_profile_link_wizard'),
    url(r'^welcome/(?P<election_instance_id>\d+)/(?P<user_id>\d+)/links/edit/(?P<link_id>\d+)$', 'politician_profile_link_wizard', name='backoffice.politician_profile_link_wizard_edit'),

    url(r'^answer/add-answer-select-question$', 'answer_add_select_question', name='backoffice.answer_add_select_question'),
    url(r'^answer/add-answer-choose-answer/(?P<question_instance_id>\d+)/$', 'answer_add_choose_answer', name='backoffice.answer_add_choose_answer'),
    url(r'^answer/add$', 'answer_add', name='backoffice.answer_add'),
    
    #TODO: Debug views remove at some point 

    url(r'^wizard/(?P<wizard_type>[-\w]+)/$', 'wizard_view', name='backoffice.show_wizard'),
    url(r'^(?P<form_type>[-\w]+)/$', 'form_view', name='backoffice.show_forms'),
    url(r'^question/test-forms$', 'test_question_forms', name='backoffice.test_question_forms'),
    
    )