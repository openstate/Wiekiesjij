#!/usr/env python
#-*- coding: utf-8 -*-
#
#Copyright 2009 Accepte. All Rights Reserved.

import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from political_profiles.models import PoliticianProfile
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson

from frontoffice.models import VisitorResult, CandidateAnswers


# Bernard, the idea is:
#   Gadget is either configured to a politician(1) or to a test result view(2).
#
# 1) Politician adds gadget to his/her profile page
#    Gadget makes request to map_openid_to_politician(openid) and gets either no_map_error
#    or politician ID.
#
#    If no_map_error, then gadget shows the link to register_openid(). User clicks and
#    page opens (normal page, not in the gadget) where the user has to confirm the mapping.
#    Next time the user opens the gadget, the map_openid_to_politician() should not fail.
#
#    Once map_openid_to_politician() succeeds, the obtained ID is stored in gadget settings.
#    Subsequent views will use the ID from the settings.
#    The ID is used in get_politician_info() to obtain the politician info.
#
# 2) User makes the test and obtains the hash.
#    User adds gadget to his/her profile page.
#    User specifies the hash to the gadget, the gadget stores it in settings.
#    The gadget makes request to get_testrestult_politicians(hash) to obtain test candidates.
#    The candidates are presented in gadget view to the user.
#    The user selects candidate, its ID is stored in the settings.
#    Subsequent views will use that ID in get_test_result(cnadidate ID) to obtain
#    the politician profile info and the score.
#
# At any time the user can reconfigure the gadget to politician profile view or to a test
# result view. In test result view the hash is stored, such that later the user is able to
# choose another candidate if he/she wants to (loosing hash means loosing test result forever).


def map_openid_to_politician(request, openid):
    """Returns User.id of politician mapped to openid. Fails if no mapping is found. Answers with JSON"""
    pass


def register_openid(request, openid):
    """Register given openid to request.user. Next time map_openid_to_politician() is called with
       the same openid, the request.user ID will be returned.
       Fails if current user has no politician profile.
    """
    pass


def get_politician_info(request, id):
    """ Returns politician profile by id """
    user = get_object_or_404(User, pk = id)
    profile = get_object_or_404(PoliticianProfile, user = user)
    response = HttpResponse(content_type = 'application/json')

    domain = u"http://%s" % Site.objects.get_current().domain
    fields = ['id', 'user_id', 'first_name', 'middle_name', 'last_name', 'initials', 'gender', 'dateofbirth']
    data = dict([(f, getattr(profile, f)) for f in fields])

    party = profile.election_party()
    data.update({
        'picture': domain + profile.picture.url,
        'age': profile.age(),
        'position': profile.position(),
        'region': profile.region(),
        'party': {
                'abbreviation': party.party.abbreviation,
                'slogan': party.party.slogan,
                'logo': domain + party.party.logo.url,
                'goto_url': domain + reverse('fo.party_profile', kwargs={'eip_id': party.pk}),
        },
        'profile_url': domain + reverse('fo.politician_profile', kwargs = {'id': id}),
        'become_fan_url': domain + reverse('fo.visitor.add_fan', kwargs = {'politician_id': id}),
        'stop_being_fan_url': domain + reverse('fo.visitor.remove_fan', kwargs = {'politician_id': id}),
        'is_fan': (request.user.profile is not None and 'visitor' == request.user.profile.type and request.user.profile in profile.fans.all()),
        # 'do_test_url': domain + reverse('fo.match_welcome', kwargs={'election_instance_id': TODO}),
    })

    simplejson.dump(data, response, cls=DjangoJSONEncoder, ensure_ascii=False)
    return response



def get_testresult_politicians(request, hash):
    """ Returns list of politician candidates ordered by score in a test reesult"""
    # this is secured by hash only (you are the only one who knows the hash)
    result = get_object_or_404(VisitorResult, hash = hash)
    data = { 'date_time': result.datetime_stamp }
    
    cand = []
    for an in result.candidate_answers.select_related('candidate__profile').order('-candidates_score'):
        cand.extend({
            'id': an.pk,
            'score': an.candidates_score,
            'name': an.candidate.profile.full_name(),
            'picture': an.candidate.profile.picture()
        })
        
    data.update(candidates = cand)

    response = HttpResponse(content_type = 'application/json')
    simplejson.dump(data, response, cls=DjangoJSONEncoder, ensure_ascii=False)
    return response


def get_testresult(request, candidate_answer):
    """Returns test info of specific candidate answer"""
    pass



