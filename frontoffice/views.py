
import re
from django.http import Http404
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from frontoffice.forms import PoliticianFilterForm, VisitorProfileForm
from elections.models import Candidacy, ElectionInstance, ElectionInstanceParty
from political_profiles.models import PoliticianProfile, PoliticalGoal, GoalRanking, VisitorProfile
from utils.functions import list_unique_order_preserving
from django.db.models import Q
import datetime

from political_profiles.models import RELIGION, DIET, MARITAL_STATUS, GENDERS

from frontoffice.decorators import visitors_only

from django.core.paginator import Paginator
from questions.forms.types import ModelAnswerForm
from frontoffice.wizards.test import BestCandidate

def redirect_view(request):
    if not request.user.is_authenticated():
        return redirect('fo.dashboard') #for testing, make take_test
    elif not request.user.profile and request.user.is_staff:
        return redirect('bo.redirect')
    elif request.user.profile.type == 'visitor':
        return redirect('fo.dashboard') #for testing, make take_test
    else:
        return redirect('bo.redirect')

def new_url(path, field, value):
    old_str = field + '='  + str(value)
    old_str = old_str.replace(' ','+')

    new_str = field + '='

    return path.replace(old_str, new_str)

def answer_question(request, election_instance_party_id, user_id=None):
    '''
        AnswerQuestion - wizard.
        @param int election_instance_party_id - ElectionInstanceParty id
        @param int user_id User (Candidate=PoliticalProfile) id
    '''
    check_permissions(request, election_instance_party_id, 'candidate')
    return AnswerQuestion(election_instance_party_id=election_instance_party_id, user_id=user_id)(request)

def test(request, election_instance_party_id):
    


    return BestCandidate(election_instance_party_id=election_instance_party_id)(request)

def election(request, id=None):

    politicians = []
    election_instances = ElectionInstance.objects.filter(election_event = settings.ELECTIONS_ELECTION_EVENT_ID)
    selected_eip = None
    eips = ElectionInstanceParty.objects.filter(election_instance__in=election_instances).order_by('position')
    if id:
        selected_eip = get_object_or_404(ElectionInstanceParty, id=id)
        politicians = selected_eip.candidate_dict()

   
    return render_to_response('frontoffice/election.html', {'selected_eip':selected_eip, 'eips':eips, 'politicians':politicians }, context_instance=RequestContext(request))

def goal(request, id):
    goal = get_object_or_404(PoliticalGoal, pk=id)

    return render_to_response('frontoffice/goal.html', {'goal': goal}, context_instance=RequestContext(request))



