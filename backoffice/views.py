#!/usr/env python
#-*- coding: utf-8 -*-
#
#Copyright 2009 Accepte. All Rights Reserved.

import os
import time

from django.db import transaction
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404

from elections.settings import ELECTION_EVENT_ID
from elections.models import ElectionInstance, ElectionInstanceParty, Party, Candidacy
from elections.functions import create_profile, profile_invite_email_templates, get_profile_template

from invitations.models import Invitation

from political_profiles import functions
from political_profiles.forms import CsvUploadForm, CsvConfirmForm


from backoffice.decorators import staff_required, candidate_required, council_admin_required , party_admin_required

from backoffice.wizards import AddElectionPartyWizard, PoliticianProfileInterestWizard, PoliticianProfileWorkWizard
from backoffice.wizards import PoliticianProfileConnectionWizard, PoliticianProfilePoliticalWizard, PoliticianProfileEducationWizard, PoliticianProfileLinkWizard
from backoffice.wizards import PoliticianProfileWizard, PoliticianProfileAppearanceWizard, CouncilEditWizard
from backoffice.wizards import PartyContactWizard, AddElectionInstanceWizard, ElectionSetupWizard2, EditElectionInstanceWizard
from backoffice.wizards import ElectionPartyEditWizard, AddCandidateWizard, AnswerQuestion

from utils.exceptions import PermissionDeniedException

from questions.forms import AnswerQuestionForm, SelectQuestionForm
from questions.models import Question

def permission_denied(request):
    return render_to_response('backoffice/permission_denied.html', {'next': request.GET.get('next', None)}, context_instance=RequestContext(request))
    
@login_required
def redirect_view(request):
    if request.user.is_staff:
        return redirect('bo.election_event')
    elif request.user.profile.type == 'council_admin':
        election_instance = request.user.councils.all()[0].election_instances.all()[0]
        return redirect('bo.election_instance_view', id=election_instance.id )
    elif request.user.profile.type == 'party_admin':
        election_instance_party = request.user.parties.all()[0].election_instance_parties.all()[0]
        return redirect('bo.election_party_view', id=election_instance_party.id)
    elif request.user.profile.type == 'candidate':
        election_instance_party = request.user.elections.all()[0].election_party_instance
        print election_instance_party.election_instance.id
        return redirect('bo.politician_welcome', election_instance_id=election_instance_party.election_instance.id)
    else:
        raise PermissionDeniedException()

@party_admin_required
def party_contact_wizard(request, id, user_id=None):
    if user_id is None:
        if request.user.profile is None or request.user.profile.type != 'party_admin':
            raise PermissionDeniedException()
        user_id = request.user.id
        
    return PartyContactWizard(user_id=user_id, eip_id=id)(request)

@party_admin_required
def party_contact_wizard_done(request, id):
    eip = get_object_or_404(ElectionInstanceParty, pk=id)
    
    return render_to_response('backoffice/wizard/partycontact/done.html', {'eip': eip, 'instance': eip.election_instance}, context_instance=RequestContext(request))
    
    
@council_admin_required
def election_instance_view(request, id):
    instance = get_object_or_404(ElectionInstance, pk=id)
    return render_to_response('backoffice/election_instance_view.html', {'instance': instance}, context_instance=RequestContext(request))

@council_admin_required
def election_instance_shrink(request, id):
    instance = get_object_or_404(ElectionInstance, pk=id)
    if instance.num_lists is None:
        instance.num_lists = 0
    else:
        instance.num_lists -= 1
    instance.save()
    return redirect('bo.election_instance_view', id=id)

@council_admin_required
def election_instance_grow(request, id):
    instance = get_object_or_404(ElectionInstance, pk=id)
    if instance.num_lists is None:
        instance.num_lists = 0
    instance.num_lists += 1
    instance.save()
    return redirect('bo.election_instance_view', id=id)

@party_admin_required
def election_party_view(request, id):
    eip = get_object_or_404(ElectionInstanceParty, pk=id)
    return render_to_response('backoffice/election_party_view.html', {'instance': eip.election_instance, 'eip': eip}, context_instance=RequestContext(request))

