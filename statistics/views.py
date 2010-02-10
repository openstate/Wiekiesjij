from itertools import izip
import os
import urllib
import hashlib
import stat
import mimetypes

from django.views.static import was_modified_since
from django.utils.http import http_date
from django.http import HttpResponseNotModified, HttpResponse
from django.db import connection
from django.conf import settings
from django.shortcuts import render_to_response, redirect
from django.core.cache import cache
from django.template.context import RequestContext
from django.utils.datastructures import SortedDict

from django.db.models import Count, Avg

from elections.models import ElectionInstanceParty, Candidacy
from political_profiles.models import RELIGION, GENDERS, MARITAL_STATUS, EducationLevel


CHART_COLORS = (
    'ED2227',
    'BDE717',
    '1D9DCE',
    'EFC620',
    '2D1DCE',
    '00ffff',
    '9900ff',
    'ff0000',
    'b866aa',
    'aab8aa',
    'aaaab8',
    'b8aa66',
    'f8e866',
    '66f866',
    '6666f8',
    'f866e8',
    'b8b8aa',
    'aab8b8',
    '66aab8',
    'b8aaaa',
    'f8f866',
    '66f8f8',
    'e866f8',
    'f86666',
)


def _query_to_dict(query_str, *query_args):
    cursor = connection.cursor()
    cursor.execute(query_str, query_args)
    col_names = [desc[0] for desc in cursor.description]
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        row_dict = dict(izip(col_names, row))
        yield row_dict
    return

def index(request, tab):
    election_instance_id = request.session.get('ElectionInstance', {}).get('id', None)
    if election_instance_id is None:
        return redirect('/')

    cache_key = 'statistics-%s' % (election_instance_id)


    context = cache.get(cache_key)
    if context is None:
        context = {}
        context.update({'gender_data': _get_gender_data(election_instance_id)})
        context.update({'smoke_data': _get_smoke_data(election_instance_id)})
        context.update({'diet_data': _get_vegetarian_data(election_instance_id)})
        context.update({'religion_data': _get_religion_data(election_instance_id)})
        context.update({'age_data': _get_age_data(election_instance_id)})
        context.update({'marital_data': _get_maritalstatus_data(election_instance_id)})
        context.update({'education_data': _get_education_data(election_instance_id)})

        cache.set(cache_key, context)

    eips = ElectionInstanceParty.objects.filter(election_instance__pk=election_instance_id).select_related('party')
    context.update({'eips': eips})
    context.update({'tab': tab})

    return render_to_response('statistics/index.html', context, context_instance=RequestContext(request))

def _get_gender_data(election_instance_id):
    query = """
        SELECT eip.id, SUM(CASE p.gender WHEN 'Male' THEN 1 ELSE 0 END) AS male_count, SUM(CASE p.gender WHEN 'Female' THEN 1 ELSE 0 END) AS female_count
        FROM elections_electioninstanceparty eip
        INNER JOIN elections_candidacy ec ON eip.id = ec.election_party_instance_id
        INNER JOIN political_profiles_politicianprofile p ON p.user_id = ec.candidate_id
        WHERE eip.election_instance_id = %s
        GROUP BY eip.id
    """
    result = {}
    for row in _query_to_dict(query, election_instance_id):
        query_dict = dict(
            cht='p3',
            chd='t:%s,%s' % (row['male_count'], row['female_count']),
            chs='280x100',
            chdl='Mannen+(%s)|Vrouwen+(%s)' % (row['male_count'], row['female_count']),
            chco=','.join(CHART_COLORS[0:2]),
        )
        result.update({row['id']: query_dict})
    return result

def _get_smoke_data(election_instance_id):
    query = """
        SELECT eip.id, SUM(CASE p.smoker WHEN 1 THEN 1 ELSE 0 END) AS smoker_count, SUM(CASE p.smoker WHEN 0 THEN 1 ELSE 0 END) AS nonsmoker_count
        FROM elections_electioninstanceparty eip
        INNER JOIN elections_candidacy ec ON eip.id = ec.election_party_instance_id
        INNER JOIN political_profiles_politicianprofile p ON p.user_id = ec.candidate_id
        WHERE eip.election_instance_id = %s
        GROUP BY eip.id
    """
    result = {}
    for row in _query_to_dict(query, election_instance_id):
        query_dict = dict(
            cht='p3',
            chd='t:%s,%s' % (row['smoker_count'], row['nonsmoker_count']),
            chs='280x100',
            chdl='Roken+(%s)|Niet+Roken+(%s)' % (row['smoker_count'], row['nonsmoker_count']),
            chco=','.join(CHART_COLORS[0:2]),
        )
        result.update({row['id']: query_dict})
    return result

