
# -*- coding: utf-8 -*-


from django.core.management import BaseCommand

from questions import settings
from questions.models import QuestionSet, QuestionSetQuestion, Question, Answer

class Command(BaseCommand):
    help = 'Adds questions'

    def handle(self, *args, **options):

        try:
            zuid_holland_set = QuestionSet.objects.get(name='Zuid Holland Set')
            return
        except QuestionSet.DoesNotExist:
            zuid_holland_set = QuestionSet.objects.create(name='Zuid Holland Set')
            
        try:
            limburg_set = QuestionSet.objects.get(name='Limburg Set')
            return
        except QuestionSet.DoesNotExist:
            limburg_set = QuestionSet.objects.create(name='Limburg Set')

        q1 = Question.objects.create(
            title=u'De volgende partijen maken kans op mijn stem:',
            question_type=settings.QTYPE_MODEL_PARTY,
            result_title=u'Partij',
            theme='q1',
            has_no_preference=False,
        )
        QuestionSetQuestion.objects.create(
                question=q1,
                questionset=zuid_holland_set,
                position=1,
        )
        QuestionSetQuestion.objects.create(
                question=q1,
                questionset=limburg_set,
                position=1,
        )
        print "Added basic question 1"
        
        q2 = Question.objects.create(
            title=u'Wat is uw belangrijkste streven?',
            frontend_title=u'Wat is het belangrijkste streven van uw kandidaat?',
            question_type=settings.QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE,
            result_title=u'Belangrijkste streven',
            theme='q2',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q2,
                questionset=zuid_holland_set,
                position=2,
        )
        QuestionSetQuestion.objects.create(
                question=q2,
                questionset=limburg_set,
                position=2,
        )
        q2_answers = [
            "Economische groei en innovatie",
            "Milieuvervuiling aanpakken en duurzaamheid",
            "Ontwikkeling van kunst en cultuur in de provincie",
            "Bezuinigingen effectief doorvoeren",
            "Het verbeteren van de jeugdzorg",
            "Voldoende natuur",
            "Voldoende recreatiemogelijkheden",
            "Het verbeteren van de woningmarkt",
            "Het verbeteren van de regionale bereikbaarheid",
            "Het leefbaar houden van kernen op het platteland",
            "Voldoende ontwikkelingsmogelijkheden voor de landbouw",
        ]
        for position, answer in enumerate(q2_answers):
            Answer.objects.create(
                question=q2,
                value=answer,
                frontoffice_value=None,
                position=position+1,
                )
        print "Added basic question 2"
        
        q3 = Question.objects.create(
            title=u'Waar legt u de meeste nadruk op?',
            frontend_title=u'Waar legt uw ideale kandidaat de meeste nadruk op?',
            question_type=settings.QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE,
            result_title=u'Nadruk',
            theme='q3',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q3,
                questionset=zuid_holland_set,
                position=3,
        )
        QuestionSetQuestion.objects.create(
                question=q3,
                questionset=limburg_set,
                position=3,
        )
        q3_answers = [
            "De provincie in gaan om te kijken wat er leeft bij de bevolking",
            "Zelf met initiatieven komen en deze naar voren brengen binnen de Provinciale Staten",
            "Het controleren van het beleid en de uitgaven van het bestuur van de Provincie",
            "Het behartigen van het belang van de partij en afstemming zoeken met belangenorganisaties",
            "Het behartigen van het belang van zijn/haar regio",
            
        ]
        for position, answer in enumerate(q3_answers):
            Answer.objects.create(
                question=q3,
                value=answer,
                frontoffice_value=None,
                position=position+1,
                )
        print "Added basic question 3"
        
        
        q4 = Question.objects.create(
            title=u'Mijn expertise ligt op het gebied van:',
            frontend_title=u'Waar ligt de expertise van uw kandidaat?',
            question_type=settings.QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE,
            result_title=u'Expertise',
            theme='q4',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q4,
                questionset=zuid_holland_set,
                position=4,
        )
        QuestionSetQuestion.objects.create(
                question=q4,
                questionset=limburg_set,
                position=4,
        )
        q4_answers = [
            "Ruimte ontwikkeling en inrichting",
            "Milieu, energie en klimaat",
            "Leefbare kernen op het platteland",
            "Waterbeheer",
            "Regionaal verkeer en Vervoer",
            "Regionale economie",
            "Jeugdzorg",
            "Cultuur en Monumentenzorg",
            "Bestuur en financiën",
            "Natuur en recreatie",
            "Landbouw",
        ]
        for position, answer in enumerate(q4_answers):
            Answer.objects.create(
                question=q4,
                value=answer,
                frontoffice_value=None,
                position=position+1,
                )
        print "Added basic question 4"
        
        q5 = Question.objects.create(
            title=u'Welke werkervaring heeft uw kandidaat?',
            frontend_title=u'Welke werkervaring heeft uw kandidaat?',
            question_type=settings.QTYPE_MODEL_WORK_EXPERIENCE_TYPE,
            result_title=u'Werkervaring',
            theme='q5',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q5,
                questionset=zuid_holland_set,
                position=5,
        )
        QuestionSetQuestion.objects.create(
                question=q5,
                questionset=limburg_set,
                position=5,
        )
        print "Added basic question 5"
        
        q6 = Question.objects.create(
            title=u'Heeft uw kandidaat politieke ervaring?',
            frontend_title=u'Heeft uw kandidaat politieke ervaring?',
            question_type=settings.QTYPE_MODEL_POLITICAL_EXPERIENCE_TYPE,
            result_title=u'Politieke ervaring',
            theme='q6',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q6,
                questionset=zuid_holland_set,
                position=6,
        )
        QuestionSetQuestion.objects.create(
                question=q6,
                questionset=limburg_set,
                position=6,
        )
        print "Added basic question 6"
        
        q7 = Question.objects.create(
            title=u'Ik zet mij vooral in voor:',
            frontend_title=u'Voor welke groep of groepen zet uw kandidaat zich extra in?',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE,
            result_title=u'Doelgroep(en) van de kandidaat',
            theme='q7',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q7,
                questionset=zuid_holland_set,
                position=7,
        )
        QuestionSetQuestion.objects.create(
                question=q7,
                questionset=limburg_set,
                position=7,
        )
        q7_answers = [
            "Voor inwoners van het landelijk gebied",
            "Voor inwoners van de steden",
        ]
        for position, answer in enumerate(q7_answers):
            Answer.objects.create(
                question=q7,
                value=answer,
                frontoffice_value=None,
                position=position+1,
                )
        print "Added basic question 7"
        
        q8zh = Question.objects.create(
            title=u'Ik woon in de regio:',
            frontend_title=u'In welke regio woont uw ideale kandidaat?',
            question_type=settings.QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE,
            result_title=u'Regio van de kandidaat',
            theme='q8',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q8zh,
                questionset=zuid_holland_set,
                position=8,
        )
        q8zh_answers = [
            "Alphen a.d. Rijn en omgeving",
            "Delft en omgeving, Westland",
            "Den Haag en omgeving",
            "Dordrecht en De Waarden t/m Gorinchem",
            "Duin- en bollengebied",
            "Gouda en omgeving, incl. Krimpenerwaard",
            "Leiden en omgeving",
            "Zoetermeer, Lansingerland",
            "Rotterdam en omgeving, incl. Waterweggebied",
            "Zuid-Hollandse eilanden",
            
        ]
        for position, answer in enumerate(q8zh_answers):
            Answer.objects.create(
                question=q8zh,
                value=answer,
                frontoffice_value=None,
                position=position+1,
                )
        print "Added Zuid holland question 8"
        
        q8lm = Question.objects.create(
            title=u'Ik woon in de regio:',
            frontend_title=u'In welke regio woont uw ideale kandidaat?',
            question_type=settings.QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE,
            result_title=u'Regio van de kandidaat',
            theme='q8',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q8lm,
                questionset=limburg_set,
                position=8,
        )
        q8lm_answers = [
            "Alphen a.d. Rijn en omgeving",
            "Delft en omgeving, Westland",
            "Den Haag en omgeving",
            "Dordrecht en De Waarden t/m Gorinchem",
            "Duin- en bollengebied",
            "Gouda en omgeving, incl. Krimpenerwaard",
            "Leiden en omgeving",
            "Zoetermeer, Lansingerland",
            "Rotterdam en omgeving, incl. Waterweggebied",
            "Zuid-Hollandse eilanden",
            
        ]
        for position, answer in enumerate(q8lm_answers):
            Answer.objects.create(
                question=q8lm,
                value=answer,
                frontoffice_value=None,
                position=position+1,
                )
        print "Added Limburg question 8"
        
        
        q9 = Question.objects.create(
            title=u'Ik haal mijn motivatie voornamelijk uit:',
            frontend_title=u'Waaruit haalt uw ideale kandidaat zijn of haar motivatie?',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE,
            result_title=u'Motivatie',
            theme='q9',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q9,
                questionset=zuid_holland_set,
                position=9,
        )
        QuestionSetQuestion.objects.create(
                question=q9,
                questionset=limburg_set,
                position=9,
        )
        q9_answers = [
            ("Een toekomstbestendige provincie", "Een toekomstbestendige provincie"),
            ("Het versterken van zijn/haar regio", "Het versterken van mijn regio"),
            ("Een krachtige partij", "Een krachtige partij"),
            ("Persoonlijke ontplooiing", "Persoonlijke ontplooiing"),
            ("Anders", "Anders"),
            
        ]
        for position, (fo_answer, answer) in enumerate(q9_answers):
            Answer.objects.create(
                question=q9,
                value=answer,
                frontoffice_value=fo_answer,
                position=position+1,
                )
        print "Added basic question 9"
        
        q10 = Question.objects.create(
            title=u'Mijn ideale kandidaat heeft de volgende vervolgopleiding afgerond:',
            question_type=settings.QTYPE_MODEL_EDUCATION_LEVEL,
            result_title=u'Opleiding',
            theme='q10',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q10,
                questionset=zuid_holland_set,
                position=10,
        )
        QuestionSetQuestion.objects.create(
                question=q10,
                questionset=limburg_set,
                position=10,
        )
        Answer.objects.create(
            question=q10,
            value=u'Geen vervolgopleiding',
            meta=u'ALL_OTHERS',
            frontoffice_value=u'Geen vervolgopleiding',
            position=1,
        )
        Answer.objects.create(
            question=q10,
            value=u'Middelbaar Beroepsonderwijs',
            meta=u'MBO',
            frontoffice_value=u'Middelbaar Beroepsonderwijs',
            position=2,
        )

        Answer.objects.create(
            question=q10,
            value=u'Hoger Beroepsonderwijs',
            meta=u'HBO',
            frontoffice_value=u'Hoger Beroepsonderwijs',
            position=3,
        )
        Answer.objects.create(
            question=q10,
            value=u'Wetenschappelijk Onderwijs',
            meta=u'Universitair',
            frontoffice_value=u'Wetenschappelijk Onderwijs',
            position=4,
        )
        print "Added basic question 10"
        
        q11 = Question.objects.create(
            title=u'Op welke manier speelt religie bij uw werk in de politiek?',
            frontend_title=u'Op welke manier speelt religie een rol bij uw ideale kandidaat?',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE,
            result_title=u'Religie',
            theme='q11',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q11,
                questionset=zuid_holland_set,
                position=11,
        )
        QuestionSetQuestion.objects.create(
                question=q11,
                questionset=limburg_set,
                position=11,
        )
        q11_answers = [
            ("Religie is leidend voor zijn/haar politiek handelen ", "Religie is leidend voor mijn politiek handelen "),
            ("Religie is een inspiratiebron voor zijn/haar politiek handelen", "Religie is een inspiratiebron voor mijn politiek handelen"),
            ("Religie speelt voor zijn/haar politiek handelen geen rol", "Religie speelt voor mijn politiek handelen geen rol"),
            
        ]
        for position, (fo_answer, answer) in enumerate(q11_answers):
            Answer.objects.create(
                question=q11,
                value=answer,
                frontoffice_value=fo_answer,
                position=position+1,
                )
        print "Added basic question 11"
        
        q12 = Question.objects.create(
            title=u'In welke leeftijdsgroep zit uw ideale kandidaat?',
            question_type=settings.QTYPE_MODEL_PROFILE_AGE,
            result_title=u'Leeftijd',
            theme='q12',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q12,
                questionset=zuid_holland_set,
                position=12,
        )
        QuestionSetQuestion.objects.create(
                question=q12,
                questionset=limburg_set,
                position=12,
        )
        Answer.objects.create(
            question=q12,
            value=u'30 jaar of jonger',
            meta=u':30',
            frontoffice_value=u'30 jaar of jonger',
            position=1,
        )
        Answer.objects.create(
            question=q12,
            value=u'tussen de 31 en de 55',
            meta=u'31:55',
            frontoffice_value=u'tussen de 31 en de 55',
            position=2,
        )
        Answer.objects.create(
            question=q12,
            value=u'Ouder dan 55 jaar',
            meta=u'55:',
            frontoffice_value=u'Ouder dan 55 jaar',
            position=3,
        )
        print "Added basic question 12"
        
        q13 = Question.objects.create(
            title=u'Mijn ideale kandidaat is:',
            question_type=settings.QTYPE_MODEL_PROFILE_GENDER,
            result_title=u'Geslacht',
            theme='q13',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q13,
                questionset=zuid_holland_set,
                position=13,
        )
        QuestionSetQuestion.objects.create(
                question=q13,
                questionset=limburg_set,
                position=13,
        )
        print "Added basic question 13"
 
        q14 = Question.objects.create(
            title=u'U heeft nu alle vragen beantwoord. Hieronder kunt u aangeven welke vragen u extra belangrijk vindt. Het is overigens niet verplicht extra gewicht aan bepaalde vragen te geven:',
            question_type=settings.QTYPE_MODEL_PROFILE_QUESTION_WEIGHT,
            theme='q14',
            has_no_preference=False,
        )
        QuestionSetQuestion.objects.create(
                question=q14,
                questionset=zuid_holland_set,
                position=1000,
        )
        QuestionSetQuestion.objects.create(
                question=q14,
                questionset=limburg_set,
                position=1000,
        )
        print "Added basic question 14"