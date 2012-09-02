import copy
import json
import random
from operator import itemgetter

from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from utils.multipathform import Step, MultiPathFormWizard
from utils.netutils import getip


from questions.forms import VisitorAnswerQuestionForm, PartyQuestionForm, WorkTypeQuestionForm, PolTypeQuestionForm
from questions.forms.types import ThemeAnswerForm
from questions.models import Question, Answer
from elections.models import Candidacy, ElectionInstanceParty, ElectionInstance
from questions.settings import QTYPE_MODEL_PROFILE_QUESTION_WEIGHT, QTYPE_NORM_POLONECHOICE_VISONECHOICE_RANGE, QTYPE_MODEL_POLITICAL_EXPERIENCE_YEARS, QTYPE_MODEL_EDUCATION_LEVEL, QTYPE_MODEL_PROFILE_RELIGION, QTYPE_MODEL_PROFILE_AGE, QTYPE_MODEL_PROFILE_GENDER, QTYPE_MODEL_PARTY
from questions.settings import QTYPE_MODEL_WORK_EXPERIENCE_TYPE, QTYPE_MODEL_POLITICAL_EXPERIENCE_TYPE
from questions.settings import FRONTOFFICE_QUESTION_TYPES, BACKOFFICE_QUESTION_TYPES, MULTIPLE_ANSWER_TYPES
from political_profiles.models import EducationLevel, PoliticianProfile, Education
from political_profiles.models import WorkExperienceSector, PoliticalExperienceType
from frontoffice.models import VisitorResult, CandidateAnswers

from utils.emails import send_email

