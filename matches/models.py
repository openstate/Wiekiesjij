from django.db import models
from questions.models import Question, Answer
from elections.models import Party

class PoliticianAnswerCache(models.Model):
    class Meta:
        db_table = 'pol_answer_cache'

    @staticmethod
    def fetch():
        '''
        TODO - translate from PHP
        '''
        pass

class Match:
    @staticmethod
    def calculate_matches(parties, themes, answer_tuples):
        '''
        parties - list of parties (ids) -- come from wizard, filled in by user
        themes - list of themes -- come from wizard, filled in by user
        answer_tuples - list of user answers -- come from wizard, filled in by user
        '''

        for ans in answer_tuples:
            if ans == -1:
                answer_tuples.remove(ans)

        # TODO translate from PHP
        answers_cache = PoliticianAnswerCache.fetch()

        if not answers_cache:
            raise Exception

        questions = Question.objects.filter(id__in=(','.join(map(lambda x: int(x[0]), answer_tuples))))

        answers = Answer.objects.filter(id__in=(','.join(map(lambda x: int(x[1]), answer_tuples))))

        question_subset = []
        for tuple in answer_tuple:
            if answers[tuple[1]].get_value() != '':
                question_subset.append(tuple[0])

        total_score = 0
        for qid in question_subset:
            question = questions[qid]
            question_rank = ((2.0) if (question.theme in themes) else (1.0))
            total_score += question.weight * ((2.0 if (question.theme in themes) else 1.0) if (question.theme != '') else 1.0)

        if 0 == total_score:
            result = []
            return result

        scores = []
        detail_scores = []

        for tuple in answer_tuples:
            question = questions[tuple[0]]
            answer = answeres[tuple[1]]
            ans_value = answer.get_value()
            factor = (2.0 if (question.theme in themes) else 1.0) if (question.theme != '') else 1.0
            range = ans_value.split('-', 1)
            if 1 == len(range):
                list = ans_value.split('/')
            for politician_id in answer_cache:
                pol_answer = answer_cache[politician_id][question.id] if (question.id in answer_cache[politician_id]) else None

                cnt = 0
                if len(range) > 1:
                    for ans in pol_answer:
                        if range[0] <= ans and ans <= range[1]
                            cnt += 1
                else:
                    for ans in list:
                        if ans in pol_answer:
                            cnt += 1

                sc = factor * question.weight * cnt / len(pol_answer)
                if question.id not in detail_scores[politician_id]:
                    detail_scores[politician_id][question.id] = sc
                else:
                    detail_scores[politician_id][question.id] += sc

                if politician_id not in scores:
                    scores[politician_id] = 0

                scores[politician_id] += sc

        
        '''
        asort($scores);
		$scores = array_reverse($scores, true);
		$scores = array_slice($scores, 0, $limit, true);

		if (!$scores) return array();

		foreach ($scores as $key => &$val)
			$val = array(
				'politician_id' => $key,
				'score' => (int) round($val / $totalScore * 100),
				'detail' => $detailScores[$key]
			);
		unset($val);

		return array_values($scores);
        '''

'''
TODO - move this finally to the test
'''