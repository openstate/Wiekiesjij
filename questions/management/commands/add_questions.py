# -*- coding: utf-8 -*-

import datetime

from django.core.management import BaseCommand

from questions import settings
from questions.models import QuestionSet, QuestionSetQuestion, Question, Answer

class Command(BaseCommand):
    help = 'Adds questions'
    
    def handle(self, *args, **options):
        
        try:
            qs1 = QuestionSet.objects.get(name='BasicSet1')
        except QuestionSetDoesNotExist:
            qs1 = None
            
        if qs1 is None:
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
                value=u'Het hebben van een open oog en oor voor wat er leeft bij de burgers en organisaties in de stad en daarover met hen in gesprek gaan',
                frontoffice_value=u'Mijn kandidaat heeft een open oog en oor voor wat er leeft bij de burgers en organisaties in de stad en gaat daarover met hen in gesprek',
                position=1,
            )
            Answer.objects.create(
                question=q4,
                value=u'Het hebben van goede ideeën over hoe het beter kan in de stad en het naar voren brengen hiervan in de gemeenteraad',
                frontoffice_value=u'Mijn kandidaat heeft zelf goede ideeën hoe het beter kan in de stad en brengt die in de gemeenteraad naar voren',
                position=2,
            )
            Answer.objects.create(
                question=q4,
                value=u'Ik controleer of het College van B&W het beleid uitvoert zoals dat door de gemeenteraad is vastgesteld',
                frontoffice_value=u'Mijn kandidaat controleert of het College van B&W het beleid uitvoert zoals die door de gemeenteraad is vastgesteld',
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
                title=u'Vanwege de economische recessie wil ik vooral bezuinigen op:',
                frontend_title=u'In deze tijden van economische recessie moet mijn ideale kandidaat vooral willen bezuinigen op:',
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
                title=u'Ik woon:',
                frontend_title=u'Mijn ideale kandidaat woont:',
                has_no_preference=False,
                question_type=settings.QUESTION_TYPE_MULTIPLECHOICE,
                theme='q7',
            )
            qsq8 = QuestionSetQuestion.objects.create(
                question=q7,
                questionset=qs1,
                position=7,
            )
            Answer.objects.create(
               question=q7,
                value=u'Minder dan 1 jaar in de gemeente',
                frontoffice_value=None,
                position=1,
            )
            Answer.objects.create(
               question=q7,
                value=u'1 tot 4 jaar in de gemeente',
                frontoffice_value=None,
                position=2,
            )
            Answer.objects.create(
               question=q7,
                value=u'4 tot 10 jaar in de gemeente',
                frontoffice_value=None,
                position=3,
            )
            Answer.objects.create(
               question=q7,
                value=u'Langer dan 10 jaar in de gemeente',
                frontoffice_value=None,
                position=4,
            )
            Answer.objects.create(
               question=q7,
                value=u'Uw hele leven in de gemeente',
                frontoffice_value=u'zijn/haar hele leven in de gemeente',
                position=5,
            )
            print "Added basic question 7"
        
        
        #extra questions
        qs1 = QuestionSet.objects.get(name='BasicSet1')
        
        try:
            q3 = Question.objects.get(theme='q3')
        except Question.DoesNotExist:
            q3 = None
        
        if q3 is None:
            q3 = Question.objects.create(
                title=u'Ik heb kennis van:',
                frontend_title=u'Mijn ideale kandidaat heeft kennis van:',
                has_no_preference=True,
                question_type=settings.QUESTION_TYPE_MULTIPLEANSWER,
                theme='q3',
            )
            qsq3 = QuestionSetQuestion.objects.create(
                question=q3,
                questionset=qs1,
                position=3,
            )
            Answer.objects.create(
               question=q3,
                value=u'De bestuurlijke organisatie',
                frontoffice_value=None,
                position=1,
            )
            Answer.objects.create(
                question=q3,
                value=u'Openbare orde & veiligheid',
                frontoffice_value=None,
                position=2,
            )
            Answer.objects.create(
                question=q3,
                value=u'Infrastructuur & vervoer',
                frontoffice_value=None,
                position=3,
            )
            Answer.objects.create(
                question=q3,
                value=u'Ruimtelijke Ordening & wonen',
                frontoffice_value=None,
                position=4,
            )
            Answer.objects.create(
                question=q3,
                value=u'Sociale zaken',
                frontoffice_value=None,
                position=5,
            )
            Answer.objects.create(
                question=q3,
                value=u'Cultuur & recreatie',
                frontoffice_value=None,
                position=6,
            )
            Answer.objects.create(
                question=q3,
                value=u'Onderwijs & welzijn' ,
                frontoffice_value=None,
                position=7,
            )
            Answer.objects.create(
                question=q3,
                value=u'Natuur & milieu',
                frontoffice_value=None,
                position=8,
            )
            Answer.objects.create(
                question=q3,
                value=u'Financiën & economische zaken',
                frontoffice_value=None,
                position=9,
            )
            print "Added basic question 3"
            
        try:
            q9 = Question.objects.get(theme='q9')
        except Question.DoesNotExist:
            q9 = None

        if q9 is None:
            q9 = Question.objects.create(
                title=u'Mijn dagelijkse bezigheid, naast mijn functie als raadslid is:',
                frontend_title=u'De dagelijkse bezigheid, naast haar functie als raadslid, van mijn ideale kandidaat is:',
                has_no_preference=True,
                question_type=settings.QUESTION_TYPE_MULTIPLECHOICE,
                theme='q9',
            )
            qsq9 = QuestionSetQuestion.objects.create(
                question=q9,
                questionset=qs1,
                position=10,
            )
            Answer.objects.create(
                question=q9,
                value=u'Werkzaam in loondienst',
                frontoffice_value=None,
                position=1,
            )
            Answer.objects.create(
                question=q9,
                value=u'Zelfstandig ondernemer',
                frontoffice_value=None,
                position=2,
            )
            Answer.objects.create(
                question=q9,
                value=u'Werkzaam in de publieke sector',
                frontoffice_value=None,
                position=3,
            )
            Answer.objects.create(
                question=q9,
                value=u'Vrijwilliger',
                frontoffice_value=None,
                position=4,
            )
            Answer.objects.create(
                question=q9,
                value=u'Huisvrouw of huisman',
                frontoffice_value=None,
                position=5,
            )
            Answer.objects.create(
                question=q9,
                value=u'Bezig met een opleiding',
                frontoffice_value=None,
                position=6,
            )
            Answer.objects.create(
                question=q9,
                value=u'Geen andere functie',
                frontoffice_value=None,
                position=7,
            )
            print "Added basic question 9"