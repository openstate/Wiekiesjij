import os.path
import os
#!/usr/env python
#-*- coding: utf-8 -*-
#
#Copyright 2009 Accepte. All Rights Reserved.

import time
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext
from elections.settings import ELECTION_EVENT_ID
from elections.models import ElectionInstance, ElectionInstanceParty
from political_profiles import functions
from utils.multipathform import MultiPathFormWizard, Step
from backoffice.decorators import staff_required
from backoffice.wizards import AddElectionInstanceWizard, ElectionSetupWizard, EditElectionInstanceWizard

# Even though your IDE (or your brains) might say this is an unused import,
# please do not remove the following Form imports
# FIXME: Remove import * once the test functions can be removed !
from backoffice.wizards import *
from political_profiles.forms import *
from elections.forms import *


def election_instance_view(request, id):
    instance = get_object_or_404(ElectionInstance, pk=id)
    return render_to_response('backoffice/election_instance_view.html', {'instance': instance}, context_instance=RequestContext(request))

def election_instance_shrink(request, id):
    instance = get_object_or_404(ElectionInstance, pk=id)
    instance.num_lists -= 1
    instance.save()
    return redirect('backoffice.election_instance_view', id=id)

def election_instance_grow(request, id):
    instance = get_object_or_404(ElectionInstance, pk=id)
    instance.num_lists += 1
    instance.save()
    return redirect('backoffice.election_instance_view', id=id)

def election_party_view(request, id):
    eip = get_object_or_404(ElectionInstanceParty, pk=id)
    return render_to_response('backoffice/election_party_view.html', {'instance': eip.election_instance, 'eip': eip}, context_instance=RequestContext(request))

def election_party_create(request, id, position):
    instance = get_object_or_404(ElectionInstance, pk=id)
    wizard = AddElectionPartyWizard(instance, position)
    return wizard(request)

def election_party_edit(request, id):
    eip = get_object_or_404(ElectionInstanceParty, pk=id)
    wizard = ElectionPartySetupWizard(eip)
    return wizard(request)

def election_party_up(request, id):
    eip = get_object_or_404(ElectionInstanceParty, pk=id)
    eip.move_up()
    return redirect('backoffice.election_instance_view', id=eip.election_instance.id)

def election_party_down(request, id):
    eip = get_object_or_404(ElectionInstanceParty, pk=id)
    eip.move_down()
    return redirect('backoffice.election_instance_view', id=eip.election_instance.id)

def election_party_shrink(request, id):
    eip = get_object_or_404(ElectionInstanceParty, pk=id)
    eip.list_length -= 1
    eip.save()
    return redirect('backoffice.election_party_view', id=id)

def election_party_grow(request, id):
    eip = get_object_or_404(ElectionInstanceParty, pk=id)
    eip.list_length += 1
    eip.save()
    return redirect('backoffice.election_party_view', id=id)

def candidate_up(request, id):
    can = get_object_or_404(Candidacy, pk=id)
    can.move_up()
    return redirect('backoffice.election_party_view', id=can.election_party_instance.id)

def candidate_down(request, id):
    can = get_object_or_404(Candidacy, pk=id)
    can.move_down()
    return redirect('backoffice.election_party_view', id=can.election_party_instance.id)


#@login_required
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


def form_view(request, form_type):
    try:
        formslist = dict(
            generic_form = globals()[form_type],
        )
    except KeyError:
        raise NameError('%s is not an existing form\nHave you checked your imports?' % (form_type))

    steps = Step('add_election_instance', forms=formslist, template='backoffice/wizard/step1.html')
    generic_form = MultiPathFormWizard(steps)
    return generic_form(request)

def wizard_view(request, wizard_type):
    try:
        wizard = globals()[wizard_type]
    except KeyError:
        raise NameError('%s is not an existing wizard\nHave you checked your imports?' % (wizard_type))
        
    return wizard()(request)

def election_setup(request, election_instance_id, user_id=None):
    '''
    Election setup wizard.
    @param int election_instance_id
    @param int user_id

    Both parameters are required. It's obvious what they mean.
    '''
    if not user_id:
        user_id = request.user.id

    return ElectionSetupWizard(election_instance_id=election_instance_id, user_id=user_id)(request)

