
import re
import hashlib
import datetime
import json
import urlparse
import urllib

from django.conf import settings
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import Http404

from frontoffice.forms import PoliticianFilterForm, VisitorProfileForm, RegionSelectForm, SmsForm
from frontoffice.models import VisitorResult
from questions.models import Question, Answer
from questions import settings as qsettings
from elections.models import Party, Candidacy, ElectionInstance, ElectionInstanceParty
from political_profiles.models import Education, PoliticianProfile, PoliticalGoal, GoalRanking, VisitorProfile, WorkExperienceSector, EducationLevel
from political_profiles.models import RELIGION, DIET, MARITAL_STATUS, GENDERS, PARTIES
from frontoffice.decorators import visitors_only
from django.contrib.auth.decorators import login_required



from frontoffice.wizards.match import BestCandidate

def redirect_view(request):
    if not request.user.is_authenticated():
        return redirect('fo.home')
    elif not request.user.profile and request.user.is_staff:
        return redirect('bo.redirect')
    elif request.user.profile.type == 'visitor':
        return redirect('fo.home')
    else:
        return redirect('bo.redirect')



#Helper function
def _new_url(path, field, value):

    bits = urlparse.urlsplit(path)
    data = urlparse.parse_qsl(bits[3])
    data2 = []
    for (key, value) in data:
        if key == field:
            data2.append((key, ''))
        else:
            data2.append((key, value))
    result = []
    for x in bits:
        result.append(x)
    result[3] = urllib.urlencode(data2)
    return urlparse.urlunsplit(result)

def match_results(request, hash, iframe=None):
    result = get_object_or_404(VisitorResult,hash=hash)

    request.session['ElectionInstance'] = dict(id=result.election_instance.id, name=result.election_instance.name)

    candidates = result.candidate_answers.all()
    if request.user.is_authenticated() and request.user.profile and request.user.profile.type == 'visitor':
        visitors_profile = request.user.profile
    else:
        visitors_profile = False
    questions =  json.loads(result.visitor_answers)
    questions = range(0,len(questions))

    if iframe:
        parent = 'frontoffice/iframe.html'
    else:
        parent = 'frontoffice/base.html'

    returndict = {'hash':hash, 'questions':questions, 'candidates': candidates, 'parent':parent, 'iframe': iframe, 'election_instance': result.election_instance}

    if request.user.is_authenticated():
        if result.user == request.user:
            returndict['show_message'] = True


    if result.telephone:
        return render_to_response('frontoffice/match_results.html', returndict, context_instance=RequestContext(request))

    if visitors_profile:
        initial = {'phone':visitors_profile.phone}

    else:
        initial = {'phone':result.telephone}

    #check for sms module
    if result.election_instance.modules.filter(slug='SMS').count() != 0:
        if request.method == 'POST':
            form = SmsForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['phone']:
                    result.telephone = form.cleaned_data['phone']
                    result.save()
                returndict['show_message'] = True
                return render_to_response('frontoffice/match_results.html', returndict, context_instance=RequestContext(request))

        else:

            form = SmsForm(initial=initial)


        returndict['form'] = form

    return render_to_response('frontoffice/match_results.html', returndict, context_instance=RequestContext(request))

def match_welcome(request, election_instance_id = None, iframe = None):
    if not election_instance_id:
        return redirect('fo.home')
    election_instance = get_object_or_404(ElectionInstance, pk=election_instance_id)

    if iframe:
        parent = 'frontoffice/iframe.html'
    else:
        parent = 'frontoffice/base.html'
    return render_to_response('frontoffice/match_welcome.html', {'election_instance': election_instance, 'parent': parent, 'iframe':iframe}, context_instance=RequestContext(request))


def match(request, election_instance_id = None, iframe=None):
    if not election_instance_id:
        return redirect('fo.home')
    return BestCandidate(election_instance_id=election_instance_id, iframe=iframe)(request)


