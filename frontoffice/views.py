
import re
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from frontoffice.forms import PoliticianFilterForm
from elections.models import Candidacy, ElectionInstance, ElectionInstanceParty, Party
from political_profiles.models import PoliticianProfile, EducationLevel
from utils.functions import list_unique_order_preserving
from django.db.models import Q
import datetime
from political_profiles.models import MOTIVATION, CHURCH, DIET, LIFE_STANCE, MARITAL_STATUS, GENDERS, NEWSPAPER, TRANSPORT, CHARITY, MEDIA, SPORT, HOBBIES , CLUBS, PETS


def new_url(path, field, value):
    old_str = field + '='  + str(value)
    old_str = old_str.replace(' ','+')

    new_str = field + '='

    return path.replace(old_str, new_str)


def election(request, id=None):

    politicians = []
    election_instances = ElectionInstance.objects.filter(election_event = settings.ELECTIONS_ELECTION_EVENT_ID)
    selected_eip = None
    eips = ElectionInstanceParty.objects.filter(election_instance__in=election_instances).order_by('position')
    if id:
        selected_eip = ElectionInstanceParty.objects.get(id=id)
        politicians = selected_eip.candidate_dict()

   
    return render_to_response('frontoffice/election.html', {'selected_eip':selected_eip, 'eips':eips, 'politicians':politicians }, context_instance=RequestContext(request))


def politician_profile_filter(request):
    politicians = []
    gender = dict(GENDERS)
    church = dict(CHURCH)
    life_stance = dict(LIFE_STANCE)
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

            year = datetime.timedelta(days=365)
            todate = datetime.date.today()
            if form.cleaned_data['start_age'] is not None:
    
                date = datetime.date(todate.year - (form.cleaned_data['start_age']), todate.month, todate.day)

                filtered_politicians = filtered_politicians.filter(dateofbirth__lt=date)
                new_path = new_url(path, 'start_age', form.cleaned_data['start_age'])
                filters.append((_('Youngest'), form.cleaned_data['start_age'], new_path))

                print date, 'young', filtered_politicians
            if form.cleaned_data['end_age'] is not None:
                #import ipdb; ipdb.set_trace()
                date = datetime.date(todate.year - (form.cleaned_data['end_age'] + 1), todate.month, todate.day)
                print date, 'old', filtered_politicians
                filtered_politicians = filtered_politicians.filter(dateofbirth__gte=date)
                print date, 'old', filtered_politicians
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
                filtered_politicians = filtered_politicians.filter(church=form.cleaned_data['religion'])
                new_path = new_url(path, 'religion', form.cleaned_data['religion'])
                filters.append((_('Religion'), church[form.cleaned_data['religion']], new_path))
            if form.cleaned_data['marital_status'] != '---------' and form.cleaned_data['marital_status']:
                filtered_politicians = filtered_politicians.filter(marital_status=form.cleaned_data['marital_status'])
                new_path = new_url(path, 'marital_status', form.cleaned_data['marital_status'])
                filters.append((_('Marital status'), marital_status[form.cleaned_data['marital_status']], new_path))
            if form.cleaned_data['life_stance'] != '---------' and form.cleaned_data['life_stance']:
                filtered_politicians = filtered_politicians.filter(life_stance=form.cleaned_data['life_stance'])
                new_path = new_url(path, 'life_stance', form.cleaned_data['life_stance'])
                filters.append((_('Life stance'), life_stance[form.cleaned_data['life_stance']], new_path))
            if form.cleaned_data['goals'] != '---------' and form.cleaned_data['goals']:
                filtered_politicians = filtered_politicians.filter(goals__goal__icontains=form.cleaned_data['life_stance'])
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
    except:
        twitter_url = None

    return render_to_response('frontoffice/profile.html', {'profile':profile,'twitter_url':twitter_url,'showtab':showtab}, context_instance=RequestContext(request))
                                                            
                                                            
def party_profile(request, eip_id):
    eip = get_object_or_404(ElectionInstanceParty, pk=eip_id)
    
    return render_to_response('frontoffice/party.html', {'eip': eip }, context_instance=RequestContext(request))