def election_setup_done(request):
    '''
    Election setup wizard success page.
    '''
    return render_to_response('backoffice/wizard/election_setup/done.html',
                              context_instance=RequestContext(request))

def politician_welcome(request):
    user_id = 2
    return render_to_response('backoffice/wizard/politician_profile/welcome.html',
                              {'user_id': user_id},
                              context_instance=RequestContext(request))

def politician_profile_setup(request, user_id):
    return PoliticianProfileWizard(user_id=user_id)(request)

def politician_profile_setup_done(request, user_id):
    return render_to_response('backoffice/wizard/politician_profile/done.html',
                              {'user_id': user_id},
                              context_instance=RequestContext(request))

def politician_profile_interest(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    interests = user.profile.interests.all()
    return render_to_response('backoffice/wizard/politician_profile/interest.html',
                              {'user_id': user_id, 'interests': interests,},
                              context_instance=RequestContext(request))

def politician_profile_interest_wizard(request, user_id, interest_id=None):
    return PoliticianProfileInterestWizard(user_id=user_id, interest_id=interest_id)(request)

def politician_profile_work(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    work = user.profile.work.all()
    return render_to_response('backoffice/wizard/politician_profile/work.html',
                              {'user_id': user_id, 'work': work,},
                              context_instance=RequestContext(request))

def politician_profile_work_wizard(request, user_id, work_id=None):
    return PoliticianProfileWorkWizard(user_id=user_id, work_id=work_id)(request)


def politician_profile_political(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    political = user.profile.political.all()
    return render_to_response('backoffice/wizard/politician_profile/political.html',
                              {'user_id': user_id, 'political': political,},
                              context_instance=RequestContext(request))

def politician_profile_political_wizard(request, user_id, political_id=None):
    return PoliticianProfilePoliticalWizard(user_id=user_id, political_id=political_id)(request)

def politician_profile_education(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    education = user.profile.education.all()
    return render_to_response('backoffice/wizard/politician_profile/education.html',
                              {'user_id': user_id, 'education': education,},
                              context_instance=RequestContext(request))

def politician_profile_education_wizard(request, user_id, education_id=None):
    return PoliticianProfileEducationWizard(user_id=user_id, education_id=education_id)(request)

def politician_profile_appearance(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    appearances = user.profile.appearances.all()
    return render_to_response('backoffice/wizard/politician_profile/appearances.html',
                              {'user_id': user_id, 'appearances': appearances,},
                              context_instance=RequestContext(request))

def politician_profile_appearance_wizard(request, user_id, appearance_id=None):
    return PoliticianProfileAppearanceWizard(user_id=user_id, appearance_id=appearance_id)(request)


def politician_profile_link(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    links = user.profile.links.all()
    print user_id
    return render_to_response('backoffice/wizard/politician_profile/links.html',
                              {'user_id': user_id, 'links': links},
                              context_instance=RequestContext(request))

def politician_profile_link_wizard(request, user_id, link_id=None):
    return PoliticianProfileLinkWizard(user_id=user_id, link_id=link_id)(request)

def council_edit(request, id):
    '''
    Council edit wizard.
    @param int id election_instance_id
    '''
    instance = get_object_or_404(ElectionInstance, pk=id)
    return CouncilEditWizard(election_instance=instance)(request)

def csv_import_candidates_step1(request):
    return render_to_response('backoffice/csv_candidates_1.html', context_instance=RequestContext(request))

def csv_import_candidates_step2(request, error = False):
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
            return redirect('backoffice.csv_candidates_step3')
            
    else:
        form = CsvUploadForm()

    forms = dict({'csv_upload': form})
    return render_to_response('backoffice/csv_candidates_2.html', {'forms':forms, 'error': error}, context_instance=RequestContext(request))

@transaction.commit_manually
def csv_import_candidates_step3(request):
    try:
        candidates = functions.get_candidates_from_csv(request.session)
    except:
        path = settings.TMP_ROOT + '/'
        if not os.path.isdir(path):
            os.remove(path + request.session['csv_candidate_filename'])
        request.session['csv_candidate_filename'] = ''
        return redirect('backoffice.csv_candidates_step2', error='true')

    if(request.POST):
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
                    candidate_obj = create_profile('candidate', tmp_data)

                    #Link candidate to party
                    candidacy = Candidacy(
                        election_party_instance = get_object_or_404(ElectionInstanceParty, party=1), #TODO: Make party dynamic
                        candidate = candidate_obj.user,
                        position = candidate['position'],
                    )
                    candidacy.save()

                    #Create invitation
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

                except Exception:
                    transaction.rollback()
                    raise
                else:
                    transaction.commit()

            os.remove(settings.TMP_ROOT + '/' + request.session['csv_candidate_filename'])
            request.session['csv_candidate_filename'] = ''
            return redirect('backoffice.election_party_view', args=1) #TODO: Make party dynamic
    else:
        form = CsvConfirmForm()

    forms = dict({'csv_confirm': form})
    return render_to_response('backoffice/csv_candidates_3.html', {'candidates':candidates, 'forms':forms}, context_instance=RequestContext(request))

def csv_import_parties_step1(request):
    return render_to_response('backoffice/csv_parties_1.html', context_instance=RequestContext(request))

def csv_import_parties_step2(request, error = False):
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
            return redirect('backoffice.csv_parties_step3')

    else:
        form = CsvUploadForm()

    forms = dict({'csv_upload': form})
    return render_to_response('backoffice/csv_parties_2.html', {'forms':forms, 'error': error}, context_instance=RequestContext(request))

@transaction.commit_manually
def csv_import_parties_step3(request):
    try:
        parties = functions.get_parties_from_csv(request.session)
    except:
        path = settings.TMP_ROOT + '/'
        if not os.path.isdir(path):
            os.remove(path + request.session['csv_party_filename'])
        request.session['csv_party_filename'] = ''
        return redirect('backoffice.csv_parties_step2', error='true')

    if(request.POST):
        form = CsvConfirmForm(request.POST)
        if form.is_valid():
            ei_id = 1 #TODO
            region_id = 1 #TODO Maybe these ID's can be obtained through ElectionInstance or so
            level_id =1 #TODO
            length_of_list = 10 #TODO

            for party in parties:
                try:
                    #Store data
                    party_obj = Party(
                        region = region_id,
                        level = level_id,
                        name = party['name'],
                        abbreviation = party['abbreviation'],
                    )
                    party_obj.save()

                    eip_obj = ElectionInstanceParty(
                        election_instance = get_object_or_404(ElectionInstance, id=ei_id),
                        party = party_obj,
                        position = party['list'],
                        list_length = length_of_list,
                    )
                    eip_obj.save()

                    tmp_data = {
                        'first_name': party['contact_first_name'],
                        'middle_name': party['contact_middle_name'],
                        'last_name': party['contact_last_name'],
                        'email': party['contact_email'],
                        'gender': party['contact_gender'],
                    }
                    contact = create_profile('party_admin', tmp_data)

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

                except Exception:
                    transaction.rollback()
                    raise
                else:
                    transaction.commit()

            os.remove(settings.TMP_ROOT + '/' + request.session['csv_party_filename'])
            request.session['csv_party_filename'] = ''
            return redirect('backoffice.election_region_view', args=region_id)
    else:
        form = CsvConfirmForm()

    forms = dict({'csv_confirm': form})
    return render_to_response('backoffice/csv_parties_3.html', {'parties':parties, 'forms':forms}, context_instance=RequestContext(request))

def council_edit(request, election_instance_id, user_id):
    '''
    Council edit wizard.
    @param int election_instance_id
    @param int user_id

    Both parameters are required. It's obvious what they mean.
    '''
    return CouncilEditWizard(election_instance_id=election_instance_id, user_id=user_id)(request)

def council_edit_done(request):
    '''
    Council edit wizard success page.
    '''
    return render_to_response('backoffice/wizard/council/edit/done.html',
                              context_instance=RequestContext(request))