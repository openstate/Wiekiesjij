
# -*- coding: utf-8 -*-


from django.core.management import BaseCommand

from questions import settings
from questions.models import QuestionSet, QuestionSetQuestion, Question, Answer

class Command(BaseCommand):
    help = 'Adds questions'

    def handle(self, *args, **options):
	print "ACHTUNG: Script out of sync with production db at 20120903"
	exit(1)
        try:
            landelijk_set = QuestionSet.objects.get(name='TEST Landelijk Set')
            return
        except QuestionSet.DoesNotExist:
            landelijk_set = QuestionSet.objects.create(name='TEST Landelijk Set')

        q1 = Question.objects.create(
            title=u'Welke partijen maken kans op uw stem?',
            question_type=settings.QTYPE_MODEL_PARTY,
            result_title=u'Partij',
            theme='q1',
            has_no_preference=False,
        )
        QuestionSetQuestion.objects.create(
                question=q1,
                questionset=landelijk_set,
                position=1,
        )
        print "Added Landelijk question 1"

        q2 = Question.objects.create(
            title=u'De belangrijkste uitdaging(en) waarvoor Nederland staat is:',
            frontend_title=u'De belangrijkste uitdaging(en) waarvoor Nederland staat is:',
            question_type=settings.QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE,
            result_title=u'Uitdagingen voor Nederland',
            theme='q2',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q2,
                questionset=landelijk_set,
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
        print "Added Landelijk question 2"


        q3 = Question.objects.create(
            title=u'Ik leg de meeste nadruk op:',
            frontend_title=u'Mijn ideale kandidaat moet de meeste nadruk leggen op: (meer antwoorden mogelijk)',
            question_type=settings.QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE,
            result_title=u'Nadruk',
            theme='q3',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q3,
                questionset=landelijk_set,
                position=3,
        )
        q3_answers = [
            "Het land in gaan om te kijken wat er leeft bij de bevolking",
            "Zelf goede ideeën verzinnen en deze naar voren brengen in de Kamer",
            "Het controleren van het beleid en de uitgaven van de regering",
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
        print "Added Landelijk question 3"


        q4 = Question.objects.create(
            title=u'Mijn expertise ligt in:',
            frontend_title=u'Waar ligt de expertise van uw kandidaat?: (meer antwoorden mogelijk)',
            question_type=settings.QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE,
            result_title=u'Expertise',
            theme='q4',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q4,
                questionset=landelijk_set,
                position=4,
        )
        q4_answers = [
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
        for position, answer in enumerate(q4_answers):
            Answer.objects.create(
                question=q4,
                value=answer,
                frontoffice_value=None,
                position=position+1,
                )
        print "Added Landelijk question 4"

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
                questionset=landelijk_set,
                position=5,
        )
        print "Added Landelijk question 5"


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
                questionset=landelijk_set,
                position=6,
        )
        print "Added Landelijk question 6"


        q7 = Question.objects.create(
            title=u'Ik zet mij vooral in voor:',
            frontend_title=u'Voor welke groep of groepen zet uw kandidaat zich extra in?',
            question_type=settings.QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE,
            result_title=u'Doelgroep(en) van de kandidaat',
            theme='q7',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q7,
                questionset=landelijk_set,
                position=7,
        )
        q7_answers = [
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
        for position, answer in enumerate(q7_answers):
            Answer.objects.create(
                question=q7,
                value=answer,
                frontoffice_value=None,
                position=position+1,
                )
        print "Added Landelijk question 7"

        q8 = Question.objects.create(
            title=u'Ik haal mijn motivatie voornamelijk uit:',
            frontend_title=u'Waaruit haalt uw ideale kandidaat zijn of haar motivatie?',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE,
            result_title=u'Motivatie',
            theme='q8',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q8,
                questionset=landelijk_set,
                position=8,
        )
        q8_answers = [
            ("Een betere wereld", "Een betere wereld"),
            ("Een sterker en beter Nederland", "Een sterker en beter Nederland"),
            ("Het versterken van zijn/haar regio", "Het versterken van mijn regio"),
            ("Een krachtige partij", "Een krachtige partij"),
            ("Persoonlijke ontplooiing", "Persoonlijke ontplooiing"),
            ("Anders", "Anders"),

        ]
        for position, (fo_answer, answer) in enumerate(q8_answers):
            Answer.objects.create(
                question=q8,
                value=answer,
                frontoffice_value=fo_answer,
                position=position+1,
                )
        print "Added Landelijk question 8"

        q9 = Question.objects.create(
            title=u'Mijn ideale kandidaat heeft de volgende vervolgopleiding afgerond:',
            question_type=settings.QTYPE_MODEL_EDUCATION_LEVEL,
            result_title=u'Opleiding',
            theme='q9',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q9,
                questionset=landelijk_set,
                position=9,
        )
        Answer.objects.create(
            question=q9,
            value=u'Geen vervolgopleiding',
            meta=u'ALL_OTHERS',
            frontoffice_value=u'Geen vervolgopleiding',
            position=1,
        )
        Answer.objects.create(
            question=q9,
            value=u'Middelbaar Beroepsonderwijs',
            meta=u'MBO',
            frontoffice_value=u'Middelbaar Beroepsonderwijs',
            position=2,
        )
        Answer.objects.create(
            question=q9,
            value=u'Hoger Beroepsonderwijs',
            meta=u'HBO',
            frontoffice_value=u'Hoger Beroepsonderwijs',
            position=3,
        )
        Answer.objects.create(
            question=q9,
            value=u'Wetenschappelijk Onderwijs',
            meta=u'Universitair',
            frontoffice_value=u'Wetenschappelijk Onderwijs',
            position=4,
        )
        print "Added Landelijk question 9"

        q10 = Question.objects.create(
            title=u'Op welke manier speelt religie bij uw werk in de politiek?',
            frontend_title=u'Op welke manier speelt religie een rol bij uw ideale kandidaat?',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE,
            result_title=u'Religie',
            theme='q10',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q10,
                questionset=landelijk_set,
                position=10,
        )
        q10_answers = [
            ("Religie is leidend voor zijn/haar politiek handelen ", "Religie is leidend voor mijn politiek handelen "),
            ("Religie is een inspiratiebron voor zijn/haar politiek handelen", "Religie is een inspiratiebron voor mijn politiek handelen"),
            ("Religie speelt voor zijn/haar politiek handelen geen rol", "Religie speelt voor mijn politiek handelen geen rol"),
        ]
        for position, (fo_answer, answer) in enumerate(q10_answers):
            Answer.objects.create(
                question=q10,
                value=answer,
                frontoffice_value=fo_answer,
                position=position+1,
                )
        print "Added Landelijk question 10"

        q11 = Question.objects.create(
            title=u'In welke leeftijdsgroep zit uw ideale kandidaat?',
            question_type=settings.QTYPE_MODEL_PROFILE_AGE,
            result_title=u'Leeftijd',
            theme='q11',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q11,
                questionset=landelijk_set,
                position=11,
        )
        Answer.objects.create(
            question=q11,
            value=u'30 jaar of jonger',
            meta=u':30',
            frontoffice_value=u'30 jaar of jonger',
            position=1,
        )
        Answer.objects.create(
            question=q11,
            value=u'tussen de 31 en de 55',
            meta=u'31:55',
            frontoffice_value=u'tussen de 31 en de 55',
            position=2,
        )
        Answer.objects.create(
            question=q11,
            value=u'Ouder dan 55 jaar',
            meta=u'55:',
            frontoffice_value=u'Ouder dan 55 jaar',
            position=3,
        )
        print "Added Landelijk question 11"

        q12 = Question.objects.create(
            title=u'Wilt u een voorkeur uitspreken voor een man of vrouw?',
            question_type=settings.QTYPE_MODEL_PROFILE_GENDER,
            result_title=u'Geslacht',
            theme='q12',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q12,
                questionset=landelijk_set,
                position=12,
        )
        print "Added Landelijk question 12"


        q13 = Question.objects.create(
            title=u'Heeft u meegeschreven aan uw partijprogramma?',
            frontend_title=u'Heeft uw kandidaat meegeschreven aan het partijprogramma?',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE,
            result_title=u'Meegeschreven partijprogramma',
            theme='q13',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q13,
                questionset=landelijk_set,
                position=13,
        )
        q13_answers = [
            ("Ja", "Ja"),
            ("Nee", "Nee"),
        ]
        for position, (fo_answer, answer) in enumerate(q13_answers):
            Answer.objects.create(
                question=q13,
                value=answer,
                frontoffice_value=fo_answer,
                position=position+1,
                )
        print "Added Landelijk question 13"

        q14 = Question.objects.create(
            title=u'Moet de 2e Kamer worden verkleind van 150 naar 100 zetels?',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE,
            result_title=u'Omvang 2e Kamer',
            theme='q14',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q14,
                questionset=landelijk_set,
                position=14,
        )
        q14_answers = [
            ("Ja", "Ja"),
            ("Nee", "Nee"),
        ]
        for position, (fo_answer, answer) in enumerate(q14_answers):
            Answer.objects.create(
                question=q14,
                value=answer,
                frontoffice_value=fo_answer,
                position=position+1,
                )
        print "Added Landelijk question 14"

        q15 = Question.objects.create(
            title=u'Zou de rol van de Eerste Kamer moeten veranderen?',
            frontend_title=u'',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE,
            result_title=u'Rol Eerste Kamer',
            theme='q15',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q15,
                questionset=landelijk_set,
                position=15,
        )
        q15_answers = [
            ("Nee", "Nee"),
            ("Ja, afschaffen", "Ja, afschaffen"),
            ("Ja, meer invloed", "Ja, meer invloed"),
        ]
        for position, (fo_answer, answer) in enumerate(q15_answers):
            Answer.objects.create(
                question=q15,
                value=answer,
                frontoffice_value=fo_answer,
                position=position+1,
                )
        print "Added Landelijk question 15"

        q16 = Question.objects.create(
            title=u'Hoe actief bent u op social media?',
            frontend_title=u'Hoe actief is uw kandidaat op social media?',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE,
            result_title=u'Social media',
            theme='q16',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q16,
                questionset=landelijk_set,
                position=16,
        )
        q16_answers = [
            ("Niet actief", "Niet actief"),
            ("Matig actief", "Matig actief"),
            ("Redelijk actief", "Redelijk actief"),
            ("Vrij actief", "Vrij actief"),
            ("Zeer actief", "Zeer actief"),
        ]
        for position, (fo_answer, answer) in enumerate(q16_answers):
            Answer.objects.create(
                question=q16,
                value=answer,
                frontoffice_value=fo_answer,
                position=position+1,
                )
        print "Added Landelijk question 16"

        q17 = Question.objects.create(
            title=u'Nederland zou zich in haar buitenlands beleid vooral moeten richten op:',
            frontend_title=u'',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE,
            result_title=u'Buitenlands beleid',
            theme='q17',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q17,
                questionset=landelijk_set,
                position=17,
        )
        q17_answers = [
            ("de VS", "de VS"),
            ("onze buurlanden", "onze buurlanden"),
            ("Europa", "Europa"),
            ("Azië", "Azië"),
            ("de BRIC-landen", "de BRIC-landen"),
        ]
        for position, (fo_answer, answer) in enumerate(q17_answers):
            Answer.objects.create(
                question=q17,
                value=answer,
                frontoffice_value=fo_answer,
                position=position+1,
                )
        print "Added Landelijk question 17"

        q18 = Question.objects.create(
            title=u'Hoeveel talen spreekt u?',
            frontend_title=u'Hoeveel talen spreekt uw kandidaat?',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE,
            result_title=u'Talen',
            theme='q18',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q18,
                questionset=landelijk_set,
                position=18,
        )
        q18_answers = [
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5 of meer", "5 of meer"),
        ]
        for position, (fo_answer, answer) in enumerate(q18_answers):
            Answer.objects.create(
                question=q18,
                value=answer,
                frontoffice_value=fo_answer,
                position=position+1,
                )
        print "Added Landelijk question 18"

        q19 = Question.objects.create(
            title=u'Nieuwspoort:',
            frontend_title=u'Nieuwspoort',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE,
            result_title=u'Nieuwspoort',
            theme='q19',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q19,
                questionset=landelijk_set,
                position=19,
        )
        q19_answers = [
            ("Afschaffen", "Afschaffen"),
            ("Nuttige ontmoetingsplaats", "Nuttige ontmoetingsplaats"),
            ("Prima, maar zelf zal ik er niet vaak te vinden zijn.", "Prima, maar zelf zal ik er niet vaak te vinden zijn."),
        ]
        for position, (fo_answer, answer) in enumerate(q19_answers):
            Answer.objects.create(
                question=q19,
                value=answer,
                frontoffice_value=fo_answer,
                position=position+1,
                )
        print "Added Landelijk question 19"

        q20 = Question.objects.create(
            title=u'Voelt u zich vooral:',
            frontend_title=u'Voelt uw kandidaat zich vooral:',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE,
            result_title=u'Regiobewoner of wereldburger',
            theme='q20',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q20,
                questionset=landelijk_set,
                position=20,
        )
        q20_answers = [
            ("Limburger/Fries/Amsterdammer/etc", "Limburger/Fries/Amsterdammer/etc"),
            ("Nederlander", "Nederlander"),
            ("Europeaan", "Europeaan"),
            ("Wereldburger", "Wereldburger"),
        ]
        for position, (fo_answer, answer) in enumerate(q20_answers):
            Answer.objects.create(
                question=q20,
                value=answer,
                frontoffice_value=fo_answer,
                position=position+1,
                )
        print "Added Landelijk question 20"

        q21 = Question.objects.create(
            title=u'Er zou een kiesdrempel moeten worden ingevoerd, voor partijen:',
            frontend_title=u'',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE,
            result_title=u'Kiesdrempel',
            theme='q21',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q21,
                questionset=landelijk_set,
                position=21,
        )
        q21_answers = [
            ("Kleiner dan 5 zetels", "Kleiner dan 5 zetels"),
            ("Kleiner dan 3 zetels", "Kleiner dan 3 zetels"),
            ("Kleiner dan 1-2 zetels", "Kleiner dan 1-2 zetels"),
            ("Er moet geen drempel ingevoerd worden", "Er moet geen drempel ingevoerd worden"),
        ]
        for position, (fo_answer, answer) in enumerate(q21_answers):
            Answer.objects.create(
                question=q21,
                value=answer,
                frontoffice_value=fo_answer,
                position=position+1,
                )
        print "Added Landelijk question 21"

        q22 = Question.objects.create(
            title=u'De komende kabinetsperiode gaan de huizenprijzen:',
            frontend_title=u'',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE,
            result_title=u'Huizenprijzen',
            theme='q22',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q22,
                questionset=landelijk_set,
                position=22,
        )
        q22_answers = [
            ("Weer omhoog", "Weer omhoog"),
            ("Verder omlaag", "Verder omlaag"),
            ("Blijven gelijk", "Blijven gelijk"),
        ]
        for position, (fo_answer, answer) in enumerate(q22_answers):
            Answer.objects.create(
                question=q22,
                value=answer,
                frontoffice_value=fo_answer,
                position=position+1,
                )
        print "Added Landelijk question 22"

        q23 = Question.objects.create(
            title=u'Wie is primair verantwoordelijk voor de economische crisis?',
            frontend_title=u'',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE,
            result_title=u'Verantwoordelijk crisis',
            theme='q23',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q23,
                questionset=landelijk_set,
                position=23,
        )
        q23_answers = [
            ("de banken", "de banken"),
            ("enkele (Zuid-)Europese landen", "enkele (Zuid-)Europese landen"),
            ("de Europese Unie", "de Europese Unie"),
            ("de VS", "de VS"),
            ("allemaal", "allemaal"),
        ]
        for position, (fo_answer, answer) in enumerate(q23_answers):
            Answer.objects.create(
                question=q23,
                value=answer,
                frontoffice_value=fo_answer,
                position=position+1,
                )
        print "Added Landelijk question 23"

        q24 = Question.objects.create(
            title=u'Met betrekking tot de omvang van de overheid:',
            frontend_title=u'',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE,
            result_title=u'Omvang overheid',
            theme='q24',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q24,
                questionset=landelijk_set,
                position=24,
        )
        q24_answers = [
            ("Er is ruimte voor groei.", "Er is ruimte voor groei."),
            ("Er is ruimte voor krimp.", "Er is ruimte voor krimp."),
            ("Krimp noch groei is op dit moment prioriteit.", "Krimp noch groei is op dit moment prioriteit."),
        ]
        for position, (fo_answer, answer) in enumerate(q24_answers):
            Answer.objects.create(
                question=q24,
                value=answer,
                frontoffice_value=fo_answer,
                position=position+1,
                )
        print "Added Landelijk question 24"

        q25 = Question.objects.create(
            title=u'Hebt u een hypotheek?',
            frontend_title=u'Heeft uw kandidaat een hypotheek?',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE,
            result_title=u'Hypotheek',
            theme='q25',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q25,
                questionset=landelijk_set,
                position=25,
        )
        q25_answers = [
            ("Ja", "Ja"),
            ("Nee", "Nee"),
        ]
        for position, (fo_answer, answer) in enumerate(q25_answers):
            Answer.objects.create(
                question=q25,
                value=answer,
                frontoffice_value=fo_answer,
                position=position+1,
                )
        print "Added Landelijk question 25"

        q26 = Question.objects.create(
            title=u'U heeft nu alle vragen beantwoord. Hieronder kunt u aangeven welke vragen u extra belangrijk vindt. Het is overigens niet verplicht extra gewicht aan bepaalde vragen te geven:',
            question_type=settings.QTYPE_MODEL_PROFILE_QUESTION_WEIGHT,
            theme='q26',
            has_no_preference=False,
        )
        QuestionSetQuestion.objects.create(
                question=q26,
                questionset=landelijk_set,
                position=1000,
        )
        print "Added Landelijk question 26"

        q27 = Question.objects.create(
            title=u'In mijn regeringscoalitie zitten de volgende partijen (kies minimaal 3 partijen):',
            frontend_title=u'',
            question_type=settings.QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE_MIN_THREE,
            result_title=u'Coalitie',
            theme='q27',
            has_no_preference=True
        )
        QuestionSetQuestion.objects.create(
                question=q27,
                questionset=landelijk_set,
                position=27,
        )
        q27_answers = [
            "Volkspartij voor Vrijheid en Democratie (VVD)",
            "Partij van de Arbeid (PvdA)",
            "Partij voor de Vrijheid (PVV)",
            "Christen Democratisch Appèl (CDA)",
            "Socialistische Partij (SP)",
            "Democraten 66 (D66)",
            "GroenLinks",
            "ChristenUnie",
            "Staatkundig Gereformeerde Partij (SGP)",
            "Partij voor de Dieren",
            "Piratenpartij",
            "Partij voor Mens en Spirit (MenS)",
            "Nederland Lokaal",
            "Libertarische Partij (LP)",
            "Democratisch Politiek Keerpunt (DPK)",
            "50Plus",
            "Liberaal Democratische Partij (LibDem)",
            "Anti Europa Partij",
            "Soeverein Onafhankelijke Pioniers Nederland (SOPN)",
        ]
        for position, answer in enumerate(q27_answers):
            Answer.objects.create(
                question=q27,
                value=answer,
                frontoffice_value=None,
                position=position+1,
                )
        print "Added Landelijk question 27"

        q28 = Question.objects.create(
            title=u'Wie ziet u het liefst als premier?',
            frontend_title=u'',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE_SECRET,
            result_title=u'Premier',
            theme='q28',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q28,
                questionset=landelijk_set,
                position=28,
        )
        q28_answers = [
            "Mark Rutte",
            "Emile Roemer",
            "Diederik Samsom",
            "Alexander Pechtold",
            "Sybrand Van Haersma Buma",
            "Geert Wilders",
        ]
        for position, answer in enumerate(q28_answers):
            Answer.objects.create(
                question=q28,
                value=answer,
                frontoffice_value=None,
                position=position+1,
                )
        print "Added Landelijk question 28"

        q29 = Question.objects.create(
            title=u'Indien uw eigen partij niet de premier zal mogen leveren, wie komt daar dan wat u betreft voor in aanmerking?',
            frontend_title=u'',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE_SECRET,
            result_title=u'Premier andere partij',
            theme='q29',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q29,
                questionset=landelijk_set,
                position=29,
        )
        q29_answers = [
            "Mark Rutte",
            "Emile Roemer",
            "Diederik Samsom",
            "Alexander Pechtold",
            "Sybrand Van Haersma Buma",
            "Geert Wilders",
        ]
        for position, answer in enumerate(q29_answers):
            Answer.objects.create(
                question=q29,
                value=answer,
                frontoffice_value=None,
                position=position+1,
                )
        print "Added Landelijk question 29"

        q30 = Question.objects.create(
            title=u'Waar zou u uzelf plaatsen binnen het politieke spectrum van uw partij?',
            frontend_title=u'',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE_SECRET,
            result_title=u'NONE',
            theme='q30',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q30,
                questionset=landelijk_set,
                position=30,
        )
        q30_answers = [
            ("Iets linkser", "Iets linkser"),
            ("Iets rechtser", "Iets rechtser"),
            ("Precies in het midden", "Precies in het midden"),
        ]
        for position, (fo_answer, answer) in enumerate(q30_answers):
            Answer.objects.create(
                question=q30,
                value=answer,
                frontoffice_value=fo_answer,
                position=position+1,
                )
        print "Added Landelijk question 30"

        q31 = Question.objects.create(
            title=u'Gaat u een voorkeurs- cq. persoonlijke campagne voeren?',
            frontend_title=u'',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE_SECRET,
            result_title=u'NONE',
            theme='q31',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q31,
                questionset=landelijk_set,
                position=31,
        )
        q31_answers = [
            ("Ja", "Ja"),
            ("Nee", "Nee"),
        ]
        for position, (fo_answer, answer) in enumerate(q31_answers):
            Answer.objects.create(
                question=q31,
                value=answer,
                frontoffice_value=fo_answer,
                position=position+1,
                )
        print "Added Landelijk question 31"

        q32 = Question.objects.create(
            title=u'Wat doet u zelf met uw voorkeurstem? Ik stem:',
            frontend_title=u'',
            question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE_SECRET,
            result_title=u'NONE',
            theme='q32',
            has_no_preference=True,
        )
        QuestionSetQuestion.objects.create(
                question=q32,
                questionset=landelijk_set,
                position=32,
        )
        q32_answers = [
            ("Op mezelf", "Op mezelf"),
            ("Op de lijsttrekker", "Op de lijsttrekker"),
            ("Op een geestverwant in de partij", "Op een geestverwant in de partij"),
        ]
        for position, (fo_answer, answer) in enumerate(q32_answers):
            Answer.objects.create(
                question=q32,
                value=answer,
                frontoffice_value=fo_answer,
                position=position+1,
                )
        print "Added Landelijk question 32"