def election(request, id=None):

    politicians = []
    if 'ElectionInstance' in request.session and id is None:
        election_instances = ElectionInstance.objects.filter(election_event = settings.ELECTIONS_ELECTION_EVENT_ID, id=request.session['ElectionInstance']['id'])
    elif id is not None:
        election_instances = ElectionInstance.objects.filter(election_event = settings.ELECTIONS_ELECTION_EVENT_ID, election_instance_parties__id=id)
    elif 'ElectionInstance' not in request.session and id is None:
        return redirect('fo.home')
    else:
        election_instances = ElectionInstance.objects.filter(election_event = settings.ELECTIONS_ELECTION_EVENT_ID)
    election_instances = ElectionInstance.objects.filter(election_event = settings.ELECTIONS_ELECTION_EVENT_ID)
    selected_eip = None
    eips = ElectionInstanceParty.objects.filter(election_instance__in=election_instances).order_by('position')
    if id:
        selected_eip = get_object_or_404(ElectionInstanceParty, pk=id)
        politicians = selected_eip.candidate_dict()
    elif eips:
        selected_eip = eips[0]
        politicians = selected_eip.candidate_dict()

    if len(election_instances) <= 1:
        return render_to_response('frontoffice/election.html', {'selected_eip':selected_eip, 'eips':eips, 'politicians':politicians, 'instance': election_instances[0]}, context_instance=RequestContext(request))
    else:
        return render_to_response('frontoffice/election.html', {'selected_eip':selected_eip, 'eips':eips, 'politicians':politicians}, context_instance=RequestContext(request))


def goal(request, id):
    goal = get_object_or_404(PoliticalGoal, pk=id)
    return render_to_response('frontoffice/goal.html', {'goal': goal, 'profile':  goal.politician}, context_instance=RequestContext(request))



