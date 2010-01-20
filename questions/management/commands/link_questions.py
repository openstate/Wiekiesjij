# -*- coding: utf-8 -*-

from django.core.management import BaseCommand

from elections.models import ElectionInstance, ElectionInstanceQuestion 

from questions.models import QuestionSet, QuestionSetQuestion

class Command(BaseCommand):
    help = 'Links the BasicSet1 to the election instances without questions and gives haaren the extra questions'
    
    def handle(self, *args, **options):
        try:
            qs = QuestionSet.objects.get(name='BasicSet1')
        except qs.DoesNotExist:
            print "No questionset found."
            return 1
        
        for ei in ElectionInstance.objects.all():

            for qsq in qs.questionsetquestion_set.order_by('position'):
                
                #Skip question 6 for den haag
                if qsq.question.theme == 'q6' and ei.council.region.lower() == 'den haag':
                    continue
                    
                if ei.questions.filter(pk=qsq.question.pk).count() != 0:
                    continue
                
                ElectionInstanceQuestion.objects.create(
                    election_instance = ei,
                    position = qsq.position,
                    question=qsq.question,
                    locked=True,
                )
            # Haaren gets some extra questions
            if ei.council.region.lower() == 'haaren':
                try:
                    qs_haren = QuestionSet.objects.get(name='HaarenExtraQuestions')
                except qs.DoesNotExist:
                    print "No questionset found for Haaren."
                    return 1
                    
                for qsq in qs_haren.questionsetquestion_set.order_by('position'):
                
                    if ei.questions.filter(pk=qsq.question.pk).count() != 0:
                        continue
                        
                    ElectionInstanceQuestion.objects.create(
                        election_instance = ei,
                        position = qsq.position,
                        question=qsq.question,
                        locked=False,
                    )
                
                