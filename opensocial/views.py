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
        'do_test_url': None, # [FIXME: to do]
    })

    simplejson.dump(data, response, cls=DjangoJSONEncoder, ensure_ascii=False)
    return response





