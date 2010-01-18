
# -*- coding: utf-8 -*-

import datetime

from django.core.management import BaseCommand

from questions import settings
from questions.models import QuestionSet, QuestionSetQuestion, Question, Answer

class Command(BaseCommand):
    help = 'Adds questions'

    def handle(self, *args, **options):


        q1 = Question.objects.create(
            title=u'De volgende partijen maken kans op mijn stem:',
            question_type=settings.QTYPE_MODEL_PARTY,
            theme='q1',
            has_no_preference=False,
        )
        print "Added basic question 1"
        q2 = Question.objects.create(
            title=u'Mijn ideale kandidaat heeft:',
            question_type=settings.QTYPE_MODEL_WORK_EXPERIENCE_YEARS,
            theme='q1',
            has_no_preference=True,
        )
        Answer.objects.create(
            question=q2,
            value=u'Geen ervaring als volksvertegenwoordiger',
            meta=u'0',
            frontoffice_value=u'Geen ervaring als volksvertegenwoordiger',
            position=1,
        )
        Answer.objects.create(
            question=q2,
            value=u'1 tot 4 jaar ervaring als volksvertegenwoordiger',
            meta=u'1:4',
            frontoffice_value=u'1 tot 4 jaar ervaring als volksvertegenwoordiger',
            position=2,
        )
        Answer.objects.create(
            question=q2,
            value=u'4 tot 8 jaar ervaring als volksvertegenwoordiger',
            meta=u'4:8',
            frontoffice_value=u'4 tot 8 jaar ervaring als volksvertegenwoordiger',
            position=3,
        )
        Answer.objects.create(
            question=q2,
            value=u'Langer dan 8 jaar ervaring als volksvertegenwoordiger',
            meta=u'8:G',
            frontoffice_value=u'Langer dan 8 jaar ervaring als volksvertegenwoordiger',
            position=4,
        )
        print "Added basic question 2"


        
        q10 = Question.objects.create(
            title=u'Mijn ideale kandidaat heeft de volgende vervolgopleiding afgerond:',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISMULTICHOICE,
            theme='q11',
            has_no_preference=True,
        )
        Answer.objects.create(
            question=q10,
            value=u'Wetenschappelijk Onderwijs',
            meta=u'Universitair',
            frontoffice_value=u'Wetenschappelijk Onderwijs',
            position=1,
        )
        Answer.objects.create(
            question=q10,
            value=u'Hoger Beroepsonderwijs',
            meta=u'HBO',
            frontoffice_value=u'Hoger Beroepsonderwijs',
            position=2,
        )
        Answer.objects.create(
            question=q10,
            value=u'Middelbaar Beroepsonderwijs',
            meta=u'MBO',
            frontoffice_value=u'Middelbaar Beroepsonderwijs',
            position=3,
        )
        Answer.objects.create(
            question=q10,
            value=u'Geen vervolgopleiding',
            meta=u'ALL_OTHERS',
            frontoffice_value=u'Geen vervolgopleiding',
            position=4,
        )
        print "Added basic question 10"


        q11 = Question.objects.create(
            title=u'Mijn ideale kandidaat behoort tot de volgende geloofsgemeenschap:',
            question_type=settings.QTYPE_MODEL_PROFILE_RELIGION,
            theme='q11',
            has_no_preference=True,
        )


        print "Added basic question 11"

        q12 = Question.objects.create(
            title=u'Mijn ideale kandidaat heeft als hobby:',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISMULTICHOICE,
            theme='q12',
            has_no_preference=True,
        )
        Answer.objects.create(
            question=q12,
            value=u'Lezen',
            frontoffice_value=u'Lezen',
            position=1,
        )

        Answer.objects.create(
            question=q12,
            value=u'Koken',
            frontoffice_value=u'Koken',
            position=2,
        )

        Answer.objects.create(
            question=q12,
            value=u'Reizen',
            frontoffice_value=u'Reizen',
            position=3,
        )

        Answer.objects.create(
            question=q12,
            value=u'Computergames',
            frontoffice_value=u'Computergames',
            position=4,
        )

        Answer.objects.create(
            question=q12,
            value=u'Sport',
            frontoffice_value=u'Sport',
            position=5,
        )

        Answer.objects.create(
            question=q12,
            value=u'Schilderen',
            frontoffice_value=u'Schilderen',
            position=6,
        )

        Answer.objects.create(
            question=q12,
            value=u'Films',
            frontoffice_value=u'Films',
            position=7,
        )

        Answer.objects.create(
            question=q12,
            value=u'Klussen',
            frontoffice_value=u'Klussen',
            position=8,
        )

        Answer.objects.create(
            question=q12,
            value=u'Handwerken',
            frontoffice_value=u'Handwerken',
            position=9,
        )

        Answer.objects.create(
            question=q12,
            value=u'TV-kijken',
            frontoffice_value=u'TV-kijken',
            position=10,
        )

        Answer.objects.create(
            question=q12,
            value=u'Spelletjes doen',
            frontoffice_value=u'Spelletjes doen',
            position=11,
        )

        Answer.objects.create(
            question=q12,
            value=u'Muziek',
            frontoffice_value=u'Muziek',
            position=12,
        )

        Answer.objects.create(
            question=q12,
            value=u'Tuinieren',
            frontoffice_value=u'Tuinieren',
            position=13,
        )

        print "Added basic question 12"

        q13 = Question.objects.create(
            title=u'Mijn ideale kandidaat is:',
            question_type=settings.QTYPE_MODEL_PROFILE_AGE,
            theme='q13',
            has_no_preference=True,
        )
        Answer.objects.create(
            question=q13,
            value=u'18 tot 25 jaar',
            meta=u'18:25',
            frontoffice_value=u'18 tot 25 jaar',
            position=1,
        )
        Answer.objects.create(
            question=q13,
            value=u'25 tot 35 jaar',
            meta=u'25:35',
            frontoffice_value=u'25 tot 35 jaar',
            position=2,
        )
        Answer.objects.create(
            question=q13,
            value=u'35 tot 50 jaar',
            meta=u'35:50',
            frontoffice_value=u'35 tot 50 jaar',
            position=3,
        )
        Answer.objects.create(
            question=q13,
            value=u'50 tot 65 jaar',
            meta=u'50:65',
            frontoffice_value=u'50 tot 65 jaar',
            position=4,
        )
        Answer.objects.create(
            question=q13,
            value=u'ouder dan 65 jaar',
            meta=u'65:G',
            frontoffice_value=u'ouder dan 65 jaar',
            position=5,
        )
        print "Added basic question 13"
        q14 = Question.objects.create(
            title=u'Mijn ideale kandidaat is:',
            question_type=settings.QTYPE_MODEL_PROFILE_GENDER,
            theme='q14',
            has_no_preference=False,
        )
        print "Added basic question 14"