def politician_profile_filter(request):
    politicians = []
    gender = dict(GENDERS)
    religion = dict(RELIGION)
    marital_status = dict(MARITAL_STATUS)
    diet = dict(DIET)


    if request.method == 'GET':
        form = PoliticianFilterForm(request.GET) # A form bound to the GET data
        election_instances = ElectionInstance.objects.filter(election_event = settings.ELECTIONS_ELECTION_EVENT_ID)
        eips = ElectionInstanceParty.objects.filter(election_instance__in=election_instances)
        elections_candidates = Candidacy.objects.filter(election_party_instance__in=eips)
        candidates = User.objects.filter(pk__in=elections_candidates)
        politicians = PoliticianProfile.objects.filter(pk__in=candidates).order_by('?')
        filtered_politicians = politicians
        path = request.get_full_path()
        region_filtered = False
        if form.is_valid():
            # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            filters = []

            if form.cleaned_data['region'] != '---------' and form.cleaned_data['region']:
                election_instances = ElectionInstance.objects.filter(election_event = settings.ELECTIONS_ELECTION_EVENT_ID, id=form.cleaned_data['region'].id)
                eips = ElectionInstanceParty.objects.filter(election_instance__in=election_instances)
                elections_candidates = Candidacy.objects.filter(election_party_instance__in=eips)
                candidates = User.objects.filter(pk__in=elections_candidates)
                politicians = PoliticianProfile.objects.filter(pk__in=candidates).order_by('?')
                filtered_politicians = politicians
 
                new_path = new_url(path, 'region', form.cleaned_data['region'].id)
                region_filtered = True
                filters.append((_('Region'), form.cleaned_data['region'].council.region, new_path))


            if form.cleaned_data['name']:
                name_filter = None
                for name in form.cleaned_data['name'].split():
                    if name_filter is None:
                        name_filter = (Q(last_name__icontains=name) | Q(first_name__icontains=name) | Q(middle_name__icontains=name))
                    else:
                        name_filter = name_filter &  (Q(last_name__icontains=name) | Q(first_name__icontains=name) | Q(middle_name__icontains=name))
                filtered_politicians = filtered_politicians.filter(name_filter)
                new_path = new_url(path, 'name', form.cleaned_data['name'])
                filters.append((_('Name'), form.cleaned_data['name'], new_path))
            if form.cleaned_data['gender'] != 'All' and form.cleaned_data['gender']:
                filtered_politicians = filtered_politicians.filter(gender=form.cleaned_data['gender'])
                new_path = new_url(path, 'gender', form.cleaned_data['gender'])
                filters.append((_('Gender'), gender[form.cleaned_data['gender']], new_path))


            if form.cleaned_data['children']  != '---------' and form.cleaned_data['children']:
                if form.cleaned_data['children'] == 1:
                    filtered_politicians = filtered_politicians.filter(num_children__gte=1)
                    new_path = new_url(path, 'children', form.cleaned_data['children'])
                    filters.append((_('Children'), _('Yes'), new_path))
                else:
                    filtered_politicians = filtered_politicians.filter(num_children=0)
                    new_path = new_url(path, 'children', form.cleaned_data['children'])
                    filters.append((_('Children'), _('No'), new_path))



            """ Calculate date from age - uses rough estimate of how 36 years 
            ago - its rough because of leapyears - to compensate will add two
            weeks to either side of age so more candidates will sho even if 
            they are a bit older or a bit younger"""

            todate = datetime.date.today()
            if form.cleaned_data['start_age'] is not None:
    
                date = datetime.date(todate.year - (form.cleaned_data['start_age']), todate.month, todate.day)

                filtered_politicians = filtered_politicians.filter(dateofbirth__lt=date)
                new_path = new_url(path, 'start_age', form.cleaned_data['start_age'])
                filters.append((_('Youngest'), form.cleaned_data['start_age'], new_path))


            if form.cleaned_data['end_age'] is not None:
                date = datetime.date(todate.year - (form.cleaned_data['end_age'] + 1), todate.month, todate.day)

                filtered_politicians = filtered_politicians.filter(dateofbirth__gte=date)

                new_path = new_url(path, 'end_age', form.cleaned_data['end_age'])
                filters.append((_('Oldest'), form.cleaned_data['end_age'], new_path))

            if form.cleaned_data['education'] != '---------' and form.cleaned_data['education']:
                filtered_politicians = filtered_politicians.filter(education__level=form.cleaned_data['education'])
                new_path = new_url(path, 'education', form.cleaned_data['education'].id)

                filters.append((_('Education'), form.cleaned_data['education'], new_path))
            if form.cleaned_data['political_exp_years']:
                filtered_politicians = filtered_politicians.filter(political_experience_days__gte=(form.cleaned_data['political_exp_years'] * 365))
                new_path = new_url(path, 'political_exp_years', form.cleaned_data['political_exp_years'])
                filters.append((_('Years political experience'), form.cleaned_data['political_exp_years'], new_path))
            if form.cleaned_data['work_exp_years']:
                filtered_politicians = filtered_politicians.filter(work_experience_days__gte=(form.cleaned_data['work_exp_years'] * 365))
                new_path = new_url(path, 'work_exp_years', form.cleaned_data['work_exp_years'])
                filters.append((_('Years work experience'), form.cleaned_data['work_exp_years'], new_path))

            if form.cleaned_data['religion'] != '---------' and form.cleaned_data['religion']:
                filtered_politicians = filtered_politicians.filter(religion=form.cleaned_data['religion'])
                new_path = new_url(path, 'religion', form.cleaned_data['religion'])
                filters.append((_('Religion'), religion[form.cleaned_data['religion']], new_path))
            if form.cleaned_data['marital_status'] != '---------' and form.cleaned_data['marital_status']:
                filtered_politicians = filtered_politicians.filter(marital_status=form.cleaned_data['marital_status'])
                new_path = new_url(path, 'marital_status', form.cleaned_data['marital_status'])
                filters.append((_('Marital status'), marital_status[form.cleaned_data['marital_status']], new_path))
            if form.cleaned_data['goals'] != '---------' and form.cleaned_data['goals']:
                filtered_politicians = filtered_politicians.filter(goals__goal__icontains=form.cleaned_data['goals'])
                new_path = new_url(path, 'goals', form.cleaned_data['goals'])
                filters.append((_('Goals'), form.cleaned_data['goals'], new_path))
            if form.cleaned_data['smoker'] != '---------' and form.cleaned_data['smoker']:
                filtered_politicians = filtered_politicians.filter(smoker=form.cleaned_data['smoker'])
                if form.cleaned_data['smoker'] == 1:
                    new_path = new_url(path, 'smoker', form.cleaned_data['smoker'])
                    filters.append((_('Smoker'), _('Yes'), new_path))
                else:
                    new_path = new_url(path, 'smoker', form.cleaned_data['smoker'])
                    filters.append((_('Smoker'), _('No'), new_path))

            if form.cleaned_data['diet'] != '---------' and form.cleaned_data['diet']:
                if form.cleaned_data['diet'] == '':
                    filtered_politicians = filtered_politicians.filter(diet='ja')
                if form.cleaned_data['diet'] == '':
                    filtered_politicians = filtered_politicians.filter(diet='nee')
                if form.cleaned_data['diet'] == '':
                    filtered_politicians = filtered_politicians.filter(diet='vegetarian')
                if form.cleaned_data['diet'] == '':
                    filtered_politicians = filtered_politicians.filter(diet='vegan')
                if form.cleaned_data['diet'] == '':
                    filtered_politicians = filtered_politicians.filter(diet='other')
                new_path = new_url(path, 'diet', form.cleaned_data['diet'])
                filters.append((_('Vegitarian'), diet[form.cleaned_data['diet']], new_path))
            politicians = list_unique_order_preserving(filtered_politicians)


                
        else:
            politicians = []
            form = PoliticianFilterForm() # An unbound form
        p = Paginator(politicians, 6)
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

    return render_to_response('frontoffice/politician_filter.html', {'region_filtered':region_filtered, 'filters':filters, 'politicians':politicians, 'form':form }, context_instance=RequestContext(request))