class BestCandidate(MultiPathFormWizard):
    '''
        BestCandidate Wizard.
    '''
    def __init__(self, *args, **kwargs):
        self.election_instance_id = kwargs['election_instance_id']
        self.iframe = kwargs['iframe']
        self.election_instance = get_object_or_404(ElectionInstance, id=self.election_instance_id)
        eips = ElectionInstanceParty.objects.filter(election_instance=self.election_instance)

        elections_candidates = Candidacy.objects.filter(election_party_instance__in=eips)
        self.elections_candidacies = elections_candidates

        # get a list of candidate ids
        self.user_ids=[] # this is a list of user ids
        for elections_candidate in  elections_candidates:
            self.user_ids.append(elections_candidate.candidate_id)
        users = User.objects.filter(pk__in=self.user_ids)
        #candidates = PoliticianProfile.objects.filter(user__in=users).order_by('?')
        #self.candidates = candidates # list of Politician Profiles in this election instance

        #Get all questions
        questions = self.election_instance.questions.filter(question_type__in=FRONTOFFICE_QUESTION_TYPES).order_by('-electioninstancequestion__position')
        steps_tree = []

        # Looping through the questions
        idx = 1;
        for question in questions:
            # Finds out if you should add a no preference option to the question
            if question.has_no_preference:
                empty_label = _('Geen voorkeur')
            else:
                empty_label=None

            if question.question_type in BACKOFFICE_QUESTION_TYPES:
                form = {str(question.id): VisitorAnswerQuestionForm}
                fkwargs={str(question.id): {'question_instance_id': question.id}}

            elif QTYPE_MODEL_PARTY == question.question_type:
                form = {str(question.id): PartyQuestionForm}

                fkwargs= {str(question.id): {'queryset': self.election_instance.parties, 'empty_label':empty_label}}

            elif QTYPE_MODEL_POLITICAL_EXPERIENCE_YEARS == question.question_type:
                form = {str(question.id): VisitorAnswerQuestionForm}
                fkwargs={str(question.id): {'question_instance_id': question.id}}

            elif QTYPE_MODEL_EDUCATION_LEVEL == question.question_type:
                form = {str(question.id): VisitorAnswerQuestionForm}
                fkwargs={str(question.id): {'question_instance_id': question.id}}

            elif QTYPE_MODEL_PROFILE_RELIGION == question.question_type:
                form = {str(question.id): VisitorAnswerQuestionForm}
                fkwargs={str(question.id): {'question_instance_id': question.id}}

            elif QTYPE_MODEL_PROFILE_AGE == question.question_type:
                form = {str(question.id): VisitorAnswerQuestionForm}
                fkwargs={str(question.id): {'question_instance_id': question.id}}

            elif QTYPE_MODEL_PROFILE_GENDER == question.question_type:
                form = {str(question.id): VisitorAnswerQuestionForm}
                fkwargs={str(question.id): {'question_instance_id': question.id}}
            elif QTYPE_MODEL_PROFILE_QUESTION_WEIGHT == question.question_type:
                form = {str(question.id): ThemeAnswerForm}
                fkwargs= {str(question.id): {'queryset': self.election_instance.questions.filter(question_type__in=FRONTOFFICE_QUESTION_TYPES).order_by('electioninstancequestion__position'), 'empty_label':empty_label}}

            elif QTYPE_MODEL_WORK_EXPERIENCE_TYPE == question.question_type:
                form = {str(question.id): WorkTypeQuestionForm}
                fkwargs= {str(question.id): {'queryset': WorkExperienceSector.objects.all(), 'empty_label' :empty_label}}
            elif QTYPE_MODEL_POLITICAL_EXPERIENCE_TYPE == question.question_type:
                form = {str(question.id): PolTypeQuestionForm}
                fkwargs= {str(question.id): {'queryset': PoliticalExperienceType.objects.all(), 'empty_label' :empty_label}}
            else:
                pass

            if self.iframe:
                parent = 'frontoffice/iframe.html'
            else:
                parent = 'frontoffice/wizard/base.html'

            step = Step(str(question.id),
                     forms=form,
                     template='frontoffice/wizard/test/step1.html',
                     extra_context={'questions': range(0, questions.count()), 'current_question': questions.count() - idx, 'question_title': question.get_frontend_title(), 'parent':parent, 'election_instance': self.election_instance},
                     form_kwargs=fkwargs)
            steps_tree.append(step)
            idx += 1

        scenario_tree = None
        for step in steps_tree:
            if None == scenario_tree:
                scenario_tree = step.next()
            else:
                scenario_tree = step.next(scenario_tree)

        template = 'frontoffice/wizard/base.html',
        super(BestCandidate, self).__init__(scenario_tree, template)

    def get_next_step(self, request, next_steps, current_path, forms_path):
        return 0

    def done(self, request, form_dict):
        num_weighted_questions = 0
        num_questions = 0
        real_score = 0
        candidate_scores = {}
        candidate_question_answers = {}
        self.multiply_questions = []
        candidate_ids = []
        questions_skipped = []
        
        # get party-list
        users_of_allowed_parties = []
        for path, forms in form_dict.iteritems():
            for question_id, form in forms.iteritems():
                num_questions = num_questions + 1
                question = Question.objects.get(id=question_id) 
                answer_value = form.cleaned_data['value']
                if QTYPE_MODEL_PARTY == question.question_type:
                    for party in answer_value:
                        current_eip = getattr(party, 'current_eip')
                        if current_eip is None:
                            return Http404()
                        candidatesOnList = current_eip.candidate_dict()
                        for id, candidateOnList in candidatesOnList.iteritems():
                            if candidateOnList:
                                users_of_allowed_parties.append(candidateOnList.candidate_id)
        users = User.objects.filter(pk__in=users_of_allowed_parties)
        candidateSelection = PoliticianProfile.objects.filter(user__in=users).order_by('?')

        # get list of candidate ids and create a dictionay entry for each candidate to keep array of scores
        for candidate in candidateSelection:
            
            candidate_scores[candidate] = []
            candidate_ids.append(candidate.id)
        # get a list of answers that each candidate has chosen and store them in a dictionary
        for candidate in self.elections_candidacies:

            candidate_question_answers[candidate.candidate.profile] = {}
            question_answers = candidate.answers.all()
            for question_answer in question_answers:
                if question_answer.question_id in candidate_question_answers[candidate.candidate.profile].keys():

                    candidate_question_answers[candidate.candidate.profile][question_answer.question_id].append(question_answer.id)
                else:
                    answer_list = []
                    answer_list.append(question_answer.id)
                    candidate_question_answers[candidate.candidate.profile][question_answer.question_id] = answer_list
        #Create a full list of candidate answers for storage
        all_candidate_answers = copy.deepcopy(candidate_question_answers)
        all_visitor_answers = {}
        all_questions = []
        for path, forms in form_dict.iteritems():
            for question_id, form in forms.iteritems():
                num_questions = num_questions + 1
                question = Question.objects.get(id=question_id)
                all_questions.append(question)
                answer_value = form.cleaned_data['value']
                empty_list = []
                # checks if the answer is will be returned in a list, make into a list if not
                if question.question_type not in MULTIPLE_ANSWER_TYPES:
                    empty_list.append(answer_value)
                    answer_value = empty_list
                else:
                    answer_value = list(answer_value)
                #all_visitor_answers[question_id] = answer_value
                #if no preference is selected question is ignored
                if 'no_pref' in answer_value:
                    all_visitor_answers[question_id] = answer_value
                    questions_skipped.append(question_id)
                    continue

                # Get length of the list to help calculate score
                length = len(answer_value)


                if question.question_type in BACKOFFICE_QUESTION_TYPES:
                    all_visitor_answers[question_id] = answer_value
                    for candidate in candidateSelection:

                        keys = candidate_question_answers[candidate].keys()
                        question_id = int(question_id)

                        score = 0
                        if question_id in keys:
                            for value in answer_value:
                                if question.question_type == QTYPE_NORM_POLONECHOICE_VISONECHOICE_RANGE:
                                    answer = Answer.objects.get(id=value)
                                    politicians_answer = Answer.objects.get(id=int(candidate_question_answers[candidate][int(question_id)][0]) )

                                    if int(politicians_answer.meta) >= int(answer.meta):
                                        score = 1
                                else:
                                    if int(value) in candidate_question_answers[candidate][int(question_id)]:
                                        score = score + 1
                        if score > 0:
                            new_score = float(float(score) / float(len(candidate_question_answers[candidate][int(question_id)])))
                        else:
                            new_score = 0
                        candidate_scores[candidate].append({question.id: new_score})

                elif QTYPE_MODEL_PARTY == question.question_type:
                    party_names = [value.name for value in answer_value]
                    for candidate in candidateSelection:
                        all_candidate_answers[candidate][question_id] = candidate.party().id

                    all_visitor_answers[question_id] = party_names

                elif QTYPE_MODEL_POLITICAL_EXPERIENCE_YEARS == question.question_type:

                    all_visitor_answers[question_id] = answer_value
                    answer = Answer.objects.get(id=answer_value[0])
                    parts = answer.meta.split(':')
                    start = parts[0]
                    if len(parts) > 1:
                        end= parts[1]
                    else:
                        end = int(parts[0]) + 1
                    if end == 'G':
                        for candidate in candidateSelection:
                            if candidate.political_experience_days == None:
                                candidate.political_experience_days = 0
                            if (int(candidate.political_experience_days)/365) >= int(start):
                                candidate_scores[candidate].append({question.id: 1})

                            all_candidate_answers[candidate][question_id] = (int(candidate.political_experience_days)/365)
                    else:
                        for candidate in candidateSelection:
                            # need to subtract one form the end figure as 'to' is up to but not equal
                            if candidate.political_experience_days == None:
                                candidate.political_experience_days = 0
                            if (int(candidate.political_experience_days)/365) in range(int(start),(int(end))):
                                candidate_scores[candidate].append({question.id: 1})

                            all_candidate_answers[candidate][question_id] = (int(candidate.political_experience_days)/365)

                elif QTYPE_MODEL_EDUCATION_LEVEL == question.question_type:

                    answer = Answer.objects.get(id=answer_value[0])
                    answer_value= answer.meta
                    if answer_value == 'ALL_OTHERS':
                        exclude_list = ['HBO', 'MBO', 'Universitair']
                        levels = EducationLevel.objects.exclude(level__in=exclude_list)
                    else:
                        levels = EducationLevel.objects.filter(level=answer_value)

                    # Check all levels that the politican can be in to be a match
                    level_names = []
                    for level in levels:
                        level_names.append(level.level)
                        #get all the education levels that have a level in the correct level list
                        ed_instances =Education.objects.filter(level=level.id)
                        for ed in ed_instances:
                            #if the education is of a candidate of this match
                            if ed.politician_id in candidate_ids:
                                #get the politician
                                candidate = PoliticianProfile.objects.get(id=ed.politician_id)
                                #Add level to all_candidate_answers
                                if question_id  in all_candidate_answers[candidate].keys():
                                    all_candidate_answers[candidate][question_id].append(ed.level.level)
                                else:
                                    all_candidate_answers[candidate][question_id] = []
                                    all_candidate_answers[candidate][question_id].append(ed.level.level)
                                answered = False

                                for question_answer in candidate_scores[candidate]:
                                    if question.id in question_answer.keys():
                                        answered = True
                                if answered == False:
                                    candidate_scores[candidate].append({question.id: 1})

                    all_visitor_answers[question_id] = level_names
                elif QTYPE_MODEL_PROFILE_RELIGION == question.question_type:
                    all_visitor_answers[question_id] = answer_value
                    for value in answer_value:

                        for candidate in candidateSelection.all():
                            all_candidate_answers[candidate][question_id] = candidate.religion
                            if candidate.religion == value:
                                candidate_scores[candidate].append({question.id: 1})


                elif QTYPE_MODEL_PROFILE_AGE == question.question_type:
                    all_visitor_answers[question_id] = answer_value
                    answer = Answer.objects.get(id=answer_value[0])
                    parts = answer.meta.split(':')
                    start = parts[0]
                    if len(parts) > 1:
                        end=parts[1]
                    if end == '':
                        for candidate in candidateSelection:
                            if candidate.age >= int(start):
                                candidate_scores[candidate].append({question.id: 1})

                            all_candidate_answers[candidate][question_id] = candidate.age
                    elif start == '':
                        for candidate in candidateSelection:
                            if candidate.age < int(end):
                                candidate_scores[candidate].append({question.id: 1})

                            all_candidate_answers[candidate][question_id] = candidate.age
                    else:
                        for candidate in candidateSelection:

                            if candidate.age in range(int(start),int(end)):
                                candidate_scores[candidate].append({question.id: 1})

                            all_candidate_answers[candidate][question_id] = candidate.age

                elif QTYPE_MODEL_PROFILE_GENDER == question.question_type:
                    all_visitor_answers[question_id] = answer_value
                    for candidate in candidateSelection:
                        if candidate.gender == answer_value[0]:
                            candidate_scores[candidate].append({question.id: 1})

                        all_candidate_answers[candidate][question_id] = candidate.gender

                elif QTYPE_MODEL_PROFILE_QUESTION_WEIGHT == question.question_type:
                    all_visitor_answers[question_id] = answer_value


                    self.multiply_questions = answer_value[0]

                elif QTYPE_MODEL_WORK_EXPERIENCE_TYPE == question.question_type:
                    all_visitor_answers[question_id] = [a.id for a in answer_value]
                    queryset = candidateSelection.all().distinct().filter(work__sector__in=answer_value)
                    for candidate in queryset:
                        candidate_scores[candidate].append({question.id: 1})
                        all_candidate_answers[candidate][question_id] = list(set([s.sector_id for s in candidate.work.all()]))

                elif QTYPE_MODEL_POLITICAL_EXPERIENCE_TYPE == question.question_type:
                    all_visitor_answers[question_id] = [a.id for a in answer_value]
                    queryset = candidateSelection.all().distinct().filter(political__type__in=answer_value)
                    for candidate in queryset:
                        candidate_scores[candidate].append({question.id: 1})
                        all_candidate_answers[candidate][question_id] = list(set([s.type_id for s in candidate.political.all()]))

                # fill out list with default score of 0 for each candidate, if not already there
                for candidate in candidateSelection:
                    answered = False
                    for question_answer in candidate_scores[candidate]:
                        if question.id in question_answer.keys():
                            answered = True
                    if answered == False:
                        candidate_scores[candidate].append({question.id: 0})

        #Add Weighting
        num_weighted_questions = 0
        for question in all_questions:
            if str(question.id) not in questions_skipped:
                  if question.theme in self.multiply_questions:
                    num_weighted_questions = num_weighted_questions + 1
        number_of_questions = (((num_questions - 2) + num_weighted_questions ) - len(questions_skipped))

        if number_of_questions < 1:
            number_of_questions = 1

        for candidate in candidateSelection:
            for question in candidate_scores[candidate]:
                for question_id, score in question.iteritems():
                    qid = question_id
                    for q in all_questions:

                        if qid == q.id:

                            if q.theme in self.multiply_questions:
                                score = score * 2
                                score = float(float(score * 100)/number_of_questions)
                                question[question_id] = score
                            else:
                                score = float(float(score * 100)/number_of_questions)
                                question[question_id] = score


        candidates_total_scores = {}
        for candidate in candidateSelection:

            total = 0
            for question in candidate_scores[candidate]:
               for question_id, score in question.iteritems():
                    total = float(total + score)

            #candidates_total_scores[candidate] = ceil(total)
            if total > 99 and settings.DEBUG == False:
                if int(total) > 100:
                    real_score = total
                total = 100

            if settings.DEBUG and total < 100 and total > 99:
                total = 100


            candidates_total_scores[candidate] = total
        visitor = VisitorResult()

        new_visitor = visitor.create()

        new_visitor.ipaddress=getip(request)
        new_visitor.election_instance = self.election_instance

        # Only link visitors
        if request.user.is_authenticated() and request.user.profile and request.user.profile.type == 'visitor':
            new_visitor.user = request.user
        new_visitor.visitor_answers = json.dumps(all_visitor_answers)
        new_visitor.save()

        sorted_candidates = [(k, candidates_total_scores[k]) for k in candidates_total_scores.keys()]
        random.seed()
        random.shuffle(sorted_candidates)

        sorted_candidates = sorted(sorted_candidates, key=itemgetter(1), reverse=True)

        for candidate, score in sorted_candidates[:5]:

            candidate_ans = CandidateAnswers()
            candidate_ans.candidate = candidate.user
            candidate_ans.candidate_answers = json.dumps(all_candidate_answers[candidate])
            candidate_ans.candidates_score = candidates_total_scores[candidate]
            candidate_ans.candidate_question_scores = json.dumps(candidate_scores[candidate])
            candidate_ans.save()
            new_visitor.candidate_answers.add(candidate_ans)

        if real_score > 0:
            try:
                send_email(
                            'Error: score more than 100 in results',
                            'info@wiekiesjij.nl',
                            'webmaster@wiekiesjij.nl',
                            {'hash': new_visitor.hash, 'real_score': real_score},
                            {'plain': 'questions/score_error.txt'},
                )
            except:
                pass
        if self.iframe:
            return redirect('fo.match_results', hash=new_visitor, iframe=self.iframe)
        else:
            return redirect('fo.match_results', hash=new_visitor)




