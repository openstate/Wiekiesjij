#!/usr/env python
#-*- coding: utf-8 -*-
#
#Copyright 2009 Accepté. All Rights Reserved.
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
   url(r'^profile/$', 'backoffice.views.view_profile', name='bo.profile'),
)


urlpatterns += patterns('backoffice.views',

    url(r'^$', 'election_event', name='bo.election_event'),

    url(r'^redirect/$', 'redirect_view', name='bo.redirect'),
    url(r'^permission_denied/$', 'permission_denied', name='bo.permission_denied'),

    url(r'^add/$', 'add_election_instance', name='bo.add_election_instance'),

    #Chancery Wizard
    url(r'^election/(?P<election_instance_id>\d+)/setup/$', 'election_setup', name='bo.election_setup'),
    url(r'^election/(?P<election_instance_id>\d+)/setup/done/$', 'election_setup_done', name='bo.election_setup_done'),
    url(r'^election/(?P<election_instance_id>\d+)/setup/(?P<user_id>\d+)/$', 'election_setup', name='bo.election_setup'),

    #Staff Views
    url(r'^election/(?P<id>\d+)/$', 'election_instance_view', name='bo.election_instance_view'),
    url(r'^election/(?P<id>\d+)/export/$', 'election_instance_export_view', name='bo.election_instance_export_view'),
    url(r'^election/(?P<election_instance_id>\d+)/questions/$', 'question_overview', name='bo.question_overview'),
    url(r'^election/(?P<id>\d+)/edit/$', 'edit_election_instance', name='bo.edit_election_instance'),
    url(r'^election/(?P<id>\d+)/edit-council/$', 'council_edit', name='bo.edit_council'),
    url(r'^election/(?P<id>\d+)/add_party/(?P<position>\d+)/$', 'election_party_create', name='bo.election_party_create'),
    url(r'^election/(?P<id>\d+)/shrink/$', 'election_instance_shrink', name='bo.election_instance_shrink'),
    url(r'^election/(?P<id>\d+)/grow/$', 'election_instance_grow', name='bo.election_instance_grow'),

    #Party Contact Wizard
    url(r'^party/(?P<id>\d+)/setup/(?P<user_id>\d+)/$', 'party_contact_wizard', name='bo.party_contact_wizard'),
    url(r'^party/(?P<id>\d+)/setup/$', 'party_contact_wizard', name='bo.party_contact_wizard'),
    url(r'^party/(?P<id>\d+)/setup/done/$', 'party_contact_wizard_done', name='bo.party_contact_wizard_done'),

    url(r'^party/(?P<id>\d+)/$', 'election_party_view', name='bo.election_party_view'),
    url(r'^party/(?P<id>\d+)/edit/$', 'election_party_edit', name='bo.election_party_edit'),
    url(r'^party/(?P<id>\d+)/up/$', 'election_party_up', name='bo.election_party_up'),
    url(r'^party/(?P<id>\d+)/down/$', 'election_party_down', name='bo.election_party_down'),
    url(r'^party/(?P<id>\d+)/shrink/$', 'election_party_shrink', name='bo.election_party_shrink'),
    url(r'^party/(?P<id>\d+)/grow/$', 'election_party_grow', name='bo.election_party_grow'),
    url(r'^party/(?P<id>\d+)/add_candidate/(?P<pos>\d+)/$', 'election_party_add_candidate', name='bo.election_party_add_candidate'),




    url(r'^candidate/(?P<id>\d+)/edit/$', 'candidate_edit', name='bo.candidate_edit'),
    url(r'^candidate/(?P<id>\d+)/up/$', 'candidate_up', name='bo.candidate_up'),
    url(r'^candidate/(?P<id>\d+)/down/$', 'candidate_down', name='bo.candidate_down'),

    url(r'^add_candidates_1/(?P<ep_id>\d+)/$', 'csv_import_candidates_step1', name='bo.csv_candidates_step1'),
    url(r'^add_candidates_2/(?P<ep_id>\d+)/$', 'csv_import_candidates_step2', {'error': 'false'}, name='bo.csv_candidates_step2'),
    url(r'^add_candidates_2/(?P<ep_id>\d+)/(?P<error>[-\w]+)/$', 'csv_import_candidates_step2', name='bo.csv_candidates_step2'),
    url(r'^add_candidates_3/(?P<ep_id>\d+)/$', 'csv_import_candidates_step3', name='bo.csv_candidates_step3'),

    url(r'^add_parties_1/(?P<ei_id>\d+)/$', 'csv_import_parties_step1', name='bo.csv_parties_step1'),
    url(r'^add_parties_2/(?P<ei_id>\d+)/$', 'csv_import_parties_step2', {'error': 'false'}, name='bo.csv_parties_step2'),
    url(r'^add_parties_2/(?P<ei_id>\d+)/(?P<error>[-\w]+)/$', 'csv_import_parties_step2', name='bo.csv_parties_step2'),
    url(r'^add_parties_3/(?P<ei_id>\d+)/$', 'csv_import_parties_step3', name='bo.csv_parties_step3'),



    url(r'^welcome/(?P<eip_id>\d+)/$', 'politician_welcome', name='bo.politician_welcome'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/$', 'politician_profile_setup', name='bo.politician_profile_setup'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/done$', 'politician_profile_setup_done', name='bo.politician_profile_setup_done'),

    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/goal$', 'politician_profile_goal', name='bo.politician_profile_goal'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/goal/add/$', 'politician_profile_goal_wizard', name='bo.politician_profile_goal_wizard'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/goal/edit/(?P<goal_id>\d+)$', 'politician_profile_goal_wizard', name='bo.politician_profile_goal_wizard_edit'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/goal/delete/(?P<goal_id>\d+)$', 'politician_profile_goal_delete', name='bo.politician_profile_goal_delete'),

    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/work$', 'politician_profile_work', name='bo.politician_profile_work'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/work/add/$', 'politician_profile_work_wizard', name='bo.politician_profile_work_wizard'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/work/edit/(?P<work_id>\d+)$', 'politician_profile_work_wizard', name='bo.politician_profile_work_wizard_edit'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/work/delete/(?P<work_id>\d+)$', 'politician_profile_work_delete', name='bo.politician_profile_work_delete'),

    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/political$', 'politician_profile_political', name='bo.politician_profile_political'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/political/add/$', 'politician_profile_political_wizard', name='bo.politician_profile_political_wizard'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/political/edit/(?P<political_id>\d+)$', 'politician_profile_political_wizard', name='bo.politician_profile_political_wizard_edit'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/political/delete/(?P<political_id>\d+)$', 'politician_profile_political_delete', name='bo.politician_profile_political_delete'),

    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/interest/$', 'politician_profile_interest', name='bo.politician_profile_interest'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/interest/add/$', 'politician_profile_interest_wizard', name='bo.politician_profile_interest_wizard'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/interest/edit/(?P<interest_id>\d+)$', 'politician_profile_interest_wizard', name='bo.politician_profile_interest_wizard_edit'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/interest/delete/(?P<interest_id>\d+)$', 'politician_profile_interest_delete', name='bo.politician_profile_interest_delete'),

    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/appearance/$', 'politician_profile_appearance', name='bo.politician_profile_appearance'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/appearance/add/$', 'politician_profile_appearance_wizard', name='bo.politician_profile_appearance_wizard'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/appearance/delete/(?P<appearance_id>\d+)$', 'politician_profile_appearance_delete', name='bo.politician_profile_appearance_delete'),
    #url(r'^welcome/appearance/(?P<path>[a-z0-9:]*)$','politician_profile_appearance_wizard', {'path':''}, name='bo.politician_profile_appearance_wizard'),
    #url(r'^welcome/appearance/(?P<action>init)/(?P<eip_id>\d+)/((?P<user_id>\d+)/)?$', 'politician_profile_appearance_wizard', {'path':''}, name='bo.politician_profile_appearance_wizard.init'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/appearance/edit/(?P<appearance_id>\d+)$', 'politician_profile_appearance_wizard', name='bo.politician_profile_appearance_wizard_edit'),

    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/education/$', 'politician_profile_education', name='bo.politician_profile_education'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/education/add/$', 'politician_profile_education_wizard', name='bo.politician_profile_education_wizard'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/education/edit/(?P<education_id>\d+)$', 'politician_profile_education_wizard', name='bo.politician_profile_education_wizard_edit'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/education/delete/(?P<education_id>\d+)$', 'politician_profile_education_delete', name='bo.politician_profile_education_delete'),

    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/links/$', 'politician_profile_link', name='bo.politician_profile_link'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/links/add/$', 'politician_profile_link_wizard', name='bo.politician_profile_link_wizard'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/links/edit/(?P<link_id>\d+)$', 'politician_profile_link_wizard', name='bo.politician_profile_link_wizard_edit'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/links/delete/(?P<link_id>\d+)$', 'politician_profile_link_delete', name='bo.politician_profile_link_delete'),

    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/connections/$', 'politician_profile_connection', name='bo.politician_profile_connection'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/connections/add/$', 'politician_profile_connection_wizard', name='bo.politician_profile_connection_wizard'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/connections/edit/(?P<connection_id>\d+)$', 'politician_profile_connection_wizard', name='bo.politician_profile_connection_wizard_edit'),
    url(r'^welcome/(?P<eip_id>\d+)/(?P<user_id>\d+)/connections/delete/(?P<connection_id>\d+)$', 'politician_profile_connection_delete', name='bo.politician_profile_connection_delete'),

    url(r'^welcome/answer-question/(?P<election_instance_party_id>\d+)/(?P<user_id>\d+)/$', 'answer_question', name='bo.answer_question'),
    url(r'^welcome/answer-question/(?P<election_instance_party_id>\d+)/(?P<user_id>\d+)/done/$', 'answer_question_done', name='bo.answer_question_done'),
    )
