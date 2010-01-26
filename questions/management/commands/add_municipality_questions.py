# -*- coding: utf-8 -*-

from django.core.management import BaseCommand

from elections.models import ElectionInstance, ElectionInstanceQuestion
from elections.settings import ELECTION_EVENT_ID
from questions import settings
from questions.models import Question, Answer

class Command(BaseCommand):
    help = 'Adds municipality specific questions'
    
    def handle(self, *args, **options):
        title = u"Ik woon in:"
        frontend_title = u"Mijn ideale kandidaat woont in:"
        
        
        items = {
            'amersfoort': [
                        u'Bergkwartier-Bosgebied',
                        u'Binnenstad',
                        u'Hoogland-Hoogland West',
                        u'Kattenbroek',
                        u'Kruiskamp-Koppel',
                        u'Liendert-Rustenburg',
                        u'Nieuwland',
                        u'Randenbroek-Schuilenburg',
                        u'Schothorst',
                        u'Soesterkwartier',
                        u'Vathorst-Hooglanderveen',
                        u'Vermeer- en Leusderkwartier',
                        u'Zielhorst',
                    ],
            'baarn': [
                        u'Centrum',
                        u'Eemdal-Noord',
                        u'Noordoostwijk',
                        u'Noordwestwijk',
                        u'Zuidwestwijk',
                        u'Zuidwijk',
                        u'Zuidoostwijk',
                        u'Buitengenied-West',
                        u'Buitengebied-Oost',
                    ],
            'bellingwedde': [
                                u'Bellingwolde/Rhederbrug/De Lethe/Den Ham',
                                u'Blijham/Morige/Zandstroom/Lutjeloo',
                                u'Klein Ulsda/Koude Hoek',
                                u'Oudeschans',
                                u'Tjabbestreek/Hoorn/Westeind',
                                u'Veelerveen/Rhederveld',
                                u'Vriescheloo',
                                u'Wedde/Wedderheide/Hoornderveen/Wedderveer',
                            ],
            'ten boer': [
                            u'Ten Boer',
                            u'Woltersum',
                            u'Ten Post',
                            u'Garmerwolde',
                            u'Sint Annen',
                            u'Winneweer',
                            u'Wittewierum',
                            u'Thesinge',
                        ],
                        
            'amsterdam centrum': [
                                    u'Nieuwmarktbuurt',
                                    u'Jordaan',
                                    u'Kadijken',
                                    u'Oostelijke Eilanden',
                                    u'Y-oever',
                                    u'Grachtengordel',
                                    u'Wallen',
                                    u'Stadshart',
                                    u'Czaar Peterbuurt',
                                ],
            'amsterdam': [
                            u'Centrum',
                            u'Noord',
                            u'West',
                            u'Nieuw-West',
                            u'Zuid',
                            u'Oost',
                            u'Zuidoost',
                        ],
            'enschede': [
                            u'Stadsdeel Centrum (o.a. Centrum, Het Zeggelt, Lasonder, De Bothoven)',
                            u'Stadsdeel Noord (o.a. Lonneker, Deppenbroek, Bolhaar, Mekkelholt, Roombeek)',
                            u'Stadsdeel Oost (o.a. Wooldrik, Velve-Lindenhof, De Eschmarke, ’t Ribbelt, Stokhorst, Dolphia, ’t Hogeland, Glanerbrug)',
                            u'Stadsdeel Zuid (Wesselerbrink, Helmerhoek, Stroinkslanden)',
                            u'Stadsdeel West (Boswinkel, Ruwenbos, Twekkelerveld, Pathmos, Stadsveld, ’t Zwering, ’t Havengebied, De Marssteden, Boekelo, Usselo, Twekkelo)',
                        ],
            'haaren': [
                            u'Biezenmortel',
                            u'Esch',
                            u'Haaren',
                            u'Helvoirt',
                      ],
            'den haag': [
                            u'Centrum',
                            u'Escamp',
                            u'Haagse Hout',
                            u'Laak',
                            u'Leidschenveen-Ypenburg',
                            u'Loosduinen',
                            u'Scheveningen',
                            u'Segbroek',
                        ],
            'groningen': [
                            u'Binnenstad',
                            u'Oosterpoortwijk',
                            u'Oranjewijk/ Hortusbuurt',
                            u'Gruno/ Stadsparkwijk/Laanhuizen/Zeeheldenwijk',
                            u'Oosterparkwijk',
                            u'Korrewegwijk/ De Hoogte',
                            u'Rivierenbuurt/Herewegbuurt',
                            u'Paddepoel/Vinkhuizen',
                            u'Selwerd/ Vinkhuizen/ Paddepoel/ Dorkwerd',
                            u'Ruischerbrug/Noorddijk/Lewenborg',
                            u'Beijum /Noorderhoogebrug/ De Hunze',
                            u'Oosterhoogebrug/ Ulgersmaborg',
                            u'De Held/Gravenburg',
                            u'De Wijert/ Helpman/Corpus den Hoorn/Klein Martijn/Coendersborg',
                            u'De Linie/Europapark',
                            u'Hoornse Meer/ Piccardthof/ Ter Borch',
                            u'Schildersbuurt/Kostverloren',
                            u'Hoogkerk/De Buitenhof',
                            u'Reitdiep/Heemwerd',
                            u'Engelbert-Meerdorpen',
                        ],
        }
        
        
        linkes = []
        for name, answers in items.iteritems():
            
            if not Question.objects.filter(theme='q8_%s' % name.replace(' ', '_')):
               
                #try link it to the propper electioninstance
                ei = None
                try:
                    if name == 'amsterdam':
                        ei = ElectionInstance.objects.get(council__region__iexact=name, election_event__pk=ELECTION_EVENT_ID, council__level='Gemeente')
                    elif name == 'amsterdam centrum':
                        ei = ElectionInstance.objects.get(council__region__iexact='amsterdam', election_event__pk=ELECTION_EVENT_ID, council__level='Deelgemeente')
                    else:
                        ei = ElectionInstance.objects.get(council__region__iexact=name, election_event__pk=ELECTION_EVENT_ID)
                    linkes.append(name)
                except ElectionInstance.DoesNotExist:
                    ei is None
                
                if ei is not None:
                    q = Question.objects.create(
                        title=title,
                        frontend_title=frontend_title,
                        has_no_preference=True,
                        question_type=settings.QTYPE_NORM_POLONECHOICE_VISONECHOICE,
                        theme='q8_%s' % name.replace(' ', '_'),
                    )
            
                    idx = 1
                    for a_title in answers:
                        Answer.objects.create(
                            question=q,
                            value=a_title,
                            frontoffice_value=None,
                            position=idx,
                        )
                        idx += 1
                        
                    Answer.objects.create(
                        question=q,
                        value=u'Een andere gemeente',
                        frontoffice_value=None,
                        position=idx
                    )
                
                    #Link the questions
                    if ei is not None:
                        ElectionInstanceQuestion.objects.create(
                            election_instance=ei,
                            question=q,
                            position=8,
                            locked=False,
                        )
            #end if question
        #end for
        
        
        for item in items.keys():
            if not item in linkes:
                print "[X] Couldn't link the question for %s" % item
            else:
                print "[V] Did link the question for %s" % item
            
        print "Done"


    