def _get_vegetarian_data(election_instance_id):
    query = """
        SELECT eip.id, SUM(CASE p.diet WHEN 'NEE' THEN 1 ELSE 0 END) AS nonveggie_count, SUM(CASE p.diet WHEN 'YES' THEN 1 ELSE 0 END) AS veggie_count
        FROM elections_electioninstanceparty eip
        INNER JOIN elections_candidacy ec ON eip.id = ec.election_party_instance_id
        INNER JOIN political_profiles_politicianprofile p ON p.user_id = ec.candidate_id
        WHERE eip.election_instance_id = %s
        GROUP BY eip.id
    """

    result = {}
    for row in _query_to_dict(query, election_instance_id):
        query_dict = dict(
            cht='p3',
            chd='t:%s,%s' % (row['nonveggie_count'], row['veggie_count']),
            chs='280x100',
            chdl='Niet+vegetarisch+(%s)|Vegetarisch+(%s)' % (row['nonveggie_count'], row['veggie_count']),
            chco=','.join(CHART_COLORS[0:2]),
        )
        result.update({row['id']: query_dict})
    return result

def _get_religion_data(election_instance_id):
    query = """
        SELECT eip.id, p.religion as label, COUNT(*) as count
        FROM elections_electioninstanceparty eip
        INNER JOIN elections_candidacy ec ON eip.id = ec.election_party_instance_id
        INNER JOIN political_profiles_politicianprofile p ON p.user_id = ec.candidate_id
        WHERE eip.election_instance_id = %s
        GROUP BY eip.id, p.religion
        ORDER BY eip.id, p.religion
    """

    result = {}
    grouped_data = {}
    current_id = None
    generator = _query_to_dict(query, election_instance_id)
    while True:
        try:
            row = generator.next()
        except StopIteration:
            row = None

        if row is None or (row['id'] != current_id and current_id is not None):
            chart_data = []
            chart_titles = []
            for (key, title) in RELIGION:
                chart_titles.append("%s" % (title))
                chart_data.append(grouped_data.get(key, 0))

            query_dict = dict(
                cht='bhs',
                chd='t:%s' % (','.join(map(str, reversed(chart_data)))),
                chs='400x280',
                chxt='y,x',
                chds='0,%s' % (sum(chart_data)),
                chxl='0:|%s' % ('|'.join(chart_titles)),
                chbh=20,
                chco=','.join(CHART_COLORS[0:len(chart_data)]),
                chg='10,0,1,1',
            )
            result.update({current_id: query_dict})
            grouped_data = {}

        if row is None:
            break

        grouped_data.update({row['label']: row['count']})
        current_id = row['id']

    return result


def _get_age_data(election_instance_id):
    query = """
        SELECT eip.id, p.age - (p.age %% 10) as label, COUNT(p.age - (p.age %% 10)) AS count
        FROM elections_electioninstanceparty eip
        INNER JOIN elections_candidacy ec ON eip.id = ec.election_party_instance_id
        INNER JOIN political_profiles_politicianprofile p ON p.user_id = ec.candidate_id
        WHERE p.age IS NOT NULL AND eip.election_instance_id = %s
        GROUP BY eip.id, (p.age - (p.age %% 10))
        ORDER BY eip.id, p.age - (p.age %% 10)
    """

    result = {}
    grouped_data = {}
    current_id = None
    generator = _query_to_dict(query, election_instance_id)
    while True:
        try:
            row = generator.next()
        except StopIteration:
            row = None

        if row is None or (row['id'] != current_id and current_id is not None):
            chart_data = []
            chart_titles = []
            for (key, title) in [(x, "%s-%s" % (x, x+9)) for x in range(10, 100, 10)]:
                chart_titles.append(title)
                chart_data.append(grouped_data.get(key, 0))

            chart_titles[0] = '<19'
            chart_titles[-1] = '90>'
            query_dict = dict(
                cht='bvs',
                chd='t:%s' % (','.join(map(str,chart_data))),
                chs='350x250',
                chxt='x,y',
                chxr='1,0,100' ,
                chds='0,%s' % (sum(chart_data)),
                chxl='0:|%s|' % ('|'.join(chart_titles)),
                chbh=30,
                chco=','.join(CHART_COLORS[0:len(chart_data)]),
                chg='0,10,1,0',
            )
            result.update({current_id: query_dict})
            grouped_data = {}

        if row is None:
            break

        grouped_data.update({row['label']: row['count']})
        current_id = row['id']

    return result

