from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.functions import move_up, move_down
from django.core import serializers

from questions.settings import QUESTION_TYPE_CHOICES, QTYPE_NORM_POLONECHOICE_VISONECHOICE, QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE, QTYPE_NORM_POLBOOL_VISBOOL, QTYPE_MODEL_POLMULTICHOICE_VISONECHOICE, QTYPE_MODEL_POLONECHOICE_VISMULTICHOICE, QTYPE_MODEL_POLMULTICHOICE_VISMULTICHOICE, QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE_MIN_THREE
class Question(models.Model):
    """
        A question, has a simple title and a description
        The question type determines how the question is displayed
    """
    
    title           = models.CharField(_('Title'), max_length=255)
    frontend_title  = models.CharField(_('Frontend title'), max_length=255, default='')
    question_type   = models.CharField(_('Type of question'), max_length=10, choices=QUESTION_TYPE_CHOICES)
    weight          = models.PositiveIntegerField(_('Weight'), default=1,)
    theme           = models.CharField(_('Theme'), max_length=255, blank=True, null=False, default='')
    has_no_preference   = models.BooleanField(_('Has a no-preference option'), default=False)
    result_title    = models.TextField(_('Question'), blank=True, null=True)
    help_text       = models.TextField(_('Help Text'), blank=True, null=True)
    
    class Meta:
        verbose_name, verbose_name_plural = _('Question'), _('Questions')

    @classmethod
    def get_themes(cls):
        '''
        Gets lists of available themes.
        '''
        return cls.objects.distinct().value_list('theme', flat=True).order('theme')

    def get_frontend_title(self):
        """
            Return self.frontend_title or self.title if empty
        """
        return self.frontend_title or self.title

    def __unicode__(self):
        return self.title

class QuestionSet(models.Model):
    """
        A set of questions for grouping questions
        Makes reusing a set of questions easier
    """
    name        = models.CharField(_('Name'), max_length=255)
    questions   = models.ManyToManyField(Question, verbose_name=_('Questions'), through='QuestionSetQuestion')
    
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
                                    limit_choices_to={'question_type__in': (QTYPE_NORM_POLONECHOICE_VISONECHOICE,       # politician one choice & visitor one choice
                                                                            QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE,   # politician multiple choices & visitor multiple choices
                                                                            QTYPE_NORM_POLBOOL_VISBOOL)})               # politician true/false & visitor true/false
    value       = models.TextField(_('Value'))
    frontoffice_value = models.TextField(_('Frontoffice value'), blank=True, null=True)
    meta        = models.CharField(_('Meta'), max_length=255, blank=True, null=True, editable=False)
    
    position    = models.PositiveIntegerField(_('Position'), default=0)
    
    class Meta:
        verbose_name, verbose_name_plural = _('Answer'), _('Answers')
        ordering = ('position', 'question')
    
    def move_down(self):
        '''
        Changes the position value with next row
        '''
        return move_down(self, 'position', 1000, {'question': self.question.id})

    def move_up(self):
        '''
        Changes the position value with previous row
        '''
        return move_up(self, 'position', 1, {'question': self.question.id})

    def get_value(self):
        '''
        Returns self.value if not empty, otherwise returns question title
        '''
        if '' == self.value:
            return self.question.title
        else:
            return self.value
            
    def get_frontoffice_value(self):
        """
            Return self.frontoffice_value or self.value if empty
        """
        return self.frontoffice_value or self.value

    def __unicode__(self):
        return u'%s - %s' % (self.question.title, self.value)