@council_admin_required
def election_party_create(request, id, position):
    instance = get_object_or_404(ElectionInstance, pk=id)
    wizard = AddElectionPartyWizard(instance, position)
    return wizard(request)

@party_admin_required
def election_party_edit(request, id):
    eip = get_object_or_404(ElectionInstanceParty, pk=id)
    wizard = ElectionPartyEditWizard(eip)
    return wizard(request)

@party_admin_required
def election_party_up(request, id):
    eip = get_object_or_404(ElectionInstanceParty, pk=id)
    eip.move_up()
    return redirect('bo.election_instance_view', id=eip.election_instance.id)

@party_admin_required
def election_party_down(request, id):
    eip = get_object_or_404(ElectionInstanceParty, pk=id)
    eip.move_down()
    return redirect('bo.election_instance_view', id=eip.election_instance.id)

@party_admin_required
def election_party_shrink(request, id):
    eip = get_object_or_404(ElectionInstanceParty, pk=id)
    if eip.list_length is None:
        eip.list_length = 0
    else:
        eip.list_length -= 1
    eip.save()
    return redirect('bo.election_party_view', id=id)

@party_admin_required
def election_party_grow(request, id):
    eip = get_object_or_404(ElectionInstanceParty, pk=id)
    if eip.list_length is None:
        eip.list_length = 0
    eip.list_length += 1
    eip.save()
    return redirect('bo.election_party_view', id=id)

@party_admin_required
def candidate_up(request, id):
    can = get_object_or_404(Candidacy, pk=id)
    can.move_up()
    return redirect('bo.election_party_view', id=can.election_party_instance.id)

@party_admin_required
def candidate_down(request, id):
    can = get_object_or_404(Candidacy, pk=id)
    can.move_down()
    return redirect('bo.election_party_view', id=can.election_party_instance.id)

@party_admin_required
def election_party_add_candidate(request, id, pos):
    return AddCandidateWizard(id, pos)(request)

@staff_required
def election_event(request):
    election_instances = ElectionInstance.objects.filter(election_event__pk=ELECTION_EVENT_ID)
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

@council_admin_required
def election_setup(request, election_instance_id, user_id=None):
    '''
    Election setup wizard.
    @param int election_instance_id
    @param int user_id

    Both parameters are required. It's obvious what they mean.
    '''
    if user_id is None:
        user_id = request.user.id
        if not request.user.profile or request.user.profile.type != 'council_admin':
            raise Http404('You are not the correct user')

    return ElectionSetupWizard2(election_instance_id=election_instance_id, user_id=user_id)(request)

@council_admin_required
def election_setup_done(request, election_instance_id):
    election_instance = get_object_or_404(ElectionInstance, pk=election_instance_id)
    return render_to_response('backoffice/wizard/election_setup/done.html', {'instance': election_instance}, context_instance=RequestContext(request))

