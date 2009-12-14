from django.utils.translation import ugettext_lazy as _

QUESTION_TYPE_MULTIPLECHOICE = 'C'
QUESTION_TYPE_MULTIPLEANSWER = 'A'
QUESTION_TYPE_BOOLEAN = 'B'
QUESTION_TYPE_RATING = 'R'

QUESTION_TYPE_CHOICES = (
    (QUESTION_TYPE_MULTIPLEANSWER, _('Multiple answers')),
    (QUESTION_TYPE_BOOLEAN, _('Boolean (yes/no, agree/disagree)')),
    (QUESTION_TYPE_MULTIPLECHOICE, _('Multiple choice')),
    (QUESTION_TYPE_RATING, _('Rating')),
)