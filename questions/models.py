from django.db import models
from django.utils.translation import ugettext_lazy as _


class Question(models.Model):
    """
        A question, has a simple title and a description
        The question type determines how the question is displayed
    """
    QUESTION_TYPE_MULTIPLECHOICE = 'C'
    QUESTION_TYPE_MULTIPLEANSWER = 'A'
    QUESTION_TYPE_BOOLEAN = 'B'
    QUESTION_TYPE_RATING = 'R'
    
    QUESTION_TYPE_CHOICES = (
        (QUESTION_TYPE_MULTIPLEANSWER, 'Multiple answers'),
        (QUESTION_TYPE_BOOLEAN, 'Boolean (yes/no, agree/disagree)'),
        (QUESTION_TYPE_MULTIPLECHOICE, 'Multiple choice'),
        (QUESTION_TYPE_RATING, 'Rating'),
    )
    
    title           = models.CharField(_('Title'), max_length=255)
    question_type   = models.CharField(_('Type of question'), max_length=1, choices=QUESTION_TYPE_CHOICES)
    weight          = models.PositiveIntegerField(_('Weight'), default=1,)
    theme           = models.CharField(_('Theme'), max_length=255, null=False)
    
    class Meta:
        verbose_name, verbose_name_plural = _('Question'), _('Questions')

    def get_themes(self):
        return self.objects.distinct(on_fields=('theme',))

class QuestionSet(models.Model):
    """
        A set of questions for grouping questions
        Makes reusing a set of questions easier
    """
    name        = models.CharField(_('Name'), max_length=255)
    question    = models.ManyToManyField(Question, verbose_name=_('Questions'))
    
    class Meta:
        verbose_name, verbose_name_plural = _('Question set'), _('Question sets')

class Answer(models.Model):
    """
        A answer to a question
        (This is one of the selectable answers, they get created with the question)
    """
    question    = models.ForeignKey(Question, verbose_name=_('Question'))
    value       = models.TextField(_('Value'))