@candidate_required
def politician_welcome(request, election_instance_id):
    user_id = request.user.id
    election_instance = get_object_or_404(ElectionInstance, pk=election_instance_id)
    return render_to_response('backoffice/wizard/politician_profile/welcome.html',
                              {'user_id': user_id,
                              'politician': request.user.profile,
                              'election_instance': election_instance,
                              'election_instance_id': election_instance_id,
                              },
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_setup(request, election_instance_id, user_id):
    return PoliticianProfileWizard(user_id=user_id, election_instance_id=election_instance_id)(request)

@candidate_required
def politician_profile_setup_done(request, election_instance_id, user_id):
    return render_to_response('backoffice/wizard/politician_profile/done.html',
                              {'user_id': user_id,
                              'election_instance_id': election_instance_id,
                              },
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_interest(request, election_instance_id, user_id):
    user = get_object_or_404(User, pk=user_id)
    interests = user.profile.interests.all()
    return render_to_response('backoffice/wizard/politician_profile/interest.html',
                              {'user_id': user_id, 'interests': interests,
                              'election_instance_id': election_instance_id,},
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_interest_delete(request, interest_id, election_instance_id, user_id):
    user = get_object_or_404(User, pk=user_id)
    interest = user.profile.interests.get(pk=interest_id)
    interest.delete()
    interests = user.profile.interests.all()
    return render_to_response('backoffice/wizard/politician_profile/interest.html',
                              {'user_id': user_id, 'interests': interests,
                              'election_instance_id': election_instance_id,},
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_interest_wizard(request, election_instance_id, user_id, interest_id=None):
    return PoliticianProfileInterestWizard(user_id=user_id, election_instance_id=election_instance_id, interest_id=interest_id)(request)

@candidate_required
def politician_profile_work(request, election_instance_id, user_id):
    user = get_object_or_404(User, pk=user_id)
    work = user.profile.work.all()
    return render_to_response('backoffice/wizard/politician_profile/work.html',
                              {'user_id': user_id, 'work': work,
                              'election_instance_id': election_instance_id,},
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_work_delete(request, work_id, election_instance_id, user_id):
    user = get_object_or_404(User, pk=user_id)
    work = user.profile.work.get(pk=work_id)
    work.delete()
    work = user.profile.work.all()
    return render_to_response('backoffice/wizard/politician_profile/work.html',
                              {'user_id': user_id, 'work': work,
                              'election_instance_id': election_instance_id,},
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_work_wizard(request, election_instance_id, user_id, work_experience_id=None):
    return PoliticianProfileWorkWizard(user_id=user_id, election_instance_id=election_instance_id, work_id=work_experience_id)(request)

@candidate_required
def politician_profile_political(request, election_instance_id, user_id):
    user = get_object_or_404(User, pk=user_id)
    political = user.profile.political.all()
    return render_to_response('backoffice/wizard/politician_profile/political.html',
                              {'user_id': user_id, 'political': political,
                              'election_instance_id': election_instance_id,},
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_political_delete(request, political_id, election_instance_id, user_id):
    user = get_object_or_404(User, pk=user_id)
    political = user.profile.political.get(pk=political_id)
    political.delete()
    political = user.profile.political.all()
    return render_to_response('backoffice/wizard/politician_profile/political.html',
                              {'user_id': user_id, 'political': political,
                              'election_instance_id': election_instance_id,},
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_political_wizard(request, election_instance_id, user_id, political_id=None):
    return PoliticianProfilePoliticalWizard(user_id=user_id, election_instance_id=election_instance_id, political_id=political_id)(request)

@candidate_required
def politician_profile_education(request, election_instance_id, user_id):
    user = get_object_or_404(User, pk=user_id)
    education = user.profile.education.all()
    return render_to_response('backoffice/wizard/politician_profile/education.html',
                              {'user_id': user_id, 'education': education,
                              'election_instance_id': election_instance_id,},
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_education_delete(request, education_id, election_instance_id, user_id):
    user = get_object_or_404(User, pk=user_id)
    education = user.profile.education.get(pk=education_id)
    education.delete()
    education = user.profile.education.all()
    return render_to_response('backoffice/wizard/politician_profile/education.html',
                              {'user_id': user_id, 'education': education,
                              'election_instance_id': election_instance_id,},
                              context_instance=RequestContext(request))
@candidate_required
def politician_profile_education_wizard(request, election_instance_id, user_id, education_id=None):
    return PoliticianProfileEducationWizard(user_id=user_id, election_instance_id=election_instance_id, education_id=education_id)(request)

@candidate_required
def politician_profile_appearance(request, election_instance_id, user_id):
    user = get_object_or_404(User, pk=user_id)
    appearances = user.profile.appearances.all()
    return render_to_response('backoffice/wizard/politician_profile/appearances.html',
                              {'user_id': user_id, 'appearances': appearances,
                              'election_instance_id': election_instance_id,},
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_appearance_delete(request, appearance_id, election_instance_id, user_id):
    user = get_object_or_404(User, pk=user_id)
    appearance = user.profile.appearances.get(pk=appearance_id)
    appearance.delete()
    appearances = user.profile.appearances.all()
    return render_to_response('backoffice/wizard/politician_profile/appearances.html',
                              {'user_id': user_id, 'appearances': appearances,
                              'election_instance_id': election_instance_id,},
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_appearance_wizard(request, election_instance_id, user_id, appearance_id=None):
    return PoliticianProfileAppearanceWizard(user_id=user_id, election_instance_id=election_instance_id, appearance_id=appearance_id)(request)
    #return PoliticianProfileAppearanceWizard()(request, *args, **kwargs)

@candidate_required
def politician_profile_link(request, election_instance_id, user_id):
    user = get_object_or_404(User, pk=user_id)
    links = user.profile.links.all()

    return render_to_response('backoffice/wizard/politician_profile/links.html',
                              {'user_id': user_id, 'links': links,
                              'election_instance_id': election_instance_id,
                              },
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_link_delete(request, link_id, election_instance_id, user_id):
    user = get_object_or_404(User, pk=user_id)
    link = user.profile.links.get(pk=link_id)
    link.delete()
    links = user.profile.links.all()
    return render_to_response('backoffice/wizard/politician_profile/links.html',
                              {'user_id': user_id, 'links': links,
                              'election_instance_id': election_instance_id,},
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_link_wizard(request, election_instance_id, user_id, link_id=None):
    return PoliticianProfileLinkWizard(user_id=user_id, election_instance_id=election_instance_id, link_id=link_id)(request)

@candidate_required
def politician_profile_connection(request, election_instance_id, user_id):
    user = get_object_or_404(User, pk=user_id)
    connections = user.profile.connections.all()

    return render_to_response('backoffice/wizard/politician_profile/connections.html',
                              {'user_id': user_id, 'connections': connections,
                              'election_instance_id': election_instance_id,
                              },
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_connection_delete(request, connection_id, election_instance_id, user_id):
    user = get_object_or_404(User, pk=user_id)
    connection = user.profile.connections.get(pk=connection_id)
    connection.delete()
    connections = user.profile.connections.all()
    return render_to_response('backoffice/wizard/politician_profile/connections.html',
                              {'user_id': user_id, 'connections': connections,
                              'election_instance_id': election_instance_id,},
                              context_instance=RequestContext(request))

@candidate_required
def politician_profile_connection_wizard(request, election_instance_id, user_id, connection_id=None):
    return PoliticianProfileConnectionWizard(user_id=user_id, election_instance_id=election_instance_id, connection_id=connection_id)(request)

@party_admin_required
def csv_import_candidates_step1(request, ep_id):
    eip = get_object_or_404(ElectionInstanceParty, pk=ep_id)
    return render_to_response('backoffice/csv_candidates_1.html', {'ep_id':ep_id, 'instance':eip.election_instance}, context_instance=RequestContext(request))

@party_admin_required
def csv_import_candidates_step2(request, ep_id, error = False):

    if(request.FILES or request.POST):
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
    try:
        candidates = functions.get_candidates_from_csv(request.session)
    except:

        path = settings.TMP_ROOT + '/'
        if not os.path.isdir(path):
            os.remove(path + request.session['csv_candidate_filename'])
        request.session['csv_candidate_filename'] = ''
        return redirect('bo.csv_candidates_step2', ep_id=ep_id, error='true')

    if(request.POST):
        eip_obj = get_object_or_404(ElectionInstanceParty, party=ep_id)
        form = CsvConfirmForm(request.POST)
        if form.is_valid():
            for candidate in candidates:
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
                    candidacy = Candidacy(
                        election_party_instance = eip_obj,
                        candidate = candidate_obj.user,
                        position = candidate['position'],
                    )
                    candidacy.save()

                    #Create invitation TODO: view and text etc.
                    templates = profile_invite_email_templates('candidate')
                    Invitation.create(
                        user_from = request.user,
                        user_to = candidate_obj.user,
                        view = '',
                        text = 'Invitation text',
                        subject = 'Invitation',
                        html_template = templates['html'],
                        plain_template = templates['plain'],
                    )

                    max_pos = int(candidate['position'])
                    if max_pos > eip_obj.list_length:
                        eip_obj.list_length = max_pos
                        eip_obj.save()

                except Exception:
                    transaction.rollback()
                    raise
                else:
                    transaction.commit()

            os.remove(settings.TMP_ROOT + '/' + request.session['csv_candidate_filename'])
            request.session['csv_candidate_filename'] = ''
            return redirect('bo.election_party_view', id=ep_id)
    else:
        form = CsvConfirmForm()
    eip = get_object_or_404(ElectionInstanceParty, pk=ep_id)
    forms = dict({'csv_confirm': form})
    return render_to_response('backoffice/csv_candidates_3.html', {'candidates':candidates, 'forms':forms, 'ep_id':ep_id, 'instance':eip.election_instance}, context_instance=RequestContext(request))

@party_admin_required
def csv_import_parties_step1(request, ei_id):
    ei_obj = get_object_or_404(ElectionInstance, id=ei_id)
    return render_to_response('backoffice/csv_parties_1.html', {'ei_id': ei_id, 'instance':ei_obj}, context_instance=RequestContext(request))

@party_admin_required
def csv_import_parties_step2(request, ei_id, error = False):
    if(request.FILES or request.POST):
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
    ei_obj = get_object_or_404(ElectionInstance, id=ei_id)
    forms = dict({'csv_upload': form})
    return render_to_response('backoffice/csv_parties_2.html', {'forms':forms, 'error': error, 'ei_id': ei_id, 'instance':ei_obj}, context_instance=RequestContext(request))

@party_admin_required
@transaction.commit_manually
def csv_import_parties_step3(request, ei_id):
    try:
        parties = functions.get_parties_from_csv(request.session)
    except:
        path = settings.TMP_ROOT + '/'
        if not os.path.isdir(path):
            os.remove(path + request.session['csv_party_filename'])
        request.session['csv_party_filename'] = ''
        return redirect('bo.csv_parties_step2', ei_id = ei_id, error='true')

    if(request.POST):
        form = CsvConfirmForm(request.POST)
        if form.is_valid():
            ei_obj = get_object_or_404(ElectionInstance, id=ei_id)
            council = ei_obj.council
            region = council.region
            level = council.level

            for party in parties:
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
                    
                    party_obj = Party(
                        region = region,
                        level = level,
                        name = party['name'],
                        abbreviation = party['abbreviation'],
                    )
                    party_obj.save()

                    eip_obj = ElectionInstanceParty(
                        election_instance = ei_obj,
                        party = party_obj,
                        position = party['list'],
                        list_length = 10, #TODO, maybe add in CSV
                    )
                    eip_obj.save()

                    party_obj.contacts.add(contact.user)
                    party_obj.save()

                    #Create invitation
                    templates = profile_invite_email_templates('party_admin')
                    Invitation.create(
                        user_from = request.user,
                        user_to = contact.user,
                        view = '',
                        text = 'Invitation text',
                        subject = 'Invitation',
                        html_template = templates['html'],
                        plain_template = templates['plain'],
                    )

                    max_list = int(party['list'])
                    if max_list > ei_obj.num_lists:
                        ei_obj.num_lists = max_list
                        ei_obj.save()

                except Exception:
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
    election_instance = get_object_or_404(ElectionInstance, pk=id)
    return CouncilEditWizard(election_instance)(request)


def answer_question(request, election_instance_party_id=None, user_id=None):
    '''
        AnswerQuestion - wizard.
        @param int election_instance_party_id - ElectionInstanceParty id
        @param int user_id User (Candidate=PoliticalProfile) id
    '''
    return AnswerQuestion(election_instance_party_id=election_instance_party_id, user_id=user_id)(request)

def answer_question_done(request):
    '''
        answer_question thanks page.
    '''
    return render_to_response('backoffice/wizard/question/answer_add/done.html',
                              context_instance=RequestContext(request))

def view_profile(request):
    """
        View a user profile
    """
    if request.user.profile:
        return render_to_response(get_profile_template(request.user.profile.type, 'backoffice_profile'), {}, context_instance=RequestContext(request))
    return redirect('/')
