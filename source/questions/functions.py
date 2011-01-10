from django.shortcuts import get_object_or_404
from elections.models import ElectionInstanceParty
from questions.settings import BACKOFFICE_QUESTION_TYPES

def get_question_count(election_instance_party):
    """
        Function used to get the number of questions in the question wizard
        Accepts either the election_instance_party or the primary key for one
    """
    if not isinstance(election_instance_party, ElectionInstanceParty):
        election_instance_party = get_object_or_404(ElectionInstanceParty, pk=election_instance_party)
    return election_instance_party.election_instance.questions.filter(question_type__in=BACKOFFICE_QUESTION_TYPES).count()