def politician_profile_filter(request):
    politicians = []
    party_data = {}
    gender = dict(GENDERS)
    religion = dict(RELIGION)
    marital_status = dict(MARITAL_STATUS)
    diet = dict(DIET)


    if request.method == 'GET':
        form = PoliticianFilterForm(request.GET) # A form bound to the GET data
        election_instances = ElectionInstance.objects.filter(election_event = settings.ELECTIONS_ELECTION_EVENT_ID)
        eips = ElectionInstanceParty.objects.filter(election_instance__in=election_instances)
        elections_candidates = Candidacy.objects.filter(election_party_instance__in=eips)

        candidates = User.objects.filter(elections__in=elections_candidates)
        politicians = PoliticianProfile.objects.filter(user__in=candidates).order_by('?')
        filtered_politicians = politicians
        path = request.get_full_path()
        region_filtered = False
        filters = []

        if not request.GET and 'ElectionInstance' in request.session:
            return redirect("%s?region=%d" % (path, request.session['ElectionInstance']['id']))

        if form.is_valid():
            # All validation rules pass
            # Process the data in form.cleaned_data
            # ...

            if form.cleaned_data['region'] != '---------' and form.cleaned_data['region']:
                election_instances = ElectionInstance.objects.filter(election_event = settings.ELECTIONS_ELECTION_EVENT_ID, id=form.cleaned_data['region'].id)
                eips = ElectionInstanceParty.objects.filter(election_instance__in=election_instances)
                elections_candidates = Candidacy.objects.filter(election_party_instance__in=eips)
                candidates = User.objects.filter(elections__in=elections_candidates)
                politicians = PoliticianProfile.objects.filter(user__in=candidates).order_by('?')
                filtered_politicians = politicians

                new_path = _new_url(path, 'region', form.cleaned_data['region'].id)
                region_filtered = form.cleaned_data['region'].name

                filters.append((_('Region'), form.cleaned_data['region'].name, new_path))

                sess = {'id': form.cleaned_data['region'].id, 'name': form.cleaned_data['region'].name}
                request.session['ElectionInstance'] = sess

            if form.cleaned_data['name']:
                name_filter = None
                for name in form.cleaned_data['name'].split():
                    if name_filter is None:
                        name_filter = (Q(last_name__icontains=name) | Q(first_name__icontains=name) | Q(middle_name__icontains=name))
                    else:
                        name_filter = name_filter &  (Q(last_name__icontains=name) | Q(first_name__icontains=name) | Q(middle_name__icontains=name))
                filtered_politicians = filtered_politicians.filter(name_filter)
                new_path = _new_url(path, 'name', form.cleaned_data['name'])
                filters.append((_('Name'), form.cleaned_data['name'], new_path))

            if form.cleaned_data['gender'] != 'All' and form.cleaned_data['gender']:
                filtered_politicians = filtered_politicians.filter(gender=form.cleaned_data['gender'])
                new_path = _new_url(path, 'gender', form.cleaned_data['gender'])
                filters.append((_('Gender'), gender[form.cleaned_data['gender']], new_path))

            if form.cleaned_data['children']  != '---------' and form.cleaned_data['children']:
                if form.cleaned_data['children'] == '1':
                    filtered_politicians = filtered_politicians.filter(num_children__gte=1)
                    new_path = _new_url(path, 'children', form.cleaned_data['children'])
                    filters.append((_('Children'), _('Yes'), new_path))
                else:
                    filtered_politicians = filtered_politicians.filter(num_children=0)
                    new_path = _new_url(path, 'children', form.cleaned_data['children'])
                    filters.append((_('Children'), _('No'), new_path))



            """ Calculate date from age - uses rough estimate of how 36 years
            ago - its rough because of leapyears - to compensate will add two
            weeks to either side of age so more candidates will sho even if
            they are a bit older or a bit younger"""

            todate = datetime.date.today()
            if form.cleaned_data['start_age'] is not None:

                date = datetime.date(todate.year - (form.cleaned_data['start_age']), todate.month, todate.day)

                filtered_politicians = filtered_politicians.filter(dateofbirth__lt=date)
                new_path = _new_url(path, 'start_age', form.cleaned_data['start_age'])
                filters.append((_('Youngest'), form.cleaned_data['start_age'], new_path))

            if form.cleaned_data['end_age'] is not None:
                date = datetime.date(todate.year - (form.cleaned_data['end_age'] + 1), todate.month, todate.day)

                filtered_politicians = filtered_politicians.filter(dateofbirth__gte=date)

                new_path = _new_url(path, 'end_age', form.cleaned_data['end_age'])
                filters.append((_('Oldest'), form.cleaned_data['end_age'], new_path))

            if form.cleaned_data['education'] != '---------' and form.cleaned_data['education']:
                filtered_politicians = filtered_politicians.filter(education__level=form.cleaned_data['education'])
                new_path = _new_url(path, 'education', form.cleaned_data['education'].id)

                filters.append((_('Education'), form.cleaned_data['education'], new_path))

            if form.cleaned_data['political_exp_years']:
                filtered_politicians = filtered_politicians.filter(political_experience_days__gte=(form.cleaned_data['political_exp_years'] * 365))
                new_path = _new_url(path, 'political_exp_years', form.cleaned_data['political_exp_years'])
                filters.append((_('Years political experience'), form.cleaned_data['political_exp_years'], new_path))

            if form.cleaned_data['work_exp_years']:
                filtered_politicians = filtered_politicians.filter(work_experience_days__gte=(form.cleaned_data['work_exp_years'] * 365))
                new_path = _new_url(path, 'work_exp_years', form.cleaned_data['work_exp_years'])
                filters.append((_('Years work experience'), form.cleaned_data['work_exp_years'], new_path))

            if form.cleaned_data['religion'] != '---------' and form.cleaned_data['religion']:
                filtered_politicians = filtered_politicians.filter(religion=form.cleaned_data['religion'])
                new_path = _new_url(path, 'religion', form.cleaned_data['religion'])
                filters.append((_('Religion'), religion[form.cleaned_data['religion']], new_path))

            if form.cleaned_data['marital_status'] != '---------' and form.cleaned_data['marital_status']:
                filtered_politicians = filtered_politicians.filter(marital_status=form.cleaned_data['marital_status'])
                new_path = _new_url(path, 'marital_status', form.cleaned_data['marital_status'])
                filters.append((_('Marital status'), marital_status[form.cleaned_data['marital_status']], new_path))

            if form.cleaned_data['goals'] != '---------' and form.cleaned_data['goals']:
                filtered_politicians = filtered_politicians.filter(goals__goal__icontains=form.cleaned_data['goals'])
                new_path = _new_url(path, 'goals', form.cleaned_data['goals'])
                filters.append((_('Goals'), form.cleaned_data['goals'], new_path))

            if form.cleaned_data['smoker'] != '---------' and form.cleaned_data['smoker']:
                if form.cleaned_data['smoker'] == '1':
                    filtered_politicians = filtered_politicians.filter(smoker='YES')
                    new_path = _new_url(path, 'smoker', form.cleaned_data['smoker'])
                    filters.append((_('Smoker'), _('Yes'), new_path))
                else:
                    filtered_politicians = filtered_politicians.filter(smoker='NO')
                    new_path = _new_url(path, 'smoker', form.cleaned_data['smoker'])
                    filters.append((_('Smoker'), _('No'), new_path))

            if form.cleaned_data['diet'] != '---------' and form.cleaned_data['diet']:
                filtered_politicians = filtered_politicians.filter(diet__iexact=form.cleaned_data['diet'])
                new_path = _new_url(path, 'diet', form.cleaned_data['diet'])
                filters.append((_('Vegitarian'), diet[form.cleaned_data['diet']], new_path))
            filtered_politicians = filtered_politicians.distinct().select_related('user')

            #no query executed so far, so we see if we can do some caching stuff here :)
            cache_key = hashlib.sha224(str(filtered_politicians.query)).hexdigest()
            data = cache.get(cache_key)
            if data is None:
                #Force query to execute
                politicians = list(filtered_politicians)

                query = elections_candidates.select_related('candidate', 'election_party_instance__party', 'election_party_instance__election_instance__council').values_list('candidate__id', 'election_party_instance__party__abbreviation', 'election_party_instance__election_instance__name')
                party_data = {}
                for (can_id, party, region) in query:
                    data = party_data.get(can_id, [])
                    if data is None:
                        data = [(party, region)]
                    else:
                        data.append((party, region))
                    party_data.update({can_id: data})
                cache.set(cache_key, (politicians, party_data), settings.POLITICIAN_BROWSER_CACHE_TIMEOUT)
            else:
                (politicians, party_data) = data
        else:
            party_data = {}
            politicians = []
            form = PoliticianFilterForm() # An unbound form


        p = Paginator(politicians, 24)
        # Make sure page request is an int. If not, deliver first page.
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        # If page request (9999) is out of range, deliver last page of results.
        try:
            politicians = p.page(page)
        except:
            politicians = p.page(p.num_pages)

    return render_to_response('frontoffice/politician_filter.html', {'party_data': party_data, 'region_filtered':region_filtered, 'filters':filters, 'politicians':politicians, 'form':form, 'num_filters':len(filters) }, context_instance=RequestContext(request))


