
#!/usr/env python
#-*- coding: utf-8 -*-
#
#Copyright 2009 Accepte. All Rights Reserved.

import os
import time
import csv

from django.db import transaction
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _


from questions.settings import BACKOFFICE_QUESTION_TYPES

from elections.settings import ELECTION_EVENT_ID
from elections.models import ElectionInstance, ElectionInstanceParty, Party, Candidacy
from elections.functions import create_profile, profile_invite_email_templates, get_profile_template, get_profile_forms

from invitations.models import Invitation

from political_profiles import functions
from political_profiles.forms import CsvUploadForm, CsvConfirmForm, AgreeForm

from utils.exceptions import PermissionDeniedException
from backoffice.decorators import staff_required, candidate_required, council_admin_required , party_admin_required

from backoffice.wizards import AddElectionPartyWizard, PoliticianProfileInterestWizard, PoliticianProfileWorkWizard
from backoffice.wizards import PoliticianProfileConnectionWizard, PoliticianProfilePoliticalWizard, PoliticianProfileEducationWizard, PoliticianProfileLinkWizard
from backoffice.wizards import PoliticianProfileWizard, PoliticianProfileAppearanceWizard, CouncilEditWizard
from backoffice.wizards import PartyContactWizard, AddElectionInstanceWizard, ElectionSetupWizard2, EditElectionInstanceWizard
from backoffice.wizards import ElectionPartyEditWizard, AddCandidateWizard, AnswerQuestion, PoliticianProfileGoalWizard

from backoffice.functions import check_permissions

from questions.functions import get_question_count

def permission_denied(request):
    if not request.user.is_authenticated():
        return redirect('fo.login')
    return render_to_response('backoffice/permission_denied.html', {'next': request.GET.get('next', None)}, context_instance=RequestContext(request))

@login_required
def redirect_view(request):
    if request.user.is_staff:
        return redirect('bo.election_event')
    elif request.user.profile.type == 'council_admin':
        election_instance = request.user.councils.all()[0].election_instances.all()[0]
        return redirect('bo.election_instance_view', id=election_instance.id )
    elif request.user.profile.type == 'party_admin':
        election_instance_party = request.user.parties.all().order_by('-id')[0].election_instance_parties.all()[0]
        return redirect('bo.election_party_view', id=election_instance_party.id)
    elif request.user.profile.type == 'candidate':
        election_instance_party = request.user.elections.all().order_by('-id')[0].election_party_instance
        return redirect('bo.politician_welcome', eip_id=election_instance_party.id)
    else:
        raise PermissionDeniedException()

@party_admin_required
def party_contact_wizard(request, id, user_id=None):
    check_permissions(request, id, 'party_admin')
    if user_id is None:
        if not (request.user.profile is None or request.user.profile.type != 'party_admin'):
            user_id = request.user.id
        elif request.user.is_staff or (request.user.profile and request.user.profile.type == 'council_admin'):
            user_id is None
        else:
            raise PermissionDeniedException()

    return PartyContactWizard(user_id=user_id, eip_id=id)(request)

@party_admin_required
def party_contact_wizard_done(request, id):
    check_permissions(request,id, 'party_admin')
    eip = get_object_or_404(ElectionInstanceParty, pk=id)

    return render_to_response('backoffice/wizard/partycontact/done.html', {'eip': eip, 'instance': eip.election_instance}, context_instance=RequestContext(request))


@council_admin_required
def election_instance_view(request, id):
    check_permissions(request,id, 'council_admin')
    instance = get_object_or_404(ElectionInstance, pk=id)
    credit_left = instance.council.credit_left()
    pos_credit_left = credit_left
    if credit_left < 0:
        pos_credit_left = abs(credit_left)

    allocated = instance.council.credit - credit_left
    enough = True
    if credit_left < 0:
        enough = False

    return render_to_response('backoffice/election_instance_view.html', {'pos_credit_left':pos_credit_left,'credit_left':credit_left,'allocated':allocated,'enough':enough,'instance': instance}, context_instance=RequestContext(request))

@council_admin_required
def election_instance_export_view(request, id):
    """
    Export a csv file containing an overview of parties for this election instance
    """

    check_permissions(request, id, 'council_admin')
    instance = get_object_or_404(ElectionInstance, pk=id)

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=partijen.csv'
    writer = csv.writer(response)

    writer.writerow(['positie', 'partij', 'contactpersoon voornaam', 'contactperson achternaam', 'contactpersoon-email', 'telefoon', 'partij-email'])
    for i, eip in instance.party_dict().items():
        if eip:
            contact = eip.party.contacts.all()[0]
            writer.writerow([i, eip.party, contact.profile.first_name, contact.profile.last_name, contact.email,  eip.party.telephone, eip.party.email])

    return response

