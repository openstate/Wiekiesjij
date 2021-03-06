# -*- coding: utf-8 -*-

from django.core.management import BaseCommand

from elections.models import ElectionInstance, ElectionInstanceQuestion

from questions.models import QuestionSet, QuestionSetQuestion

class Command(BaseCommand):
    help = 'Links the Landelijk Set to the election instances without questions and gives haaren the extra questions'

    def handle(self, *args, **options):
        try:
            qs = QuestionSet.objects.get(name='TEST Landelijk Set')
            print qs
        except QuestionSet.DoesNotExist:
            print "No questionset found."
            return

        for ei in ElectionInstance.objects.all():

            print ei
            for qsq in qs.questionsetquestion_set.order_by('position'):

                if ei.questions.filter(pk=qsq.question.pk).count() != 0:
                    print "%s has questions" % ei
                    continue

                print "Linking question %s, position %s to ElectionInstance %s" % (qsq.question, qsq.position, ei)

                if False:
                    ElectionInstanceQuestion.objects.create(
                        election_instance = ei,
                        position = qsq.position,
                        question=qsq.question,
                        locked=True,
                    )