def politician_profile(request, id, tab = "favs"):
    user = get_object_or_404(User, pk=id)
    profile = get_object_or_404(PoliticianProfile, user=user)
    if Candidacy.objects.filter(candidate=user).count() == 0:
        return Http404()
    showtab = tab

    current_eip = getattr(profile.party(), 'current_eip')
    if current_eip is None:
        return Http404()
    else:
        ei = current_eip.election_instance

    election_instance = get_object_or_404(ElectionInstance, pk=ei.pk)
    request.session['ElectionInstance'] = dict(id=election_instance.id, name=election_instance.name)

    if 'back' in request.GET:
        back = request.GET['back']
    else:
        back = None

    #Getting the twitter RSS feed URL
    try:
        twitter = profile.connections.filter(type__type='Twitter')[0] #Raises an exception if no twitter account is entered
        regex = re.compile(r"/(?P<id>[A-Za-z0-9\-=_]+)/?$")
        match = regex.search(twitter.url)
        username = match.group('id')
        twitter_url = mark_safe("""http://www.twitter.com/statuses/user_timeline/%(username)s.rss""" % {'username':username})
    except:
        twitter_url = None

    #record view
    user.statistics.update_profile_views(request)

    return render_to_response('frontoffice/politician_profile.html', {'profile':profile,'twitter_url':twitter_url,'showtab':showtab, 'back':back}, context_instance=RequestContext(request))

def politician_comments(request, id):
    user = get_object_or_404(User, pk=id)
    profile = get_object_or_404(PoliticianProfile, user=user)

    return render_to_response('frontoffice/politician_comments.html', {'profile':profile}, context_instance=RequestContext(request))