@staff_required
def question_overview(request, election_instance_id):
    instance = get_object_or_404(ElectionInstance, pk=election_instance_id)

    questions = instance.questions.filter(question_type__in=BACKOFFICE_QUESTION_TYPES).order_by('electioninstancequestion__position')

    return render_to_response('backoffice/question_overview.html', {'instance': instance, 'questions': questions}, context_instance=RequestContext(request))

@council_admin_required
def election_instance_shrink(request, id):
    check_permissions(request,id, 'council_admin')
    instance = get_object_or_404(ElectionInstance, pk=id)
    if instance.num_lists is None:
        instance.num_lists = 0
    else:
        instance.num_lists -= 1
    instance.save()
    return redirect('bo.election_instance_view', id=id)

@council_admin_required
def election_instance_grow(request, id):
    check_permissions(request,id, 'council_admin')
    instance = get_object_or_404(ElectionInstance, pk=id)
    if instance.num_lists is None:
        instance.num_lists = 0
    instance.num_lists += 1
    instance.save()
    return redirect('bo.election_instance_view', id=id)

@party_admin_required
def election_party_view(request, id):
    check_permissions(request,id, 'party_admin')
    eip = get_object_or_404(ElectionInstanceParty, pk=id)
    return render_to_response('backoffice/election_party_view.html', {'instance': eip.election_instance, 'eip': eip}, context_instance=RequestContext(request))

@council_admin_required
def election_party_create(request, id, position):
    check_permissions(request,id, 'council_admin')
    instance = get_object_or_404(ElectionInstance, pk=id)
    #Fix for double submit exception
    try:
        eip = ElectionInstanceParty.objects.get(position=position, election_instance__id=id)
    except ElectionInstanceParty.DoesNotExist:
        eip = None

    if eip:
        if request.POST.get('skip', None) is not None:
            return redirect('bo.election_instance_view', id=id)
        return redirect('bo.election_party_edit', id=eip.id)

    wizard = AddElectionPartyWizard(instance, position)
    return wizard(request)

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

@party_admin_required
def election_statistics_view(request, id):
    check_permissions(request,id, 'party_admin')

    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("""
SELECT
	  g.name as partijNaam
	, f.list_length as lijstLengte
	, e.aantalKandidatenAangemaakt
	, e.aantalKandidatenAlEensIngelogd
	, e.aantalKandidatenKlaar
FROM
	 elections_electioninstanceparty f
	LEFT OUTER JOIN  (
			SELECT 
				election_party_instance_id
				, COUNT(candidate_id) AS aantalKandidatenAangemaakt
				, SUM(is_active) AS aantalKandidatenAlEensIngelogd
				, SUM(heeftVragenIngevuld) AS aantalKandidatenKlaar
			FROM
				(
					SELECT 
						  a.election_party_instance_id
						, a.candidate_id
						, b.is_active
						, d.heeftVragenIngevuld
					FROM
						elections_candidacy a
						LEFT OUTER JOIN (SELECT id, is_active FROM auth_user) b ON (b.id = a.candidate_id)
						LEFT OUTER JOIN (SELECT id, user_id FROM political_profiles_politicianprofile) c ON (a.candidate_id = c.user_id)
						LEFT OUTER JOIN (
							SELECT candidacy_id, COUNT(id) > 0 as heeftVragenIngevuld FROM elections_candidacy_answers GROUP BY candidacy_id
						) d ON (c.id = d.candidacy_id)
				) h
			GROUP BY
				election_party_instance_id
	) e  ON (e.election_party_instance_id = f.id)
	LEFT OUTER JOIN elections_party g ON (e.election_party_instance_id = g.id)
WHERE f.election_instance_id = %s
    """, [id]);
    statistics = dictfetchall(cursor)
    eip = get_object_or_404(ElectionInstanceParty, pk=id)
    return render_to_response('backoffice/statistics.html', {'instance': eip.election_instance, 'eip': eip, 'statistics': statistics}, context_instance=RequestContext(request))
    

@party_admin_required
def election_party_edit(request, id):
    check_permissions(request,id, 'party_admin')
    eip = get_object_or_404(ElectionInstanceParty, pk=id)
    wizard = ElectionPartyEditWizard(eip)
    return wizard(request)

