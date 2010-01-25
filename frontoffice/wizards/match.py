import datetime

from django.db import transaction
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from utils.multipathform import Step, MultiPathFormWizard

from questions.forms.types import MultipleAnswerForm, BooleanForm, MultipleChoiceForm
from questions.forms import SelectQuestionForm, VisitorAnswerQuestionForm
from questions.forms.types import ModelMultiAnswerForm, ModelAnswerForm, ThemeAnswerForm
from questions.models import Question, Answer
from elections.models import Candidacy, ElectionInstanceParty
from questions.settings import QTYPE_MODEL_PROFILE_QUESTION_WEIGHT, QTYPE_NORM_POLONECHOICE_VISONECHOICE_RANGE, QUESTION_TYPE_CHOICES, QTYPE_NORM_POLONECHOICE_VISONECHOICE, QTYPE_MODEL_WORK_EXPERIENCE_YEARS, QTYPE_MODEL_EDUCATION_LEVEL, QTYPE_MODEL_PROFILE_RELIGION, QTYPE_MODEL_PROFILE_AGE, QTYPE_MODEL_PROFILE_GENDER, QTYPE_MODEL_PARTY, QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE
from questions.settings import FRONTOFFICE_QUESTION_TYPES, BACKOFFICE_QUESTION_TYPES, MULTIPLE_ANSWER_TYPES
from political_profiles.models import WorkExperienceSector, EducationLevel, PoliticianProfile, Education