def party_profile(request, eip_id, tab='can'):
    eip = get_object_or_404(ElectionInstanceParty, pk=eip_id)
    return render_to_response('frontoffice/party.html', {'eip': eip, 'showtab':tab }, context_instance=RequestContext(request))

#def dashboard(request):
#    """
#        Render a generic page for any kind of user, from where the user can do whatever they have rights for.
#    """
#    user = request.user
#    try:
#        profile = user.profile #Every logged in user has a profile, right?
#    except AttributeError:
#        return redirect('fo.login')
#    return render_to_response('frontoffice/dashboard.html', {'user': user, 'profile': profile}, context_instance=RequestContext(request))

@login_required
def edit_visitor_profile(request):
    user = request.user

    if user.profile and user.profile.type != 'visitor':
        return redirect('fo.redirect')

    profile = get_object_or_404(VisitorProfile, user=user)
    results = VisitorResult.objects.filter(user=user)

    if request.method == 'POST':
        form = VisitorProfileForm(request.POST)
        if form.is_valid():
            data = form.clean()
            profile.first_name = data['name']['first_name']
            profile.middle_name = data['name']['middle_name']
            profile.last_name = data['name']['last_name']
            profile.phone = data['phone']
            profile.send_text = data['send_text']

            profile.save()

    else:
        initial_dict = {
            'name': {'first_name': profile.first_name, 'middle_name': profile.middle_name, 'last_name': profile.last_name, },
            'phone': profile.phone,
            'send_text': profile.send_text,
            }
        form = VisitorProfileForm(initial=initial_dict)

    return render_to_response('frontoffice/visitor_profile.html', {'results':results, 'profile': profile, 'form':form}, context_instance=RequestContext(request))

@login_required
@visitors_only
def fan_add(request, politician_id):
    """ Become a fan of a politician """
    user = get_object_or_404(User, pk = politician_id)
    profile = get_object_or_404(PoliticianProfile, user = user)
    request.user.profile.favorites.add(profile)
    return redirect('fo.politician_profile', id = politician_id)

@login_required
@visitors_only
def fan_remove(request, politician_id):
    """ Remove politician from fan list. """
    user = get_object_or_404(User, pk = politician_id)
    profile = get_object_or_404(PoliticianProfile, user = user)
    request.user.profile.favorites.remove(profile)
    if request.method == 'GET':
        if 'redirect' in request.GET:
            return redirect(request.GET['redirect'])
    return redirect('fo.politician_profile', id = politician_id)


@visitors_only
def thumbs_up(request, goal_id):
    goal = get_object_or_404(PoliticalGoal, pk=goal_id)
    user = request.user
    try:
        rank, created = GoalRanking.objects.get_or_create(user=user, goal=goal, defaults={'ranking': 0})
        rank.ranking = 1
        rank.save()
    except:
        pass

    return redirect('fo.politician_profile', id = goal.politician.user.id)


@visitors_only
def thumbs_down(request, goal_id):
    goal = get_object_or_404(PoliticalGoal, pk=goal_id)
    user = request.user
    try:
        rank, created = GoalRanking.objects.get_or_create(user=user, goal=goal, defaults={'ranking': 0})
        rank.ranking = -1
        rank.save()
    except:
        pass

    return redirect('fo.politician_profile', id = goal.politician.user.id)


def home(request):
    region = 6
    #if request.method == 'POST':
    #    form = RegionSelectForm(request.POST)
    #    if form.is_valid():
    #        region = form.cleaned_data['region']
    #        dict = {'id': region.id, 'name': region.name}
    #        request.session['ElectionInstance'] = dict
    #else:
    #    form = RegionSelectForm()
    dict = {'id': 1, 'name': 'Tweede kamer verkiezingen 2012'}
    request.session['ElectionInstance'] = dict
    form = RegionSelectForm()

    if 'ElectionInstance' in request.session:
        initial_dict = {'region': request.session['ElectionInstance'].get('id')}
        form = RegionSelectForm(initial=initial_dict) #overwrite the form

    return render_to_response('frontoffice/home.html', {'form': form}, context_instance=RequestContext(request))