def _get_maritalstatus_data(election_instance_id):
    query = """
        SELECT eip.id, p.marital_status AS label, COUNT(*) AS count
        FROM elections_electioninstanceparty eip
        INNER JOIN elections_candidacy ec ON eip.id = ec.election_party_instance_id
        INNER JOIN political_profiles_politicianprofile p ON p.user_id = ec.candidate_id
        WHERE eip.election_instance_id = %s
        GROUP BY eip.id, p.marital_status
        ORDER BY eip.id, p.marital_status
    """

    result = {}
    grouped_data = {}
    current_id = None
    generator = _query_to_dict(query, election_instance_id)
    while True:
        try:
            row = generator.next()
        except StopIteration:
            row = None

        if row is None or (row['id'] != current_id and current_id is not None):
            chart_data = []
            chart_titles = []
            for (key, title) in MARITAL_STATUS:
                chart_titles.append("%s (%s)" % (title, grouped_data.get(key, 0)))
                chart_data.append(grouped_data.get(key, 0))

            query_dict = dict(
                cht='p3',
                chd='t:%s' % (','.join(map(str,chart_data))),
                chs='280x100',
                chdl='%s' % ('|'.join(chart_titles)),
                chco=','.join(CHART_COLORS[0:len(chart_data)]),
            )
            result.update({current_id: query_dict})
            grouped_data = {}

        if row is None:
            break

        grouped_data.update({row['label']: row['count']})
        current_id = row['id']

    return result

def _get_education_data(election_instance_id):
    query = """
        SELECT eip.id, el.level AS label, COUNT(*) AS count
        FROM elections_electioninstanceparty eip
        INNER JOIN elections_candidacy ec ON eip.id = ec.election_party_instance_id
        INNER JOIN political_profiles_politicianprofile p ON p.user_id = ec.candidate_id
        INNER JOIN political_profiles_education ppe ON ppe.politician_id = p.id
        INNER JOIN political_profiles_educationlevel el ON el.id = ppe.level_id
        WHERE eip.election_instance_id = %s
        GROUP BY eip.id, el.level
        ORDER BY eip.id, el.id
    """
    
    education_levels = EducationLevel.objects.order_by('level').values_list('level', flat=True)

    result = {}
    grouped_data = {}
    current_id = None
    generator = _query_to_dict(query, election_instance_id)
    while True:
        try:
            row = generator.next()
        except StopIteration:
            row = None

        if row is None or (row['id'] != current_id and current_id is not None):
            chart_data = []
            chart_titles = []
            for title in education_levels:
                key = title
                chart_titles.append("%s (%s)" % (title, grouped_data.get(key, 0)))
                chart_data.append(grouped_data.get(key, 0))

            query_dict = dict(
                cht='p3',
                chd='t:%s' % (','.join(map(str,chart_data))),
                chs='280x120',
                chdl='%s' % ('|'.join(chart_titles)),
                chco=','.join(CHART_COLORS[0:len(chart_data)]),
            )
            result.update({current_id: query_dict})
            grouped_data = {}

        if row is None:
            break

        grouped_data.update({row['label']: row['count']})
        current_id = row['id']

    return result

def _get_chart_to_serve(request):
    """
        Caches images from google charts based on request string
    """
    default_image = '%s/defaults/party-dummy.jpg' % (settings.MEDIA_ROOT)  #TODO; change default
    
    qs = request.META.get('QUERY_STRING', '')
    if qs == '':
        return default_image
        
    imagekey = hashlib.sha224(qs).hexdigest()
    
    path = '%s/statistics/%s.png' % (settings.MEDIA_ROOT, imagekey)
    if not os.path.isfile(path):
        """
            Get the image from google
        """
        google_url = "http://chart.apis.google.com/chart?%s" % (qs)
        try:
            urllib.urlretrieve(google_url, path)
        except:
            return default_image
        
        
    return '%s/statistics/%s.png' % (settings.MEDIA_ROOT, imagekey)

def chart_cache(request):
    fullpath = _get_chart_to_serve(request)
    
    statobj = os.stat(fullpath)
    if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                              statobj[stat.ST_MTIME], statobj[stat.ST_SIZE]):
        return HttpResponseNotModified()
    mimetype = mimetypes.guess_type(fullpath)[0] or 'application/octet-stream'
    contents = open(fullpath, 'rb').read()
    response = HttpResponse(contents, mimetype=mimetype)
    response["Last-Modified"] = http_date(statobj[stat.ST_MTIME])
    response["Content-Length"] = len(contents)
    return response