import datetime

from django.core.management import BaseCommand

from questions import settings
from questions.models import Question, Answer
 
class Command(BaseCommand):
    help = 'Adds questions'
    
    def handle(self, *args, **options):
        q1 = Question.objects.create(
            title='Welke krant leest u?',
            frontend_title='Welke krant moet uw politicus lezen?',
            has_no_preference=True,
            question_type=settings.QUESTION_TYPE_MULTIPLEANSWER,
            theme='media',
        )
        Answer.objects.create(
            question=q1,
            value='NRC',
        )
        Answer.objects.create(
            question=q1,
            value='Sp!ts',
        )
        Answer.objects.create(
            question=q1,
            value='Straatkrant',
        )
        Answer.objects.create(
            question=q1,
            value='Telegraaf',
        )
        Answer.objects.create(
            question=q1,
            value='AD',
        )
        print "Added MULTIPLEANSWER question"

        q2 = Question.objects.create(
            title='Met welk vervoermiddel gaat u naar uw werk?',
            frontend_title='Welk vervoermiddel moet uw politicus gebruiken?',
            has_no_preference=True,
            question_type=settings.QUESTION_TYPE_MULTIPLECHOICE,
            theme='transpotation',
        )
        Answer.objects.create(
            question=q2,
            value='Auto',
        )
        Answer.objects.create(
            question=q2,
            value='Trein',
        )
        Answer.objects.create(
            question=q2,
            value='Bus',
        )
        Answer.objects.create(
            question=q2,
            value='Fiets',
        )
        Answer.objects.create(
            question=q2,
            value='Metro',
        )
        Answer.objects.create(
            question=q2,
            value='Tram',
        )
        Answer.objects.create(
            question=q2,
            value='Benenwagen',
        )
        print "Added MULTIPLECHOICE question"
        
        q3 = Question.objects.create(
            title='Vind u dit systeem handig?',
            frontend_title='moet de politicus dit systeem handig vinden?',
            has_no_preference=True,
            question_type=settings.QUESTION_TYPE_BOOLEAN,
            theme='system',
        )
        Answer.objects.create(
            question=q3,
            value='Ja',
        )
        Answer.objects.create(
            question=q3,
            value='Nee',
        )
        print "Added BOOLEAN question"