def opensocial_sharing(request, hash):
    result = get_object_or_404(VisitorResult,hash=hash) #Just to make sure we have a valid hash
    request.session['ElectionInstance'] = dict(id=result.election_instance.id, name=result.election_instance.name)
    return render_to_response('frontoffice/opensocial_sharing.html', {'hash': hash, 'election_instance': result.election_instance}, context_instance=RequestContext(request))

def match_result_details(request, hash, candidate_id, iframe=None):
    result = get_object_or_404(VisitorResult,hash=hash)
    request.session['ElectionInstance'] = dict(id=result.election_instance.id, name=result.election_instance.name)

    candidate = result.candidate_answers.get(candidate=candidate_id)

    visitors_answer =  json.loads(result.visitor_answers)
    candidate_answer =  json.loads(candidate.candidate_answers)
    candidate_scores =  json.loads(candidate.candidate_question_scores)
    candidate_score = {}
    questions_dict = {}
    for i in candidate_scores:
        for key, value in i.items():
            candidate_score[key] = value

    for qid, ans in visitors_answer.items():

        qid = str(qid)
        question = get_object_or_404(Question ,id=qid)
        questions_dict[qid] = {}
        questions_dict[qid]['visitor'] = ans
        questions_dict[qid]['question'] = question
        if qid in candidate_score.keys():
            questions_dict[qid]['score'] = candidate_score[qid]
        else:
            questions_dict[qid]['score'] = 0
        if qid in candidate_answer.keys():
            questions_dict[qid]['candidate'] = candidate_answer[qid]

    for key in questions_dict.keys():
        if questions_dict[key]['question'].question_type == 'H':
            weighted_questions = questions_dict[key]['visitor']

    skipped = 0
    weighted = len(weighted_questions[0])
    for key in questions_dict.keys():
        if 'no_pref' in questions_dict[key]['visitor']:
            skipped = skipped + 1
            if questions_dict[key]['question'].theme in weighted_questions[0]:
                weighted = weighted - 1
            questions_dict[key]['doubled'] = False
            questions_dict[key]['skipped'] = True
        else:
            questions_dict[key]['skipped'] = False
            if questions_dict[key]['question'].theme in weighted_questions[0]:
                questions_dict[key]['doubled'] = True
            else:
                questions_dict[key]['doubled'] = False

    num_questions = len(visitors_answer) -2 - skipped + weighted
    for key in questions_dict.keys():

        question = questions_dict[key]['question']

        questions_dict[key]['question_type'] = question.question_type
        if questions_dict[key]['doubled'] == True:
            questions_dict[key]['score'] = (questions_dict[key]['score'] * num_questions) / 2
        else:
            questions_dict[key]['score'] = (questions_dict[key]['score'] * num_questions)

        if  questions_dict[key]['score'] > 100 and settings.DEBUG == False:
            questions_dict[key]['score'] = 100

        if question.question_type in qsettings.BACKOFFICE_QUESTION_TYPES:
            questions_dict[key]['type'] = 'backoffice'
            if 'no_pref' not in questions_dict[key]['visitor']:
                answers = []
                for answer in Answer.objects.filter(id__in=questions_dict[key]['visitor']):
                    answers.append(answer.value)
                questions_dict[key]['visitor'] = answers
                if 'candidate' in questions_dict[key].keys():
                    answers = []
                    for answer in  Answer.objects.filter(id__in=questions_dict[key]['candidate']):
                        answers.append(answer.value)
                    questions_dict[key]['candidate'] = answers

                else:
                    questions_dict[key]['candidate'] = ['Not Answered']
            else:
                questions_dict[key]['visitor'] = ['Question Skipped']
        elif qsettings.QTYPE_MODEL_PARTY == question.question_type:
            questions_dict[key]['type'] = 'party'
            if 'candidate' in questions_dict[key].keys():
                temp_list = []
                eip = get_object_or_404(Party,id=questions_dict[key]['candidate'])
                temp_list.append(eip.name)
                questions_dict[key]['candidate'] = temp_list
                questions_dict[key]['score'] = 100
            else:
                questions_dict[key]['candidate'] = ['Not Answered']

        elif qsettings.QTYPE_MODEL_POLITICAL_EXPERIENCE_YEARS == question.question_type:
            questions_dict[key]['type'] = 'political_experience'
            if 'no_pref' not in questions_dict[key]['visitor']:
                answers = []
                for answer in Answer.objects.filter(id__in=questions_dict[key]['visitor']):
                    answers.append(answer.value)
                questions_dict[key]['visitor'] = answers
            else:
                questions_dict[key]['visitor'] = ['Question Skipped']
            if 'candidate' in questions_dict[key].keys():
                temp_list = []
                if candidate.candidate.profile.political_experience_days:
                    number = int((candidate.candidate.profile.political_experience_days)/365)
                else:
                    number = 0
                years_worked = ungettext('Candidate has %(number)d year experience', 'Candidate has %(number)d years experience', number) % {'number': number}

                temp_list.append(years_worked)
                questions_dict[key]['candidate'] = temp_list
            else:
                questions_dict[key]['candidate'] = ['Not Answered']

        elif qsettings.QTYPE_MODEL_EDUCATION_LEVEL == question.question_type:
            if 'no_pref' not in questions_dict[key]['visitor']:
                questions_dict[key]['visitor'] = questions_dict[key]['visitor']
            else:
                questions_dict[key]['visitor'] = ['Question Skipped']
            if 'candidate' in questions_dict[key].keys():

                answers = []
                for answer in  Education.objects.filter(politician=candidate.candidate.profile):
                    answers.append(answer.level)

                questions_dict[key]['candidate'] = answers
            else:
                questions_dict[key]['candidate'] = ['Not Answered']
        elif qsettings.QTYPE_MODEL_PROFILE_RELIGION == question.question_type:
            if 'no_pref' not in questions_dict[key]['visitor']:
                answers = []
                for ans in questions_dict[key]['visitor']:
                    answers.append(ans)
                questions_dict[key]['visitor'] = answers
            else:
                questions_dict[key]['visitor'] = ['Question Skipped']

            if 'candidate' in questions_dict[key].keys():
                temp_list = []
                temp_list.append(questions_dict[key]['candidate'])
                questions_dict[key]['candidate'] = temp_list
            else:
                questions_dict[key]['candidate'] = ['Not Answered']
        elif qsettings.QTYPE_MODEL_PROFILE_AGE == question.question_type:
            if 'no_pref' not in questions_dict[key]['visitor']:
                answers = []
                for answer in Answer.objects.filter(id__in=questions_dict[key]['visitor']):
                    answers.append(answer.value)
                questions_dict[key]['visitor'] = answers
            else:
                questions_dict[key]['visitor'] = ['Question Skipped']
            if 'candidate' in questions_dict[key].keys():

                temp_list = []
                temp_list.append(questions_dict[key]['candidate'])
                questions_dict[key]['candidate'] = temp_list
            else:
                questions_dict[key]['candidate'] = ['Not Answered']
        elif qsettings.QTYPE_MODEL_PROFILE_GENDER == question.question_type:
            if 'no_pref' not in questions_dict[key]['visitor']:
                answers = []
                answers.append(questions_dict[key]['visitor'])
                questions_dict[key]['visitor'] = answers
            else:
                questions_dict[key]['visitor'] = ['Question Skipped']
            if 'candidate' in questions_dict[key].keys():
                questions_dict[key]['candidate'] = questions_dict[key]['candidate']
            else:
                questions_dict[key]['candidate'] = ['Not Answered']

        elif qsettings.QTYPE_MODEL_PROFILE_QUESTION_WEIGHT == question.question_type:
                questions_dict[key]['visitor'] = 'weighted'

        else:
            pass
        questions_dict[key]['score'] = int(questions_dict[key]['score'])
        questions_dict[key]['question'] = question.result_title

    if iframe:
        parent = 'frontoffice/iframe.html'
    else:
        parent = 'frontoffice/base.html'

    returndict = {'hash': hash, 'questions':questions_dict,'candidate':candidate,'parent': parent, 'iframe': iframe, 'election_instance': result.election_instance}

    return render_to_response('frontoffice/match_details.html', returndict, context_instance=RequestContext(request))
