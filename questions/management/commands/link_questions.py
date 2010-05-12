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
                
                if ei.questions.filter(pk=qsq.question.pk).count() != 0:
                    continue
                
                ElectionInstanceQuestion.objects.create(
                    election_instance = ei,
                    position = qsq.position,
                    question=qsq.question,
                    locked=True,
                )
                