from elections.models import ElectionInstance, ElectionInstanceParty, ElectionInstanceQuestion, ElectionInstanceQuestionAnswer
from elections.functions import get_profile_forms, create_profile, profile_invite_email_templates, get_profile_model
from types import ListType
from questions.forms import SelectQuestionForm, AnswerQuestionForm
class BestCandidate(MultiPathFormWizard):
    '''
        BestCandidate Wizard.
    '''
    def __init__(self, *args, **kwargs):
        self.election_instance_id = kwargs['election_instance_id']
        self.iframe = kwargs['iframe']
        self.election_instance = ElectionInstance.objects.get(id=self.election_instance_id)
        eips = ElectionInstanceParty.objects.filter(election_instance=self.election_instance)

        elections_candidates = Candidacy.objects.filter(election_party_instance__in=eips)
        self.elections_candidacies = elections_candidates
        print len(self.elections_candidacies)
        # get a list of candidate ids
        self.user_ids=[] # this is a list of user ids
        for elections_candidate in  elections_candidates:
            self.user_ids.append(elections_candidate.candidate_id)
        users = User.objects.filter(pk__in=self.user_ids)
        candidates = PoliticianProfile.objects.filter(user__in=users)
        self.candidates = candidates # list of Politician Profiles in this election instance
        print len(candidates)
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
                form = {str(question.id): ModelMultiAnswerForm}

                fkwargs= {str(question.id): {'queryset': self.election_instance.parties, 'attribute':'name', 'empty_label':empty_label}}

            elif QTYPE_MODEL_WORK_EXPERIENCE_YEARS == question.question_type:
                form = {str(question.id): VisitorAnswerQuestionForm}
                fkwargs={str(question.id): {'question_instance_id': question.id}}

            elif QTYPE_MODEL_EDUCATION_LEVEL == question.question_type:
                form = {str(question.id): AnswerQuestionForm}
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
            else:
                pass

            if self.iframe:
                parent = 'frontoffice/wizard/iframe.html'
            else:
                parent = 'frontoffice/wizard/base.html'
                
            step = Step(str(question.id),
                     forms=form,
                     template='frontoffice/wizard/test/step1.html',
                     extra_context={'questions': range(0, questions.count()), 'current_question': questions.count() - idx, 'question_title': question.get_frontend_title(), 'parent':parent},
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

    @transaction.commit_manually
    def done(self, request, form_dict):

        candidate_scores = {}
        candidate_question_answers = {}
        candidate_ids = []
        # get list of candidate ids and create a dictionay entry for each candidate to keep array of scores
        for candidate in self.candidates:
            candidate_scores[candidate] = []
            candidate_ids.append(candidate.id)
        # get a list of answers that each candidate has chosen and store them in a dictionary
        for candidate in self.elections_candidacies:
            candidate_question_answers[candidate] = {}
            question_answers = candidate.answers.all()
            for question_answer in question_answers:
                if question_answer.question_id in candidate_question_answers[candidate].keys():

                    candidate_question_answers[candidate][question_answer.question_id].append(question_answer.id)
                else:
                    answer_list = []
                    answer_list.append(question_answer.id)
                    candidate_question_answers[candidate][question_answer.question_id] = answer_list
                
        for path, forms in form_dict.iteritems():
            for question_id, form in forms.iteritems():
                print question_id, 'QUESTION'
                question = Question.objects.get(id=question_id)

                answer_value = form.cleaned_data['value']
                empty_list = []
                # checks if the answer is will be returned in a list, make into a list if not
                if question.question_type not in MULTIPLE_ANSWER_TYPES:
                    empty_list.append(answer_value)
                    answer_value = empty_list
                else:    
                    answer_value = list(answer_value)

                #if no preference is selected question is ignored
                if 'no_pref' in answer_value:
                    print question_id, 'no-pref'
                    for candidate in self.candidates:
                        candidate_scores[candidate].append({question.id: 0})
                    continue

                # Get length of the list to help calculate score
                length = len(answer_value)


                if question.question_type in BACKOFFICE_QUESTION_TYPES:

                    for candidate in self.elections_candidacies:

                        keys = candidate_question_answers[candidate].keys()
                        question_id = int(question_id)

                        score = 0
                        if question_id in keys:
                            for value in answer_value:
                                if question.question_type == QTYPE_NORM_POLONECHOICE_VISONECHOICE_RANGE:
                                    answer = Answer.objects.get(id=value)
                                    politicians_answer = Answer.objects.get(id=int(candidate_question_answers[candidate][int(question_id)][0]) )
                                    print int(politicians_answer.meta), int(answer.meta)
                                    if int(politicians_answer.meta) >= int(answer.meta):
                                        score = 1
                                else:
                                    if int(value) in candidate_question_answers[candidate][int(question_id)]:
                                        score = score + 1
                        if score > 0:
                            new_score = float(float(score) / float(length))
                        else:
                            new_score = 0
                        candidate_scores[candidate.candidate.profile].append({question.id: new_score})
                        if question_id in keys:
                            print question_id, candidate.candidate.profile.full_name(), candidate_question_answers[candidate][int(question_id)], answer_value, 'score:', new_score

                elif QTYPE_MODEL_PARTY == question.question_type:
                    for value in answer_value:
                        for candidate in self.candidates:
                            if candidate.party() == value:
                                candidate_scores[candidate].append({question.id: 1})
                                print question_id, candidate.full_name(), candidate.party(), answer_value, 'score:', 1 

                elif QTYPE_MODEL_WORK_EXPERIENCE_YEARS == question.question_type:
                    answer = Answer.objects.get(id=answer_value[0])
                    parts = answer.meta.split(':')
                    start = parts[0]
                    if len(parts) > 1:
                        end= parts[1]
                    else:
                        end = int(parts[0]) + 1                    
                    if end == 'G':
                        for candidate in self.candidates:
                            if candidate.work_experience_days == None:
                                candidate.work_experience_days = 0
                            if (int(candidate.work_experience_days)/365) >= int(start):
                                candidate_scores[candidate].append({question.id: 1})
                                print question_id, candidate.full_name(), (int(candidate.work_experience_days)/365), answer.meta, 'score:', 1 
                    else:
                        for candidate in self.candidates:
                            # need to subtract one form the end figure as 'to' is up to but not equal
                            if candidate.work_experience_days == None:
                                candidate.work_experience_days = 0
                            if (int(candidate.work_experience_days)/365) in range(int(start),(int(end)-1)):
                                candidate_scores[candidate].append({question.id: 1})
                                print question_id, candidate.candidate.profile.full_name(), (int(candidate.work_experience_days)/365), answer.meta, 'score:', 1

                elif QTYPE_MODEL_EDUCATION_LEVEL == question.question_type:
                    answer = Answer.objects.get(id=answer_value[0])
                    answer_value= answer.meta
                    if answer_value == 'ALL_OTHERS':
                        exclude_list = ['HBO', 'MBO', 'Universitair']
                        levels = EducationLevel.objects.exclude(level__in=exclude_list)
                    else:
                        levels = EducationLevel.objects.exclude(level=answer_value)
                    for level in levels:
                        ed_instances =Education.objects.filter(level=level.id)
                        for ed in ed_instances:
                            if ed.politician_id in candidate_ids:
                                candidate = PoliticianProfile.objects.get(id=ed.politician_id)
                                answered = False
                                for question_answer in candidate_scores[candidate]:
                                    if question.id in question_answer.keys():
                                        answered = True
                                if answered == False:
                                    candidate_scores[candidate].append({question.id: 1})
                                    print question_id, candidate.full_name(), ed.politician_id , candidate_ids, 'score:', 1

                elif QTYPE_MODEL_PROFILE_RELIGION == question.question_type:
                    for value in answer_value:
                        for candidate in self.candidates:
                            if candidate.religion == value:
                                candidate_scores[candidate].append({question.id: 1})
                                print question_id, candidate.full_name(), candidate.religion , answer_value, 'score:', 1


                elif QTYPE_MODEL_PROFILE_AGE == question.question_type:
                    answer = Answer.objects.get(id=answer_value[0])
                    parts = answer.meta.split(':')
                    start = parts[0]
                    if len(parts) > 1:
                        end=parts[1]
                    if end == 'G':
                        for candidate in self.candidates:
                            if candidate.age() >= int(start):
                                candidate_scores[candidate].append({question.id: 1})
                                print question_id, candidate.full_name(), candidate.age() , answer.meta, 'score:', 1
                    else:
                        for candidate in self.candidates:
                            # need to subtract one form the end figure as 'to' is up to but not equal
                            if candidate.age() in range(int(start),int(end)-1):
                                candidate_scores[candidate].append({question.id: 1})
                                print question_id, candidate.candidate.profile.full_name(), candidate.age() , answer.meta, 'score:', 1

                elif QTYPE_MODEL_PROFILE_GENDER == question.question_type:

                    matches = self.candidates.filter(gender=answer_value[0])
                    for match in matches:
                        candidate_scores[match].append({question.id: 1})
                        print question_id, match.full_name(), match.gender , answer_value[0], 'score:', 1

                elif QTYPE_MODEL_PROFILE_QUESTION_WEIGHT == question.question_type:

                    self.multiply_questions = answer_value[0]

                else:
                    print 'skipped'
                    pass

                # fill out list with default score of 0 for each candidate, if not already there
                for candidate in self.candidates:
                    answered = False
                    for question_answer in candidate_scores[candidate]:
                        if question.id in question_answer.keys():
                            answered = True
                    if answered == False:
                        candidate_scores[candidate].append({question.id: 0})

        #Add Weighting
        for candidate in self.candidates:
            for question in candidate_scores[candidate]:
                for question_id, score in question.iteritems():
                    qid = str(question_id)
                    theme = 'q'+qid
                    if theme in self.multiply_questions:
                        score = score * 2                       
                        question[question_id] = score


        for candidate in self.candidates:
            print candidate.full_name()
            total = 0

            for question in candidate_scores[candidate]:
                for question_id, score in question.iteritems():
                    total = total + score
            print candidate_scores[candidate]
            print total, 'score'
            
        return redirect('fo.test', election_instance_id=self.election_instance_id)