@party_admin_required
def election_party_up(request, id):
    check_permissions(request,id, 'party_admin')
    eip = get_object_or_404(ElectionInstanceParty, pk=id)
    eip.move_up()
    return redirect('bo.election_instance_view', id=eip.election_instance.id)

@party_admin_required
def election_party_down(request, id):
    check_permissions(request,id, 'party_admin')
    eip = get_object_or_404(ElectionInstanceParty, pk=id)
    eip.move_down()
    return redirect('bo.election_instance_view', id=eip.election_instance.id)

@party_admin_required
def election_party_shrink(request, id):
    check_permissions(request,id, 'party_admin')
    eip = get_object_or_404(ElectionInstanceParty, pk=id)
    if eip.list_length is None:
        eip.list_length = 0
    else:
        eip.list_length -= 1
    eip.save()
    return redirect('bo.election_party_view', id=id)

@party_admin_required
def election_party_grow(request, id):
    check_permissions(request,id, 'party_admin')
    eip = get_object_or_404(ElectionInstanceParty, pk=id)
    if eip.list_length is None:
        eip.list_length = 0
    eip.list_length += 1
    eip.save()
    return redirect('bo.election_party_view', id=id)

@party_admin_required
def candidate_up(request, id):
    can = get_object_or_404(Candidacy, pk=id)
    check_permissions(request,can.election_party_instance.id, 'party_admin')
    can.move_up()
    return redirect('bo.election_party_view', id=can.election_party_instance.id)

@party_admin_required
def candidate_down(request, id):
    can = get_object_or_404(Candidacy, pk=id)
    check_permissions(request,can.election_party_instance.id, 'party_admin')
    can.move_down()
    return redirect('bo.election_party_view', id=can.election_party_instance.id)

@party_admin_required
def election_party_add_candidate(request, id, pos):
    check_permissions(request,id, 'party_admin')
    if Candidacy.objects.filter(election_party_instance__pk=id, position=pos).count() != 0:
        request.user.message_set.create(message=ugettext('U heeft al iemand op positie %(pos)s uitgenodigd.') % {'pos': pos})
        return redirect('bo.election_party_view', id=id)
    return AddCandidateWizard(id, pos)(request)

@staff_required
def election_event(request):
    election_instances = ElectionInstance.objects.filter(election_event__pk=ELECTION_EVENT_ID).order_by('name')
    return render_to_response('backoffice/election_event_view.html', {'election_instances': election_instances,},
                              context_instance=RequestContext(request))


@staff_required
def add_election_instance(request):
    wizard = AddElectionInstanceWizard()
    return wizard(request)

@staff_required
def edit_election_instance(request, id):
    wizard = EditElectionInstanceWizard(id)
    return wizard(request)


@staff_required
def candidate_edit(request, id):
    candidacy = get_object_or_404(Candidacy, pk=id)
    if candidacy.candidate.is_active:
        request.user.message_set.create(message=ugettext('De kandidaat die u wilt wijzigen heeft zijn/haar account al geactiveerd.'))
        return redirect('bo.election_party_view', id=candidacy.election_party_instance.id)

    FormClass = get_profile_forms('candidate', 'edit')[0]

    if request.method == 'POST':
        form = FormClass(user=candidacy.candidate, data=request.POST)

        if form.is_valid():
            candidacy.candidate.email = form.cleaned_data['email']
            candidacy.candidate.profile.first_name = form.cleaned_data['name']['first_name']
            candidacy.candidate.profile.middle_name = form.cleaned_data['name']['middle_name']
            candidacy.candidate.profile.last_name = form.cleaned_data['name']['last_name']
            candidacy.candidate.profile.gender = form.cleaned_data['gender']
            candidacy.candidate.save()
            candidacy.candidate.profile.save()

            request.user.message_set.create(message=ugettext('De kandidaat is gewijzigd.'))
            return redirect('bo.election_party_view', id=candidacy.election_party_instance.id)
    else:
        initial = {
            'name': {
                'first_name': candidacy.candidate.profile.first_name,
                'middle_name': candidacy.candidate.profile.middle_name,
                'last_name': candidacy.candidate.profile.last_name,
            },
            'email': candidacy.candidate.email,
            'gender': candidacy.candidate.profile.gender,
        }
        form = FormClass(user=candidacy.candidate, initial=initial)

    return render_to_response('backoffice/edit_candidate.html', {'form': form, 'candidacy': candidacy}, context_instance=RequestContext(request))

