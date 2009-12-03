from django.db import models
from questions.models import Question, Answer
from political_profiles.models import PoliticianProfile
from elections.models import Party
from django.contrib.auth.models import User

class PoliticianAnswerCache(models.Model):
    politician = models.ForeignKey(User, related_name="%(class)s", unique=True, verbose_name=_('User'))
    question = models.ForeignKey(Question, related_name="%(class)s", unique=True, verbose_name=_('Question'))
    answer = models.CharField(_('Answer'), related_name="%(class)s", max_length=255, verbose_name=_('Answer'))

    class Meta:
        db_table = 'pol_answer_cache'
        unique_together = (('politician', 'question'),)

    @staticmethod
    def fetch(*args, **kargs):
        '''
        TODO - translated from PHP. Test this well.
        '''

        '''
        $args = func_get_args();
		$where = $args ? ' '.call_user_func_array(array(self::db(), 'formatQuery'), $args) : '';
		$raw = self::db()->query('SELECT t.* FROM %t t%l', self::$tableName, $where)->fetchAllRows();
		$data = array();
		foreach ($raw as $row)
			$data[$row['politician_id']][$row['question_id']][] = $row['answer'];
		return $data;
        '''

        where = '' if not args else args
        raw = PoliticianAnswerCache.objects.filter(where)
        data = {}
        for row in raw:
            data[row.politician_id] = {}
            data[row.politician_id][row.question_id] = row.answer
        return data

    @staticmethod
    def invalidate_politician(self, politician_id):
        return PoliticianAnswerCache.objects.filter(politician_id=politician_id).delete()

    @staticmethod
    def invalidate_question(self, question_id):
        return PoliticianAnswerCache.objects.filter(question_id=question_id).delete()

    @staticmethod
    def revalidate(self, politician_id):
        '''
        TODO - change this, as for now it won't work at all.
        '''
        questions = Question.objects.filter()

        invalidated_entries = PoliticianAnswerCache.objects.filter()
        if politician_id:
            invalidated_entries = invalidated_entries.filter(politician_id=politician_id)

        politician = PoliticianProfile.objects.filter(user__in=(','.join(map(lambda x: int(x.politician_id), invalidated_entries))))

        politician = map(lambda x: {int(x.id): x}, politician)

        for pol in politician:
            for qid in invalidated_entries[pol.id]:
                pass
        '''
        require_once('Question.class.php');
		require_once('PoliticianExtended.class.php');
		$question = new Question();
		$questions = $question->select()->get();

		$invalidatedEntries = self::db()->query('
			SELECT v.question_id, v.politician_id
			FROM (
				SELECT p.id AS politician_id, q.id AS question_id
				FROM politicians_extended p, questions q
			) v LEFT JOIN %t t
			USING (question_id, politician_id)
			WHERE t.id IS NULL'.
			($politicianId ? ' AND v.politician_id = %' : ''),
			self::$tableName, $politicianId
		)->fetchAllCells(false, 'politician_id');

		if (!$invalidatedEntries) return;

		$politician = new PoliticianExtended();
		$politicians = $politician->select()->where('t1.id IN (%l)', implode(', ', array_map('intval', array_keys($invalidatedEntries))))->get();

		foreach ($politicians as $pol)
			foreach ($invalidatedEntries[$pol->id] as $qid) {
				$question = $questions[$qid];
				if (!$question->field)
					$answer = array();
				else {
					@list($field, $subfield) = explode('.', $question->field, 2);
					$answer = $pol->$field;
					if ($answer instanceof RecordCollection)
						$answer = $answer->toArray();
					if ($subfield)
						if (is_array($answer))
							$answer = array_map(create_function('$x', 'return $x->'.$subfield.';'), $answer);
						else
							$answer = array($answer->$subfield);
					if (!is_array($answer))
						$answer = array($answer);
					$answer = array_filter(array_unique(array_flatten($answer)), 'is_scalar');
				}
				if (!$answer) $answer = array(null);
				foreach ($answer as $ans)
					self::db()->query(
						'INSERT INTO %t (politician_id, question_id, answer) VALUES (%, %, %)',
						self::$tableName, $pol->id, $qid, $ans
					);
			}
        '''




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

        tmp_scores = sorted(dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)[0:limit]

        if not tmp_scores:
            return []

        scores = []
        for key, val in tmp_scores:
            scores.append({'politician_id': key,
                           'score': int(round(val / total_score * 100)),
                           'detail': detail_scores[key]})

        del tmp_scores

        return scores

'''
TODO - write a test for this.
'''