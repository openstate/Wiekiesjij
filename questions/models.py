from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.functions import move_up, move_down

from questions.settings import QUESTION_TYPE_CHOICES, QUESTION_TYPE_MULTIPLECHOICE, QUESTION_TYPE_MULTIPLEANSWER, QUESTION_TYPE_BOOLEAN, QUESTION_TYPE_RATING


class Question(models.Model):
    """
        A question, has a simple title and a description
        The question type determines how the question is displayed
    """
    
    title           = models.CharField(_('Title'), max_length=255)
    frontend_title  = models.CharField(_('Frontend title'), max_length=255, default='')
    question_type   = models.CharField(_('Type of question'), max_length=1, choices=QUESTION_TYPE_CHOICES)
    weight          = models.PositiveIntegerField(_('Weight'), default=1,)
    theme           = models.CharField(_('Theme'), max_length=255, blank=True, null=False, default='')
    has_no_preference   = models.BooleanField(_('Has a no-preference option'), default=False)

    class Meta:
        verbose_name, verbose_name_plural = _('Question'), _('Questions')

    @classmethod
    def get_themes(cls):
        '''
        Gets lists of available themes.
        '''
        return cls.objects.distinct().value_list('theme', flat=True).order('theme')

    def __unicode__(self):
        return self.title

class QuestionSet(models.Model):
    """
        A set of questions for grouping questions
        Makes reusing a set of questions easier
    """
    name        = models.CharField(_('Name'), max_length=255)
    question    = models.ManyToManyField(Question, verbose_name=_('Questions'), through='QuestionSetQuestion')

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name, verbose_name_plural = _('Question set'), _('Question sets')
        
        
    def __unicode__(self):
        return self.name
        
class QuestionSetQuestion(models.Model):
    """
        Links a question and a set together using a position
    """
    question    = models.ForeignKey(Question, verbose_name=_('Question'))
    questionset = models.ForeignKey(QuestionSet, verbose_name=_('Question set'))
    
    position    = models.PositiveIntegerField(_('Position'), default=0)
    
    class Meta:
        verbose_name, verbose_name_plural = _('Question set question'), _('Question set questions')
        ordering = ('position', 'questionset')
        
    def move_down(self):
        '''
        Changes the position value with next row
        '''
        return move_down(self, 'position', 1000, {'questionset': self.questionset.id})

    def move_up(self):
        '''
        Changes the position value with previous row
        '''
        return move_up(self, 'position', 1, {'questionset': self.questionset.id})
    

class Answer(models.Model):
    """
        A answer to a question
        (This is one of the selectable answers, they get created with the question)
    """
    question    = models.ForeignKey(Question, verbose_name=_('Question'), related_name='answers',
                                    limit_choices_to={'question_type__in': (QUESTION_TYPE_MULTIPLECHOICE,
                                                                            QUESTION_TYPE_MULTIPLEANSWER,
                                                                            QUESTION_TYPE_BOOLEAN)})
    value       = models.TextField(_('Value'))

    def get_value(self):
        '''
        Returns self.value if not empty, otherwise returns question title
        '''
        if '' == self.value:
            return self.question.title
        else:
            return self.value

    def __unicode__(self):
        return self.question.title + ' - ' + self.value
