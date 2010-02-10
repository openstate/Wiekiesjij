from itertools import izip

from django.db import connection
from django.shortcuts import render_to_response, redirect
from django.core.cache import cache
from django.template.context import RequestContext
from django.utils.datastructures import SortedDict

from django.db.models import Count, Avg

from elections.models import ElectionInstanceParty, Candidacy
from political_profiles.models import RELIGION, GENDERS, MARITAL_STATUS, EducationLevel


CHART_COLORS = (
    'f8b8aa',
    'aaf8aa',
    'aaaaf8',
    'f8aab8',
    'f8f8aa',
    'aaf8f8',
    'b8aaf8',
    'f8aaaa',
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

def index(request):
    election_instance_id = request.session.get('ElectionInstance', {}).get('id', None)
    if election_instance_id is None:
        return redirect('/')

    cache_key = 'statistics'


    context = None #cache.get(cache_key)
    if context is None:
        context = {}
        context.update({'gender_data': _get_gender_data(election_instance_id)})
        context.update({'smoke_data': _get_smoke_data(election_instance_id)})
        context.update({'diet_data': _get_vegetarian_data(election_instance_id)})
        context.update({'religion_data': _get_religion_data(election_instance_id)})
        context.update({'age_data': _get_age_data(election_instance_id)})
        context.update({'marital_data': _get_maritalstatus_data(election_instance_id)})
        context.update({'education_data': _get_education_data(election_instance_id)})

        #cache.set(cache_key, context)

    eips = ElectionInstanceParty.objects.filter(election_instance__pk=election_instance_id).select_related('party')
    context.update({'eips': eips[0:1]})

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
            chco=','.join(CHART_COLORS),
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
            chco=','.join(CHART_COLORS),
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
            chco=','.join(CHART_COLORS),
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
                chs='300x300',
                chxt='y,x',
                chds='0,%s' % (sum(chart_data)),
                chxl='0:|%s|' % ('|'.join(chart_titles)),
                chbh=20,
                chco=','.join(CHART_COLORS),
                chg='%s,0,1,1' % (100/sum(chart_data)),
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
                chco=','.join(CHART_COLORS),
                chg='0,10,1,0',
            )
            result.update({current_id: query_dict})
            grouped_data = {}

        if row is None:
            break

        grouped_data.update({row['label']: row['count']})
        print grouped_data
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
                chco=','.join(CHART_COLORS),
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
        ORDER BY eip.id, el.level
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
                chco=','.join(CHART_COLORS),
            )
            result.update({current_id: query_dict})
            grouped_data = {}

        if row is None:
            break

        grouped_data.update({row['label']: row['count']})
        current_id = row['id']

    return result


def chart_cache(request):
    """
        Caches images from google charts based on request string
    """
    print request.META
    pass