import re
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from frontoffice.forms import PoliticianFilterForm
from elections.models import Candidacy, ElectionInstance, ElectionInstanceParty
from political_profiles import PoliticianProfile
from utils.functions import list_unique_order_preserving
from django.db.models import Q
import datetime



def politician_profile_filter(request):
    politicians = []
    if request.method == 'GET':
        form = PoliticianFilterForm(request.GET) # A form bound to the GET data
        election_instances = ElectionInstance.objects.filter(election_event = settings.ELECTIONS_ELECTION_EVENT_ID)
        eips = ElectionInstanceParty.objects.filter(election_instance__in=election_instances)
        elections_candidates = Candidacy.objects.filter(election_party_instance__in=eips)
        candidates = User.objects.filter(pk__in=elections_candidates)
        politicians = PoliticianProfile.objects.filter(pk__in=candidates).order_by('?')
        filtered_politicians = politicians

        if form.is_valid():
            # All validation rules pass
            # Process the data in form.cleaned_data
            # ...

            if form.cleaned_data['name']:
                name_filter = None
                for name in form.cleaned_data['name'].split():
                    if name_filter is None:
                        name_filter = (Q(last_name__icontains=name) | Q(first_name__icontains=name) | Q(middle_name__icontains=name))
                    else:
                        name_filter = name_filter &  (Q(last_name__icontains=name) | Q(first_name__icontains=name) | Q(middle_name__icontains=name))
                filtered_politicians = filtered_politicians.filter(name_filter)
            print filtered_politicians
            if form.cleaned_data['gender'] != 'Either' and form.cleaned_data['gender']:
                filtered_politicians = filtered_politicians.filter(gender=form.cleaned_data['gender'])
            print filtered_politicians
            if form.cleaned_data['children'] is not None:
                if form.cleaned_data['children'] == 1:
                    filtered_politicians = filtered_politicians.filter(num_children__gte=1)
                else:
                    filtered_politicians = filtered_politicians.filter(num_children=0)

            


            """ Calculate date from age - uses rough estimate of how 36 years 
            ago - its rough because of leapyears - to compensate will add two
            weeks to either side of age so more candidates will sho even if 
            they are a bit older or a bit younger"""

            year = datetime.timedelta(days=365)
            extra = datetime.timedelta(days=10)
            if form.cleaned_data['start_age'] is not None:
                date = datetime.datetime.now() - (year * form.cleaned_data['start_age']) + extra
                filtered_politicians = filtered_politicians.filter(dateofbirth__lte=date)
            if form.cleaned_data['end_age'] is not None:
                date = datetime.datetime.now() - (year * form.cleaned_data['end_age']) - extra

                filtered_politicians = filtered_politicians.filter(dateofbirth__gte=date)


            if form.cleaned_data['education']:
                filtered_politicians = filtered_politicians.filter(education__level=form.cleaned_data['education'])
            if form.cleaned_data['political_exp_years']:
                filtered_politicians = filtered_politicians.filter(political_experience_days__gte=(form.cleaned_data['political_exp_years'] * 365))

            politicians = list_unique_order_preserving(filtered_politicians)
 
        else:
            politicians = []
            form = PoliticianFilterForm() # An unbound form

    return render_to_response('frontoffice/politician_filter.html', {'politicians':politicians, 'form':form }, context_instance=RequestContext(request))


def politician_profile(request, id):
    user = get_object_or_404(User, pk=id)
    profile = get_object_or_404(PoliticianProfile, user=user)
    try:
        showtab = request.GET['tab']
    except:
        showtab = "favs"

    #Getting the twitter RSS feed URL
    try:
        twitter = profile.connections.filter(type__type='Twitter')[0]
        regex = re.compile(r"^(http://)?(www\.)?(twitter\.com/)?(?P<id>[A-Za-z0-9\-=_]+)")
        match = regex.match(twitter.url)
        if not match: return ""
        username = match.group('id')
        twitter_url = mark_safe("""http://www.twitter.com/statuses/user_timeline/%(username)s.rss""" % {'username':username})
    except:
        twitter_url = None

    return render_to_response('frontoffice/profile.html', { 'profile':profile,
                                                            'user':user,
                                                            'twitter_url': twitter_url,
                                                            'showtab':showtab}, context_instance=RequestContext(request))