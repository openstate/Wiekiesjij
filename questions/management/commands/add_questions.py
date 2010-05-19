
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
            return
        except QuestionSet.DoesNotExist:
            qs1 = QuestionSet.objects.create(name='BasicSet1')

        q1 = Question.objects.create(
            title=u'De volgende partijen maken kans op mijn stem:',
            question_type=settings.QTYPE_MODEL_PARTY,
            theme='q1',
            has_no_preference=False,
        )
        qsq1 = QuestionSetQuestion.objects.create(
                question=q1,
                questionset=qs1,
                position=1,
        )
        print "Added basic question 1"
        
        q2 = Question.objects.create(
            title=u'Wat is de belangrijkste uitdaging waar Nederland voor staat?',
            frontend_title=u'De belangrijkste uitdaging(en) waarvoor Nederland staat is:',
            question_type=settings.QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE,
            result_title=u'Belangrijkste uitdaging(en) voor Nederland',
            theme='q2',
            has_no_preference=True,
        )
        qsq2 = QuestionSetQuestion.objects.create(
                question=q2,
                questionset=qs1,
                position=2,
        )
        q2_answers = [
            "Economische groei, innovatie en concurrentie met het buitenland",
            "Integratie van minderheden",
            "Vertrouwen in de politiek binnen de samenleving",
            "Duurzaamheid en het klimaatprobleem aanpakken",
            "Begrotingstekort en staatsschuld terugdringen",
            "Voldoende werkgelegenheid",
            "Sociale voorzieningen in stand houden",
            "Misdaad bestrijden, veiligheid op straat",
            "Eerlijk verdelen van welvaart",
            "Bijdragen aan wereldvrede",
            "Verbeteren dierenwelzijn",
            "Betere gezondheidszorg",
            "Beter onderwijs",
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
            title=u'Welke partijen zitten in uw regeringscoalitie:',
            frontend_title=u'In mijn regeringscoalitie zitten de volgende partijen:',
            question_type=settings.QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE,
            result_title=u'Regeringscoalitie',
            theme='q3',
            has_no_preference=True,
        )
        qsq3 = QuestionSetQuestion.objects.create(
                question=q3,
                questionset=qs1,
                position=3,
        )
        q3_answers = [
            "CDA",
            "PvdA",
            "SP",
            "VVD",
            "PVV",
            "GroenLinks",
            "ChristenUnie",
            "D66",
            "Partij voor de Dieren",
            "Staatkundig Gereformeerde Partij",
            "Nieuw Nederland",
            "Trots op Nederland",
            "Partij voor Mens en Spirit",
            "Heel Nederland",
            "Partij één",
            "Lijst 17",
            "Piratenpartij",
            "Evangelische Partij Nederland",
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
            title=u'Ik steun de volgende kandidaat-premier:',
            frontend_title=u'Mijn kandidaat ziet het liefst als premier:',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE,
            result_title=u'Premier',
            theme='q4',
            has_no_preference=True,
        )
        qsq4 = QuestionSetQuestion.objects.create(
                question=q4,
                questionset=qs1,
                position=4,
        )
        q4_answers = [
            "Job Cohen (PvdA)",
            "Jan Peter Balkenende (CDA)",
            "Mark Rutte (VVD)",
            "Geert Wilders (PVV)",
            "Anders",
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
            title=u'Als parlementariër leg ik de meeste nadruk op:',
            frontend_title=u'Mijn ideale kandidaat moet de meeste nadruk leggen op:',
            question_type=settings.QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE,
            result_title=u'De nadruk van de kandidaat',
            theme='q5',
            has_no_preference=True,
        )
        qsq5 = QuestionSetQuestion.objects.create(
                question=q5,
                questionset=qs1,
                position=5,
        )
        q5_answers = [
            ("Het land in gaan om te kijken wat er leeft bij de bevolking", "Het land in gaan om te kijken wat er leeft bij de bevolking"),
            ("Zelf goede ideeën verzinnen en deze naar voren brengen in de Kamer", "Zelf goede ideeën verzinnen en deze naar voren brengen in de Kamer"),
            ("Het controleren van het beleid en de uitgaven van de regering", "Het controleren van het beleid en de uitgaven van de regering"),
            ("Het behartigen van het belang van de partij en afstemming zoeken met belangenorganisaties", "Het behartigen van het belang van de partij en afstemming zoeken met belangenorganisaties"),
            ("Het behartigen van het belang van zijn/haar regio", "Het behartigen van het belang van mijn regio"),
        ]
        for position, (fo_answer, answer) in enumerate(q5_answers):
            Answer.objects.create(
                question=q5,
                value=answer,
                frontoffice_value=fo_answer,
                position=position+1,
                )
        print "Added basic question 5"
        
        q6 = Question.objects.create(
            title=u'Ik heb kennis van:',
            frontend_title=u'Waar ligt de expertise van uw kandidaat?',
            question_type=settings.QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE,
            result_title=u'Expertise',
            theme='q6',
            has_no_preference=True,
        )
        qsq6 = QuestionSetQuestion.objects.create(
                question=q6,
                questionset=qs1,
                position=6,
        )
        q6_answers = [
            "Burger en bestuur",
            "Economie en financiën",
            "Sociale zaken en werkgelegenheid",
            "Onderwijs, cultuur en wetenschap",
            "Integratie, immigratie en inburgering",
            "Volkshuisvesting en ruimtelijke ordening",
            "Verkeer en vervoer",
            "Landbouw, milieu en natuur",
            "Volksgezondheid, welzijn en sport",
            "Openbare orde en veiligheid",
            "Buitenlandse zaken, ontwikkelingssamenwerking en defensie",
        ]
        for position, answer in enumerate(q6_answers):
            Answer.objects.create(
                question=q6,
                value=answer,
                frontoffice_value=None,
                position=position+1,
                )
        print "Added basic question 6"
        
        q7 = Question.objects.create(
            title=u'Welke werkervaring heeft uw kandidaat?',
            frontend_title=u'Welke werkervaring heeft uw kandidaat?',
            question_type=settings.QTYPE_MODEL_WORK_EXPERIENCE_TYPE,
            result_title=u'Werkervaring',
            theme='q7',
            has_no_preference=True,
        )
        qsq7 = QuestionSetQuestion.objects.create(
                question=q7,
                questionset=qs1,
                position=7,
        )
        print "Added basic question 7"
        
        q8 = Question.objects.create(
            title=u'Heeft uw kandidaat politieke ervaring?',
            frontend_title=u'Heeft uw kandidaat politieke ervaring?',
            question_type=settings.QTYPE_MODEL_POLITICAL_EXPERIENCE_TYPE,
            result_title=u'Politieke ervaring',
            theme='q8',
            has_no_preference=True,
        )
        qsq8 = QuestionSetQuestion.objects.create(
                question=q8,
                questionset=qs1,
                position=8,
        )
        print "Added basic question 8"
        
        q9 = Question.objects.create(
            title=u'Ik zet mij vooral in voor:',
            frontend_title=u'Voor welke groep of groepen zet uw kandidaat zich extra in?',
            question_type=settings.QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE,
            result_title=u'Doelgroep(en) van de kandidaat',
            theme='q9',
            has_no_preference=True,
        )
        qsq9 = QuestionSetQuestion.objects.create(
                question=q9,
                questionset=qs1,
                position=9,
        )
        q9_answers = [
            "Zelfstandig ondernemers",
            "Werkgevers",
            "Werknemers",
            "Uitkeringsgerechtigden",
            "Jongeren of studenten",
            "Gezinnen",
            "Ouderen",
            "Minderheden",
            "Chronisch zieken en gehandicapten",
        ]
        for position, answer in enumerate(q9_answers):
            Answer.objects.create(
                question=q9,
                value=answer,
                frontoffice_value=None,
                position=position+1,
                )
        print "Added basic question 9"
        
        q10 = Question.objects.create(
            title=u'Ik haal mijn persoonlijke motivatie voornamelijk uit het streven naar:',
            frontend_title=u'Mijn kandidaat haalt zijn persoonlijke motivatie uit het streven naar:',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE,
            result_title=u'Persoonlijke motivatie',
            theme='q10',
            has_no_preference=True,
        )
        qsq10 = QuestionSetQuestion.objects.create(
                question=q10,
                questionset=qs1,
                position=10,
        )
        q10_answers = [
            ("Een betere wereld","Een betere wereld"),
            ("Een sterker en beter Nederland","Een sterker en beter Nederland"),
            ("Het versterken van zijn/haar regio","Het versterken van mijn regio"),
            ("Een krachtige partij","Een krachtige partij"),
            ("Persoonlijke ontplooiing","Persoonlijke ontplooiing"),
            ("Anders","Anders"),
        ]
        for position, (fo_answer, answer) in enumerate(q10_answers):
            Answer.objects.create(
                question=q10,
                value=answer,
                frontoffice_value=fo_answer,
                position=position+1,
                )
        print "Added basic question 10"
        
        q11 = Question.objects.create(
            title=u'Mijn ideale kandidaat heeft de volgende vervolgopleiding afgerond:',
            question_type=settings.QTYPE_MODEL_EDUCATION_LEVEL,
            result_title=u'Opleiding',
            theme='q11',
            has_no_preference=True,
        )
        qsq11= QuestionSetQuestion.objects.create(
                question=q11,
                questionset=qs1,
                position=11,
        )
        Answer.objects.create(
            question=q11,
            value=u'Geen vervolgopleiding',
            meta=u'ALL_OTHERS',
            frontoffice_value=u'Geen vervolgopleiding',
            position=1,
        )
        Answer.objects.create(
            question=q11,
            value=u'Middelbaar Beroepsonderwijs',
            meta=u'MBO',
            frontoffice_value=u'Middelbaar Beroepsonderwijs',
            position=2,
        )

        Answer.objects.create(
            question=q11,
            value=u'Hoger Beroepsonderwijs',
            meta=u'HBO',
            frontoffice_value=u'Hoger Beroepsonderwijs',
            position=3,
        )
        Answer.objects.create(
            question=q11,
            value=u'Wetenschappelijk Onderwijs',
            meta=u'Universitair',
            frontoffice_value=u'Wetenschappelijk Onderwijs',
            position=4,
        )
        print "Added basic question 11"
        
        q12 = Question.objects.create(
            title=u'Op welke manier speelt religie bij uw werk in de politiek?',
            frontend_title=u'Op welke manier speelt religie een rol bij uw ideale kandidaat?',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE,
            result_title=u'Religie',
            theme='q12',
            has_no_preference=True,
        )
        qsq12 = QuestionSetQuestion.objects.create(
                question=q12,
                questionset=qs1,
                position=12,
        )
        q12_answers = [
            ("Religie is leidend voor zijn/haar politiek handelen", "Religie is leidend voor mijn politiek handelen"),
            ("Religie is een inspiratiebron voor zijn/haar politiek handelen", "Religie is een inspiratiebron voor mijn politiek handelen"),
            ("Religie inspireert hem/haar persoonlijk", "Religie inspireert mij persoonlijk"),
            ("Religie speelt voor hem/haar geen rol", "Religie speelt voor mij geen rol"),
        ]
        for position, (fo_answer, answer) in enumerate(q12_answers):
            Answer.objects.create(
                question=q12,
                value=answer,
                frontoffice_value=fo_answer,
                position=position+1,
                )
        print "Added basic question 12"
        
        q13 = Question.objects.create(
            title=u'In welke leeftijdsgroep zit uw ideale kandidaat?',
            question_type=settings.QTYPE_MODEL_PROFILE_AGE,
            result_title=u'Leeftijd',
            theme='q13',
            has_no_preference=True,
        )
        qsq13 = QuestionSetQuestion.objects.create(
                question=q13,
                questionset=qs1,
                position=13,
        )
        Answer.objects.create(
            question=q13,
            value=u'30 jaar of jonger',
            meta=u':30',
            frontoffice_value=u'30 jaar of jonger',
            position=1,
        )
        Answer.objects.create(
            question=q13,
            value=u'tussen de 31 en de 55',
            meta=u'31:55',
            frontoffice_value=u'tussen de 31 en de 55',
            position=2,
        )
        Answer.objects.create(
            question=q13,
            value=u'Ouder dan 55 jaar',
            meta=u'55:',
            frontoffice_value=u'Ouder dan 55 jaar',
            position=3,
        )
        print "Added basic question 13"
        
        q14 = Question.objects.create(
            title=u'Mijn ideale kandidaat is:',
            question_type=settings.QTYPE_MODEL_PROFILE_GENDER,
            result_title=u'Geslacht',
            theme='q14',
            has_no_preference=False,
        )
        qsq14 = QuestionSetQuestion.objects.create(
                question=q14,
                questionset=qs1,
                position=14,
        )
        print "Added basic question 14"
 
        q15 = Question.objects.create(
            title=u'U heeft nu alle vragen beantwoord. Hieronder kunt u aangeven welke vragen u extra belangrijk vindt. Het is overigens niet verplicht extra gewicht aan bepaalde vragen te geven:',
            question_type=settings.QTYPE_MODEL_PROFILE_QUESTION_WEIGHT,
            theme='q15',
            has_no_preference=False,
        )
        qsq15 = QuestionSetQuestion.objects.create(
                question=q15,
                questionset=qs1,
                position=1000,
        )
        print "Added basic question 15"