@council_admin_required
def election_setup(request, election_instance_id, user_id=None):
    '''
    Election setup wizard.
    @param int election_instance_id
    @param int user_id

    Both parameters are required. It's obvious what they mean.
    '''
    check_permissions(request,election_instance_id, 'council_admin')
    if user_id is None:
        user_id = request.user.id
        if not request.user.profile or request.user.profile.type != 'council_admin':
            raise PermissionDeniedException('You are not the correct user')

    return ElectionSetupWizard2(election_instance_id=election_instance_id, user_id=user_id)(request)

@council_admin_required
def election_setup_done(request, election_instance_id):
    check_permissions(request,election_instance_id, 'council_admin')
    election_instance = get_object_or_404(ElectionInstance, pk=election_instance_id)
    return render_to_response('backoffice/wizard/election_setup/done.html', {'instance': election_instance}, context_instance=RequestContext(request))

@candidate_required
def politician_welcome(request, eip_id):
    check_permissions(request, eip_id, 'candidate')
    election_instance_party = get_object_or_404(ElectionInstanceParty, pk=eip_id)
    if not request.user.profile or request.user.profile.type != 'candidate':
        raise PermissionDeniedException('Geen toegang met de huidige account')
    else:
        user = get_object_or_404(election_instance_party.candidates, candidate=request.user).candidate

    return render_to_response('backoffice/wizard/politician_profile/welcome.html',
                              {'user_id': user.id,
                              'politician': user.profile,
                              'election_instance': election_instance_party.election_instance,
                              'eip_id': eip_id,
                              'questions': range(0, get_question_count(eip_id)),
                              },
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_setup(request, eip_id, user_id):
    check_permissions(request, eip_id, 'candidate')
    return PoliticianProfileWizard(user_id=user_id, eip_id=eip_id)(request)

@candidate_required
def politician_profile_setup_done(request, eip_id, user_id):
    check_permissions(request, eip_id, 'candidate')
    return render_to_response('backoffice/wizard/politician_profile/done.html',
                              {'user_id': user_id,
                              'eip_id': eip_id,
                              'questions': range(0, get_question_count(eip_id)),
                              },
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_interest(request, eip_id, user_id):
    check_permissions(request, eip_id, 'candidate')
    user = get_object_or_404(User, pk=user_id)
    interests = user.profile.interests.all()
    return render_to_response('backoffice/wizard/politician_profile/interest.html',
                              {'user_id': user_id, 'interests': interests,
                              'eip_id': eip_id,
                              'questions': range(0, get_question_count(eip_id)),
                              },
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_interest_delete(request, interest_id, eip_id, user_id):
    check_permissions(request, eip_id, 'candidate')
    user = get_object_or_404(User, pk=user_id)
    try:
        interest = user.profile.interests.get(pk=interest_id)
        interest.delete()
    except ObjectDoesNotExist:
        pass
    return redirect('backoffice.views.politician_profile_interest', eip_id=eip_id, user_id = user_id)

@candidate_required
def politician_profile_interest_wizard(request, eip_id, user_id, interest_id=None):
    check_permissions(request, eip_id, 'candidate')
    return PoliticianProfileInterestWizard(user_id=user_id, eip_id=eip_id, interest_id=interest_id)(request)

@candidate_required
def politician_profile_work(request, eip_id, user_id):
    check_permissions(request, eip_id, 'candidate')
    user = get_object_or_404(User, pk=user_id)
    work = user.profile.work.all()
    return render_to_response('backoffice/wizard/politician_profile/work.html',
                              {'user_id': user_id, 'work': work,
                              'eip_id': eip_id,
                              'questions': range(0, get_question_count(eip_id)),
                              },
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_work_delete(request, work_id, eip_id, user_id):
    check_permissions(request, eip_id, 'candidate')
    user = get_object_or_404(User, pk=user_id)
    try:
        work = user.profile.work.get(pk=work_id)
        work.delete()
    except ObjectDoesNotExist:
        pass
    return redirect('backoffice.views.politician_profile_work', eip_id=eip_id, user_id=user_id)

@candidate_required
def politician_profile_work_wizard(request, eip_id, user_id, work_id=None):
    check_permissions(request, eip_id, 'candidate')
    return PoliticianProfileWorkWizard(user_id=user_id, eip_id=eip_id, work_id=work_id)(request)

@candidate_required
def politician_profile_goal(request, eip_id, user_id):
    check_permissions(request, eip_id, 'candidate')
    user = get_object_or_404(User, pk=user_id)
    goals = user.profile.goals.all()
    return render_to_response('backoffice/wizard/politician_profile/goals.html',
                              {'user_id': user_id, 'goals': goals,
                              'eip_id': eip_id,
                              'questions': range(0, get_question_count(eip_id)),
                              },
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_goal_delete(request, goal_id, eip_id, user_id):
    check_permissions(request, eip_id, 'candidate')
    user = get_object_or_404(User, pk=user_id)
    try:
        goal = user.profile.goals.get(pk=goal_id)
        goal.delete()
    except ObjectDoesNotExist:
        pass
    return redirect('backoffice.views.politician_profile_goal', eip_id=eip_id, user_id=user_id)

@candidate_required
def politician_profile_goal_wizard(request, eip_id, user_id, goal_id=None):
    check_permissions(request, eip_id, 'candidate')
    return PoliticianProfileGoalWizard(user_id=user_id, eip_id=eip_id, goal_id=goal_id)(request)

@candidate_required
def politician_profile_political(request, eip_id, user_id):
    check_permissions(request, eip_id, 'candidate')
    user = get_object_or_404(User, pk=user_id)
    political = user.profile.political.all()
    return render_to_response('backoffice/wizard/politician_profile/political.html',
                              {'user_id': user_id, 'political': political,
                              'eip_id': eip_id,
                              'questions': range(0, get_question_count(eip_id)),
                              },
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_political_delete(request, political_id, eip_id, user_id):
    check_permissions(request, eip_id, 'candidate')
    user = get_object_or_404(User, pk=user_id)
    try:
        political = user.profile.political.get(pk=political_id)
        political.delete()
    except ObjectDoesNotExist:
        pass
    return redirect('backoffice.views.politician_profile_political', eip_id=eip_id, user_id=user_id)

@candidate_required
def politician_profile_political_wizard(request, eip_id, user_id, political_id=None):
    check_permissions(request, eip_id, 'candidate')
    return PoliticianProfilePoliticalWizard(user_id=user_id, eip_id=eip_id, political_id=political_id)(request)

@candidate_required
def politician_profile_education(request, eip_id, user_id):
    check_permissions(request, eip_id, 'candidate')
    user = get_object_or_404(User, pk=user_id)
    education = user.profile.education.all()
    return render_to_response('backoffice/wizard/politician_profile/education.html',
                              {'user_id': user_id, 'education': education,
                              'eip_id': eip_id,
                              'questions': range(0, get_question_count(eip_id)),
                              },
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_education_delete(request, education_id, eip_id, user_id):
    check_permissions(request, eip_id, 'candidate')
    user = get_object_or_404(User, pk=user_id)
    try:
        education = user.profile.education.get(pk=education_id)
        education.delete()
    except ObjectDoesNotExist:
        pass
    return redirect('backoffice.views.politician_profile_education', eip_id=eip_id, user_id=user_id)

@candidate_required
def politician_profile_education_wizard(request, eip_id, user_id, education_id=None):
    check_permissions(request, eip_id, 'candidate')
    return PoliticianProfileEducationWizard(user_id=user_id, eip_id=eip_id, education_id=education_id)(request)

@candidate_required
def politician_profile_appearance(request, eip_id, user_id):
    check_permissions(request, eip_id, 'candidate')
    user = get_object_or_404(User, pk=user_id)
    appearances = user.profile.appearances.all()
    return render_to_response('backoffice/wizard/politician_profile/appearances.html',
                              {'user_id': user_id, 'appearances': appearances,
                              'eip_id': eip_id,
                              'questions': range(0, get_question_count(eip_id)),
                              },
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_appearance_delete(request, appearance_id, eip_id, user_id):
    check_permissions(request, eip_id, 'candidate')
    user = get_object_or_404(User, pk=user_id)
    try:
        appearance = user.profile.appearances.get(pk=appearance_id)
        appearance.delete()
    except ObjectDoesNotExist:
        pass
    return redirect('backoffice.views.politician_profile_appearance', eip_id=eip_id, user_id=user_id)

@candidate_required
def politician_profile_appearance_wizard(request, eip_id, user_id, appearance_id=None):
    check_permissions(request, eip_id, 'candidate')
    return PoliticianProfileAppearanceWizard(user_id=user_id, eip_id=eip_id, appearance_id=appearance_id)(request)

@candidate_required
def politician_profile_link(request, eip_id, user_id):
    check_permissions(request, eip_id, 'candidate')
    user = get_object_or_404(User, pk=user_id)
    links = user.profile.links.all()

    return render_to_response('backoffice/wizard/politician_profile/links.html',
                              {'user_id': user_id, 'links': links,
                              'eip_id': eip_id,
                              'questions': range(0, get_question_count(eip_id)),
                              },
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_link_delete(request, link_id, eip_id, user_id):
    check_permissions(request, eip_id, 'candidate')
    user = get_object_or_404(User, pk=user_id)
    try:
        link = user.profile.links.get(pk=link_id)
        link.delete()
    except ObjectDoesNotExist:
        pass
    return redirect('backoffice.views.politician_profile_link', eip_id=eip_id, user_id=user_id)

@candidate_required
def politician_profile_link_wizard(request, eip_id, user_id, link_id=None):
    check_permissions(request, eip_id, 'candidate')
    return PoliticianProfileLinkWizard(user_id=user_id, eip_id=eip_id, link_id=link_id)(request)

@candidate_required
def politician_profile_connection(request, eip_id, user_id):
    check_permissions(request, eip_id, 'candidate')
    user = get_object_or_404(User, pk=user_id)
    connections = user.profile.connections.all()

    return render_to_response('backoffice/wizard/politician_profile/connections.html',
                              {'user_id': user_id, 'connections': connections,
                              'eip_id': eip_id,
                              'questions': range(0, get_question_count(eip_id)),
                              },
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_connection_delete(request, connection_id, eip_id, user_id):
    check_permissions(request, eip_id, 'candidate')
    user = get_object_or_404(User, pk=user_id)
    try:
        connection = user.profile.connections.get(pk=connection_id)
        connection.delete()
    except ObjectDoesNotExist:
        pass
    return redirect('backoffice.views.politician_profile_connection', eip_id=eip_id, user_id=user_id)

@candidate_required
def politician_profile_connection_wizard(request, eip_id, user_id, connection_id=None):
    check_permissions(request, eip_id, 'candidate')
    return PoliticianProfileConnectionWizard(user_id=user_id, eip_id=eip_id, connection_id=connection_id)(request)

@party_admin_required
def csv_import_candidates_step1(request, ep_id):
    check_permissions(request, ep_id, 'party_admin')
    eip = get_object_or_404(ElectionInstanceParty, pk=ep_id)
    return render_to_response('backoffice/csv_candidates_1.html', {'ep_id':ep_id, 'instance':eip.election_instance}, context_instance=RequestContext(request))

@party_admin_required
def csv_import_candidates_step2(request, ep_id, error = False):
    check_permissions(request, ep_id, 'party_admin')
    if request.method == 'POST':
        form = CsvUploadForm(request.POST, request.FILES)
        if form.is_valid():
            #Save file in tmp dir
            file = form.files['file']
            filename = str(time.time()) + '.csv' #about 1000 unique filenames per second?
            destination = open(settings.TMP_ROOT + '/' + filename, 'wb+')

            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()
            request.session['csv_candidate_filename'] = filename
            return redirect('bo.csv_candidates_step3', ep_id)

    else:
        form = CsvUploadForm()
    eip = get_object_or_404(ElectionInstanceParty, pk=ep_id)
    forms = dict({'csv_upload': form})
    return render_to_response('backoffice/csv_candidates_2.html', {'forms':forms, 'error':error, 'ep_id':ep_id, 'instance':eip.election_instance }, context_instance=RequestContext(request))

@party_admin_required
@transaction.commit_manually
def csv_import_candidates_step3(request, ep_id):
    check_permissions(request, ep_id, 'party_admin')
    eip_obj = get_object_or_404(ElectionInstanceParty, pk=ep_id)
    try:
        positions = Candidacy.objects.filter(election_party_instance=eip_obj).values_list('position', flat=True)
        candidate_emails = Candidacy.objects.filter(election_party_instance=eip_obj).values_list('candidate__email', flat=True)
        candidates = functions.get_candidates_from_csv(request.session, positions, candidate_emails)
    except:

        path = settings.TMP_ROOT + '/'
        if not os.path.isdir(path):
            os.remove(path + request.session['csv_candidate_filename'])
        request.session['csv_candidate_filename'] = ''
        return redirect('bo.csv_candidates_step2', ep_id=ep_id, error='true')

    if request.method == 'POST':
        form = CsvConfirmForm(request.POST)
        if form.is_valid():
            for candidate in candidates.values():
                try:
                    #Store data
                    tmp_data = {
                        'first_name': candidate['first_name'],
                        'middle_name': candidate['middle_name'],
                        'last_name': candidate['last_name'],
                        'initials': candidate['initials'],
                        'email': candidate['email'],
                        'gender': candidate['gender'],
                    }
                    created, candidate_obj = create_profile('candidate', tmp_data)

                    if candidate_obj is None:
                        continue

                    #Link candidate to party
                    Candidacy.objects.create(
                        election_party_instance = eip_obj,
                        candidate = candidate_obj.user,
                        position = candidate['position'],
                    )

                    #Create invitation TODO: view and text etc.
                    templates = profile_invite_email_templates('candidate')
                    Invitation.create(
                        user_from = request.user,
                        user_to = candidate_obj.user,
                        view = reverse('bo.politician_welcome', kwargs={'eip_id': eip_obj.id}),
                        text = '<p>Wiekiesjij is de voorkeurstemhulp van Nederland. Middels het beantwoorden een vijftiental vragen zullen bezoekers gekoppeld worden aan hun favoriete kandidaten. Middels de informatie die u hier invult zullen wij daarnaast in staat zijn om de bezoekers de mogelijkheid te bieden om te browsen tussen alle kandidaten, de partijen en is het mogelijk om de uitgebreide profielen van alle politici te bekijken.</p>',
                        subject = ugettext('Invitation Wiekiesjij'),
                        html_template = templates['html'],
                        plain_template = templates['plain'],
                    )

                    position = int(candidate['position'])
                    if position > eip_obj.list_length:
                        eip_obj.list_length = position
                        eip_obj.save()

                except:
                    transaction.rollback()
                    raise

            transaction.commit()
            os.remove(settings.TMP_ROOT + '/' + request.session['csv_candidate_filename'])
            request.session['csv_candidate_filename'] = ''
            return redirect('bo.election_party_view', id=ep_id)
    else:
        form = CsvConfirmForm()
    eip = get_object_or_404(ElectionInstanceParty, pk=ep_id)
    forms = dict({'csv_confirm': form})
    return render_to_response('backoffice/csv_candidates_3.html', {'candidates':candidates, 'forms':forms, 'ep_id':ep_id, 'instance':eip.election_instance}, context_instance=RequestContext(request))

@council_admin_required
def csv_import_parties_step1(request, ei_id):
    check_permissions(request, ei_id, 'council_admin')
    ei_obj = get_object_or_404(ElectionInstance, pk=ei_id)
    return render_to_response('backoffice/csv_parties_1.html', {'ei_id': ei_id, 'instance':ei_obj}, context_instance=RequestContext(request))

@council_admin_required
def csv_import_parties_step2(request, ei_id, error = False):
    check_permissions(request, ei_id, 'council_admin')
    if request.method == 'POST':
        form = CsvUploadForm(request.POST, request.FILES)
        if form.is_valid():
            #Save file in tmp dir
            file = form.files['file']
            filename = str(time.time()) + '.csv' #about 1000 unique filenames per second?
            destination = open(settings.TMP_ROOT + '/' + filename, 'wb+')

            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()
            request.session['csv_party_filename'] = filename
            return redirect('bo.csv_parties_step3', ei_id = ei_id)

    else:
        form = CsvUploadForm()
    ei_obj = get_object_or_404(ElectionInstance, pk=ei_id)
    forms = dict({'csv_upload': form})
    return render_to_response('backoffice/csv_parties_2.html', {'forms':forms, 'error': error, 'ei_id': ei_id, 'instance':ei_obj}, context_instance=RequestContext(request))

@council_admin_required
@transaction.commit_manually
def csv_import_parties_step3(request, ei_id):
    check_permissions(request, ei_id, 'council_admin')
    ei_obj = get_object_or_404(ElectionInstance, pk=ei_id)
    try:
        lists = ElectionInstanceParty.objects.filter(election_instance=ei_obj).values_list('position', flat=True)
        parties = functions.get_parties_from_csv(request.session, lists)
    except:
        path = settings.TMP_ROOT + '/'
        if not os.path.isdir(path):
            os.remove(path + request.session['csv_party_filename'])
        request.session['csv_party_filename'] = ''
        return redirect('bo.csv_parties_step2', ei_id = ei_id, error='true')

    if request.method == 'POST':
        form = CsvConfirmForm(request.POST)
        if form.is_valid():

            council = ei_obj.council
            region = council.region
            level = council.level

            for party in parties.values():
                try:
                    #Store data
                    tmp_data = {
                        'first_name': party['contact_first_name'],
                        'middle_name': party['contact_middle_name'],
                        'last_name': party['contact_last_name'],
                        'email': party['contact_email'],
                        'gender': party['contact_gender'],
                    }
                    created, contact = create_profile('party_admin', tmp_data)

                    if contact is None:
                        continue

                    party_obj = Party.objects.create(
                        region = region,
                        level = level,
                        name = party['name'],
                        abbreviation = party['abbreviation'],
                    )

                    eip_obj = ElectionInstanceParty.objects.create(
                        election_instance = ei_obj,
                        party = party_obj,
                        position = unicode(party['list']),
                        list_length = 10, #TODO, maybe add in CSV
                    )

                    party_obj.contacts.add(contact.user)
                    party_obj.save()

                    #Create invitation
                    templates = profile_invite_email_templates('party_admin')
                    Invitation.create(
                        user_from = request.user,
                        user_to = contact.user,
                        view=reverse('bo.party_contact_wizard', kwargs={'id': eip_obj.pk}),
                        text='<p>U bent aangekomen op de beheerderpagina van Wiekiesjij. Om Wiekiesjij gereed te maken voor uw partij volgen er nu een aantal schermen waarin u informatie kunt achterlaten. Wanneer deze informatie is ingevuld zullen we overgaan tot het uitnodigen van de kandidaten van uw partij.</p><p>We beginnen met het instellen van een wachtwoord voor Wiekiesjij door op <strong>Accepteer uitnodiging</strong> te klikken. Heeft u al eens eerder gebruik gemaakt van Wiekiesjij, drukt u dan op <strong>Ik heb al een account</strong>.</p><p>Om het gereedmaken van Wiekiesjij zo gemakkelijk mogelijk te laten verlopen hebben we een snelle start [link] handleiding [/link] beschikbaar gesteld die u kunt raadplegen.</p>',
                        subject = ugettext('Invitation Wiekiesjij'),
                        html_template = templates['html'],
                        plain_template = templates['plain'],
                    )

                    max_list = int(party['list'])
                    if max_list > ei_obj.num_lists:
                        ei_obj.num_lists = max_list
                        ei_obj.save()

                except:
                    transaction.rollback()
                    raise
                else:
                    transaction.commit()

            os.remove(settings.TMP_ROOT + '/' + request.session['csv_party_filename'])
            request.session['csv_party_filename'] = ''
            return redirect('bo.election_instance_view', id=ei_id)
    else:
        form = CsvConfirmForm()
    ei_obj = get_object_or_404(ElectionInstance, id=ei_id)
    forms = dict({'csv_confirm': form})
    return render_to_response('backoffice/csv_parties_3.html', {'parties':parties, 'forms':forms, 'ei_id': ei_id, 'instance':ei_obj}, context_instance=RequestContext(request))

@council_admin_required
def council_edit(request, id):
    '''
    Council edit wizard.
    @param int election_instance_id
    @param int user_id

    Both parameters are required. It's obvious what they mean.
    '''
    check_permissions(request, id, 'council_admin')
    election_instance = get_object_or_404(ElectionInstance, pk=id)
    return CouncilEditWizard(election_instance)(request)


@candidate_required
def answer_question(request, election_instance_party_id, user_id=None):
    '''
        AnswerQuestion - wizard.
        @param int election_instance_party_id - ElectionInstanceParty id
        @param int user_id User (Candidate=PoliticalProfile) id
    '''
    check_permissions(request, election_instance_party_id, 'candidate')
    return AnswerQuestion(election_instance_party_id=election_instance_party_id, user_id=user_id)(request)

@candidate_required
def answer_question_done(request, election_instance_party_id, user_id):
    '''
        answer_question thanks page.
    '''
    check_permissions(request, election_instance_party_id, 'candidate')

    user = get_object_or_404(User, pk=user_id)

    message = None

    if request.method == 'POST':
        form = AgreeForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user.profile.hns_dev = data['hns_dev']
            user.profile.science = data['science']

            user.profile.save()

            message = _('Your preference has been saved')
    else:
        initial = {
            'hns_dev': user.profile.hns_dev,
            'science': user.profile.science,
        }
        form = AgreeForm(initial=initial)

    return render_to_response('backoffice/wizard/question/answer_add/done.html', {
                                'questions': range(0, get_question_count(election_instance_party_id)),
                                'eip_id': election_instance_party_id,
                                'user_id': user_id,
                                'form': form,
                                'message': message,
                            },
                            context_instance=RequestContext(request))

def view_profile(request):
    """
        View a user profile
    """
    if request.user.profile:
        return render_to_response(get_profile_template(request.user.profile.type, 'backoffice_profile'), {}, context_instance=RequestContext(request))
    return redirect('/')
