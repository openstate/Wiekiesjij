from django import template
from django.core.urlresolvers import reverse
from django.conf import settings

from questions.models import Answer, Question, QuestionSet

from django.template import loader, Context

register = template.Library()
