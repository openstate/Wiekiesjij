# -*- coding: utf-8 -*-

import datetime

from django.core.management import BaseCommand

from questions import settings
from questions.models import QuestionSet, QuestionSetQuestion, Question, Answer

class Command(BaseCommand):
    help = 'Adds questions'
    
    def handle(self, *args, **options):
        qs1 = QuestionSet.objects.create(name='BasicSet1')
        
        
        
        q4 = Question.objects.create(
            title=u'Als gemeenteraadslid leg ik de meeste nadruk op:',
            frontend_title=u'Mijn ideale kandidaat legt binnen haar functie als gemeenteraadslid de meeste nadruk op:',
            has_no_preference=True,
            question_type=settings.QUESTION_TYPE_MULTIPLECHOICE,
            theme='q4',
        )
        qsq4 = QuestionSetQuestion.objects.create(
            question=q4,
            questionset=qs1,
            position=4,
        )
        Answer.objects.create(
            question=q4,
            value=u'Het hebben van een open oog en oor voor wat er leeft bij de burgers en organisaties in de stad en gaat daarover met hen in gesprek',
            frontoffice_value=u'Mijn kandidaat heeft een open oog en oor voor wat er leeft bij de burgers en organisaties in de stad en gaat daarover met hen in gesprek',
            position=1,
        )
        Answer.objects.create(
            question=q4,
            value=u'Het hebben goede ideeën hoe het beter kan in de stad en het naar voren brengen in de gemeenteraad hiervan',
            frontoffice_value=u'Mijn kandidaat heeft zelf goede ideeën hoe het beter kan in de stad en brengt die in de gemeenteraad naar voren',
            position=2,
        )
        Answer.objects.create(
            question=q4,
            value=u'Het controlleren of het College van B&W het beleid uitvoert en binnen het budget blijft zoals die door de gemeenteraad zijn vastgesteld',
            frontoffice_value=u'Mijn kandidaat controleert of het College van B&W het beleid uitvoert en binnen het budget blijft zoals die door de gemeenteraad zijn vastgesteld',
            position=3,
        )
        print "Added basic question 4"
        
        
        q5 = Question.objects.create(
            title=u'Ik zet mij vooral in voor:',
            frontend_title=u'Mijn ideale kandidaat zet zich vooral in voor:',
            has_no_preference=False,
            question_type=settings.QUESTION_TYPE_MULTIPLEANSWER,
            theme='q5',
        )
        qsq5 = QuestionSetQuestion.objects.create(
            question=q5,
            questionset=qs1,
            position=5,
        )
        Answer.objects.create(
            question=q5,
            value=u'Starters',
            frontoffice_value=None,
            position=1,
        )
        Answer.objects.create(
            question=q5,
            value=u'Ambtenaren',
            frontoffice_value=None,
            position=2,
        )
        Answer.objects.create(
            question=q5,
            value=u'Werknemers',
            frontoffice_value=None,
            position=3,
        )
        Answer.objects.create(
            question=q5,
            value=u'Senioren (65+)',
            frontoffice_value=None,
            position=4,
        )
        Answer.objects.create(
            question=q5,
            value=u'Ondernemers',
            frontoffice_value=None,
            position=4,
        )
        Answer.objects.create(
            question=q5,
            value=u'Minima',
            frontoffice_value=None,
            position=5,
        )
        Answer.objects.create(
            question=q5,
            value=u'Niet-werkenden',
            frontoffice_value=None,
            position=6,
        )
        Answer.objects.create(
            question=q5,
            value=u'Studenten',
            frontoffice_value=None,
            position=7,
        )
        Answer.objects.create(
            question=q5,
            value=u'Vrijwilligers',
            frontoffice_value=None,
            position=8,
        )
        print "Added basic question 5"
        
        q6 = Question.objects.create(
            title=u'Vanwege de recessie wil ik vooral bezuinigen op:',
            frontend_title=u'Vanwege de recessie moet mijn ideale kandidaat vooral willen bezuinigen op:',
            has_no_preference=True,
            question_type=settings.QUESTION_TYPE_MULTIPLEANSWER,
            theme='q6',
        )
        qsq6 = QuestionSetQuestion.objects.create(
            question=q6,
            questionset=qs1,
            position=6,
        )
        Answer.objects.create(
            question=q6,
            value=u'Werk en Inkomen',
            frontoffice_value=None,
            position=1,
        )
        Answer.objects.create(
            question=q6,
            value=u'Vestigingsklimaat',
            frontoffice_value=None,
            position=2,
        )
        Answer.objects.create(
            question=q6,
            value=u'Openbare orde en Veiligheid',
            frontoffice_value=None,
            position=3,
        )
        Answer.objects.create(
            question=q6,
            value=u'Stedelijke ontwikkeling',
            frontoffice_value=None,
            position=4,
        )
        Answer.objects.create(
            question=q6,
            value=u'Milieu & Duurzame Ontwikkeling',
            frontoffice_value=None,
            position=5,
        )
        Answer.objects.create(
            question=q6,
            value=u'Onderwijs en Jeugd',
            frontoffice_value=None,
            position=6,
        )
        Answer.objects.create(
            question=q6,
            value=u'Zorg en Volksgezondheid',
            frontoffice_value=None,
            position=7,
        )
        Answer.objects.create(
            question=q6,
            value=u'Sport',
            frontoffice_value=None,
            position=8,
        )
        Answer.objects.create(
            question=q6,
            value=u'Cultuur en Media',
            frontoffice_value=None,
            position=9,
        )
        Answer.objects.create(
            question=q6,
            value=u'Integratie en Emancipatie',
            frontoffice_value=None,
            position=10,
        )
        Answer.objects.create(
           question=q6,
            value=u'Ambtelijk apparaat',
            frontoffice_value=None,
            position=11,
        )
        print "Added basic question 6"
        
        q7 = Question.objects.create(
            title=u'Ondanks de recessie wil ik vooral investeren in:',
            frontend_title=u'Ondanks de recessie moet mijn ideale kandidaat vooral willen investeren in:',
            has_no_preference=True,
            question_type=settings.QUESTION_TYPE_MULTIPLEANSWER,
            theme='q7',
        )
        qsq7 = QuestionSetQuestion.objects.create(
            question=q7,
            questionset=qs1,
            position=7,
        )
        Answer.objects.create(
            question=q7,
            value=u'Werk en Inkomen',
            frontoffice_value=None,
            position=1,
        )
        Answer.objects.create(
            question=q7,
            value=u'Vestigingsklimaat',
            frontoffice_value=None,
            position=2,
        )
        Answer.objects.create(
            question=q7,
            value=u'Openbare orde en Veiligheid',
            frontoffice_value=None,
            position=3,
        )
        Answer.objects.create(
           question=q7,
            value=u'Stedelijke ontwikkeling',
            frontoffice_value=None,
            position=4,
        )
        Answer.objects.create(
            question=q7,
            value=u'Milieu & Duurzame Ontwikkeling',
            frontoffice_value=None,
            position=5,
        )
        Answer.objects.create(
            question=q7,
            value=u'Onderwijs en Jeugd',
            frontoffice_value=None,
            position=6,
        )
        Answer.objects.create(
            question=q7,
            value=u'Zorg en Volksgezondheid',
            frontoffice_value=None,
            position=7,
        )
        Answer.objects.create(
            question=q7,
            value=u'Sport',
            frontoffice_value=None,
            position=8,
        )
        Answer.objects.create(
            question=q7,
            value=u'Cultuur en Media',
            frontoffice_value=None,
            position=9,
        )
        Answer.objects.create(
            question=q7,
            value=u'Integratie en Emancipatie',
            frontoffice_value=None,
            position=10,
        )
        Answer.objects.create(
           question=q7,
            value=u'Ambtelijk apparaat',
            frontoffice_value=None,
            position=11,
        )
        print "Added basic question 7"
        
        q8 = Question.objects.create(
            title=u'U woont:',
            frontend_title=u'Mijn ideale kandidaat woont:',
            has_no_preference=False,
            question_type=settings.QUESTION_TYPE_MULTIPLECHOICE,
            theme='q8',
        )
        qsq8 = QuestionSetQuestion.objects.create(
            question=q8,
            questionset=qs1,
            position=8,
        )
        Answer.objects.create(
           question=q8,
            value=u'Minder dan 1 jaar in de gemeente',
            frontoffice_value=None,
            position=1,
        )
        Answer.objects.create(
           question=q8,
            value=u'1 tot 4 jaar in de gemeente',
            frontoffice_value=None,
            position=2,
        )
        Answer.objects.create(
           question=q8,
            value=u'4 tot 10 jaar in de gemeente',
            frontoffice_value=None,
            position=3,
        )
        Answer.objects.create(
           question=q8,
            value=u'Uw hele leven in de gemeente',
            frontoffice_value=u'zijn/haar hele leven in de gemeente',
            position=4,
        )
        print "Added basic question 8"
        