# -*- coding: utf-8 -*-

from django.core.management import BaseCommand

from elections.models import ElectionInstance, ElectionInstanceQuestion 

from questions.models import QuestionSetQuestion

class Command(BaseCommand):
    help = 'Links the BasicSet1 to the election instances without questions and gives haaren the extra questions'
    
    def handle(self, *args, **options):

        for question in ElectionInstanceQuestion.objects.all():
            print question.position
            if question.position == 1:
                question.question.result_title = 'Uw partijvoorkeur'
            if question.position == 2:
                question.question.result_title = 'Aantal jaren ervaring als volksvertegenwoordiger'
            if question.position == 3:
                question.question.result_title = 'Kennis van politieke thema\'s (Politieke expertise)'
            if question.position == 4:
                question.question.result_title = 'Nadruk van de kandidaat in haar functie als gemeenteraadslid'
            if question.position == 5:
                question.question.result_title = 'Doelgroep waar de kandidaat zich voor inzet'
            if question.position == 6:
                question.question.result_title = 'Bezuinigingsmaatregelen in deze economische recessie'
            if question.position == 7:
                question.question.result_title = 'Het aantal jaren dat de kandidaat in uw gemeente woont'
            if question.position == 8:
                question.question.result_title = 'De woonwijk waar de kandidaat woont'
            if question.position == 9:
                question.question.result_title = 'De dagelijkse werkzaamheden van de kandidaat'
            if question.position == 10:
                question.question.result_title = 'Afgeronde vervolgopleiding van de kandidaat'
            if question.position == 11:
                question.question.result_title = 'Geloofsgemeenschap waar de kandidaat toe behoort'
            if question.position == 12:
                question.question.result_title = 'De hobby\'s van de kandidaat'
            if question.position == 13:
                question.question.result_title = 'De leeftijd van de kandidaat'
            if question.position == 14:
                question.question.result_title = 'Het geslacht van de kandidaat (man/vrouw)'
            if question.position == 50:
                question.question.result_title = 'Megastallen in het buitengebied van Haaren'
            if question.position == 51:
                question.question.result_title = 'Bouwen van woonruimtes voor jongeren'
            if question.position == 52:
                question.question.result_title = 'Samenwerking met andere gemeenten / gemeentelijke herindeling'
            if question.position == 53:
                question.question.result_title = 'Eén loket voor optimale gemeentelijke dienstverlening'
            if question.position == 54:
                question.question.result_title = 'Financiering van plannen van bedrijven en burgers, die Haaren prettiger maken om in te leven'

            question.question.save()
 
                
                