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
    fields = ['id', 'user_id', 'first_name', 'middle_name', 'last_name', 'initials', 'gender', 'dateofbirth']
    data = dict([(f, getattr(profile, f)) for f in fields])
    
    party = profile.election_party()
    data.update({
        #[FIXME: scaled version is needed!]
        'picture': domain + (profile.picture.url if profile.picture else settings.MEDIA_URL + "defaults/pol-dummy_jpg_140x210_upscale_q85.jpg"),
        'age': profile.age(),
        'position': profile.position(),
        'region': profile.region(),
        'party': {
                'abbreviation': party.party.abbreviation,
                'slogan': party.party.slogan,
                'logo': domain + (party.party.logo.url if party.party.logo else settings.MEDIA_URL + "defaults/party-dummy_jpg_120x80_upscale_q85.jpg"),
                'goto_url': domain + reverse('fo.party_profile', kwargs={'eip_id': party.pk}),
        },
        'profile_url': domain + reverse('fo.politician_profile', kwargs = {'id': politician_id}),
        'become_fan_url': domain + reverse('fo.visitor.add_fan', kwargs = {'politician_id': politician_id}),
        'stop_being_fan_url': domain + reverse('fo.visitor.remove_fan', kwargs = {'politician_id': politician_id}),
    })

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
        cand.append({
            'id': an.pk,
            'score': an.candidates_score,
            'name': an.candidate.profile.full_name(),
            #[FIXME: scaled version is needed!]
            'picture': domain + (an.candidate.profile.picture.url if an.candidate.profile.picture else settings.MEDIA_URL + "defaults/pol-dummy_jpg_140x210_upscale_q85.jpg")
        })
        
    data.update(candidates = cand)

    response = HttpResponse(content_type = 'application/json')
    simplejson.dump(data, response, cls=DjangoJSONEncoder, ensure_ascii=False)
    return response