def politician_profile(request, id, tab = "favs"):
    user = get_object_or_404(User, pk=id)
    profile = get_object_or_404(PoliticianProfile, user=user)
    showtab = tab

    #Getting the twitter RSS feed URL
    try:
        twitter = profile.connections.filter(type__type='Twitter')[0] #Raises an exception if no twitter account is entered
        regex = re.compile(r"^(http://)?(www\.)?(twitter\.com/)?(?P<id>[A-Za-z0-9\-=_]+)")
        match = regex.match(twitter.url)
        username = match.group('id')
        twitter_url = mark_safe("""http://www.twitter.com/statuses/user_timeline/%(username)s.rss""" % {'username':username})

        # record view
        #user.statistics.update_profile_views(request)
    except:
        twitter_url = None

    return render_to_response('frontoffice/politician_profile.html', {'profile':profile,'twitter_url':twitter_url,'showtab':showtab, 'test_url': 'http://www.google.com/ig?refresh=1'}, context_instance=RequestContext(request))

def politician_comments(request, id):
    user = get_object_or_404(User, pk=id)
    profile = get_object_or_404(PoliticianProfile, user=user)
    
    return render_to_response('frontoffice/politician_comments.html', {'profile':profile}, context_instance=RequestContext(request))
                                                            
def party_profile(request, eip_id):
    eip = get_object_or_404(ElectionInstanceParty, pk=eip_id)
    
    return render_to_response('frontoffice/party.html', {'eip': eip }, context_instance=RequestContext(request))

def dashboard(request):
    """
        Render a generic page for any kind of user, from where the user can do whatever they have rights for.
    """
    user = request.user
    try:
        profile = user.profile #Every logged in user has a profile, right?
    except AttributeError:
        return redirect('fo.login')
    return render_to_response('frontoffice/dashboard.html', {'user': user, 'profile': profile}, context_instance=RequestContext(request))

#def edit_profile(request):
#    user = request.user
#    try:
#        profile = user.profile #Every logged in user has a profile, right?
#    except AttributeError:
#        raise Http404
#
#    return redirect('fo.'+profile.type+'.edit_profile')

@visitors_only
def edit_visitor_profile(request):
    user = request.user
    profile = get_object_or_404(VisitorProfile, user=user)

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

    return render_to_response('frontoffice/visitor_profile.html', {'profile': profile, 'form':form}, context_instance=RequestContext(request))

@visitors_only
def fan_add(request, politician_id):
    """ Become a fan of a politician """
    user = get_object_or_404(User, pk = politician_id)
    profile = get_object_or_404(PoliticianProfile, user = user)
    request.user.profile.favorites.add(profile)
    return redirect('fo.politician_profile', id = politician_id)


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
    # [FIXME: bug in django 1.1, .only('council__region') produces correct SQL
    # (checked using django-toolbar), later elinstance.council.region is empty.
    # It is not empty if whole council object is fetched (unnecesary data)]
    election_instances = ElectionInstance.objects.filter(election_event = settings.ELECTIONS_ELECTION_EVENT_ID).select_related('council').only('id', 'council')
    
    rt = [ (el.pk, el.council.region) for el in election_instances ]
    return render_to_response('frontoffice/home.html', {'elections': rt}, context_instance=RequestContext(request))
