from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.urlresolvers import reverse

#from frontoffice.forms import PoliticianFilterForm
from elections.models import Candidacy, ElectionInstance, ElectionInstanceParty
from political_profiles import PoliticianProfile
from utils.functions import list_unique_order_preserving



def politician_profile_filter(request):
    politicians = []
    if request.method == 'GET':
        form = PoliticianFilterForm(request.GET) # A form bound to the GET data
        election_instances = ElectionInstance.objects.filter(election_event = settings.ELECTIONS_ELECTION_EVENT_ID)
        eips = ElectionInstanceParty.objects.filter(election_instance__in=election_instances)
        elections_candidates = Candidacy.objects.filter(election_party_instance__in=eips)
        candidates = User.objects.filter(pk__in=elections_candidates)
        politicians = PoliticianProfile.objects.filter(pk__in=candidates)

        #for election_candidate in elections_candidates:
        #    politicians.append(get_object_or_404(User, pk=election_candidate.candidate_id).profile)

        if form.is_valid():
            # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            filtered_candidates = []
            if form.cleaned_data['name']:

                for name in form.cleaned_data['name'].split():
                    filtered_candidates.extend(politicians.filter(last_name__contains=name))
                    filtered_candidates.extend(politicians.filter(first_name__contains=name))
                    filtered_candidates.extend(politicians.filter(middle_name__contains=name))


                politicians = filtered_candidates
                politicians = list_unique_order_preserving(filtered_candidates)







        else:
            form = PoliticianFilterForm() # An unbound form

    return render_to_response('frontoffice/politician_filter.html', {'politicians':politicians, 'form':form }, context_instance=RequestContext(request))



