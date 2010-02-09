#!/usr/env python
#-*- coding: utf-8 -*-
#
#Copyright 2009 Accepte. All Rights Reserved.

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from political_profiles.models import PoliticianProfile
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson

from frontoffice.models import VisitorResult
from opensocial.models import OpenIDMap

from frontoffice.decorators import politicians_only
from django.contrib.auth.decorators import login_required

from django.conf import settings



def map_openid_to_user(request, container, openid):
    """
        Maps container::openid to registered user. Throws 404 if mapping is not found.
    """
    omap = get_object_or_404(OpenIDMap, openid = openid, container = container)
    response = HttpResponse(content_type = 'application/json')
    simplejson.dump({'politician_id': omap.user_id}, response, cls=DjangoJSONEncoder, ensure_ascii=False)
    return response



@login_required
@politicians_only
def register_openid(request, container, openid):
    """
        Register given container::openid to request.user.
        Next time map_openid_to_user() is called with the same container::openid,
        the current request.user ID will be returned.

        Fails if current user has no politician profile.
    """
    ct = OpenIDMap.objects.filter(openid = openid, container = container).count()

    container = container.strip()
    openid = openid.strip()
    if ct == 0 and container != "" and openid != "": # if no such mapping doesn't exist yet
        OpenIDMap.objects.create(user = request.user, openid = openid, container = container)

    # redirect to profile page
    return redirect('fo.politician_profile', id = request.user.id)


@login_required
@politicians_only
def unregister_openid(request, id):
    """
        Removes OpenID mapping.
    """
    OpenIDMap.objects.filter(user = request.user, pk = id).delete()
    return redirect('fo.politician_profile', id = request.user.id)


def get_politician_info(request, politician_id):
    """ Returns politician profile by id """
    user = get_object_or_404(User, pk = politician_id)
    profile = get_object_or_404(PoliticianProfile, user = user)
    response = HttpResponse(content_type = 'application/json')

    domain = u"http://%s" % Site.objects.get_current().domain
    party = profile.election_party()
    data = {
        #[FIXME: scaled version is needed!]
        'name': profile.full_name(),
        'picture': domain + (profile.picture.url if profile.picture else settings.MEDIA_URL + "defaults/pol-dummy_jpg_140x210_upscale_q85.jpg"),
        'age': profile.age(),
        'position': profile.position(),
        'region': profile.region(),
        'party_short': party.party.abbreviation,
        'party_name': party.party.name,
        'profile_url': domain + reverse('fo.politician_profile', kwargs = {'id': politician_id}),
        'become_fan_url': domain + reverse('fo.visitor.add_fan', kwargs = {'politician_id': politician_id}),
    }

    simplejson.dump(data, response, cls=DjangoJSONEncoder, ensure_ascii=False)
    return response



def get_testresult(request, hash):
    """ Returns list of politician candidates ordered by score in a test result"""
    # this is secured by hash only (you are the only one who knows the hash)
    result = get_object_or_404(VisitorResult, hash = hash)
    data = { 'date_time': result.datetime_stamp }
    domain = u"http://%s" % Site.objects.get_current().domain
    
    cand = []
    for an in result.candidate_answers.select_related('candidate__profile').order_by('-candidates_score'):
        profile = an.candidate.profile
        party = profile.election_party().party
        cand.append({
            'id': an.pk,
            'score': an.candidates_score,
            'name': profile.full_name(),
            #[FIXME: scaled version is needed!]
            'picture': domain + (an.candidate.profile.picture.url if an.candidate.profile.picture else settings.MEDIA_URL + "defaults/pol-dummy_jpg_140x210_upscale_q85.jpg"),
            'age': profile.age(),
            'region': profile.region(),
            'position': profile.position(),
            'party_short': party.abbreviation,
            'party_name': party.name,
            'profile_url': domain + reverse('fo.politician_profile', kwargs = {'id': an.candidate.id}),
        })
        
    data.update(candidates = cand)

    response = HttpResponse(content_type = 'application/json')
    simplejson.dump(data, response, cls=DjangoJSONEncoder, ensure_ascii=False)
    return response



