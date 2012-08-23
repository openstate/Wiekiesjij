from django.utils.translation import ugettext_lazy as _


PROFILE_QUESTION_WEIGHT_OPTIONS = (
    ('q2', 'Belangrijkste streven kandidaat'),
    ('q3', 'Nadruk kandidaat'),
    ('q4', 'Expertise kandidaat'),
    ('q5', 'Werkervaring kandidaat'),
    ('q6', 'Politieke ervaring kandidaat'),
    ('q7', 'Doelgroep(en) van de kandidaat'),
    ('q8', 'Regio van de kandidaat'),
    ('q9', 'Motivatie van de kandidaat'),
    ('q10', 'Opleiding kandidaat'),
    ('q11', 'Religieuze motivatie kandidaat'),
    ('q12', 'Leeftijd kandidaat'),
    ('q13', 'Geslacht kandidaat'),
)


QTYPE_NORM_POLONECHOICE_VISONECHOICE = 'C'
QTYPE_NORM_POLONECHOICE_VISONECHOICE_SECRET = 'CS'
QTYPE_NORM_POLONECHOICE_VISONECHOICE_RANGE = 'G'
QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE = 'A'
QTYPE_NORM_POLBOOL_VISBOOL = 'B'
QTYPE_MODEL_POLMULTICHOICE_VISONECHOICE = 'D'
QTYPE_MODEL_POLONECHOICE_VISMULTICHOICE = 'E'
QTYPE_MODEL_POLMULTICHOICE_VISMULTICHOICE = 'F'
QTYPE_MODEL_PARTY = 'Z'
QTYPE_MODEL_POLITICAL_EXPERIENCE_YEARS = 'Y'
QTYPE_MODEL_POLITICAL_EXPERIENCE_TYPE = 'I'
QTYPE_MODEL_WORK_EXPERIENCE_TYPE = 'J'
QTYPE_MODEL_EDUCATION_LEVEL = 'X'
QTYPE_MODEL_PROFILE_RELIGION = 'W'
QTYPE_MODEL_PROFILE_AGE ='U'
QTYPE_MODEL_PROFILE_GENDER ='T'
QTYPE_MODEL_PROFILE_QUESTION_WEIGHT = 'H'
QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE_MIN_THREE_SECRET = 'KS'

QUESTION_TYPE_CHOICES = (
(QTYPE_MODEL_POLITICAL_EXPERIENCE_TYPE, _('Politician political experience, vistor selects a sector')),
(QTYPE_MODEL_WORK_EXPERIENCE_TYPE, _('Politician work experience, vistor selects a sector')),
(QTYPE_NORM_POLONECHOICE_VISONECHOICE_RANGE, _('Politicians chooses one, Visitor selects one but calculation based on meta')),
(QTYPE_MODEL_PROFILE_AGE, _('Politicians Age, Visitor Selects age range')),
(QTYPE_MODEL_PROFILE_GENDER, _('Politicians gender, Visitor Selects gender')),
(QTYPE_MODEL_PROFILE_RELIGION, _('Politicians religon, Visitor Selects religons')),
(QTYPE_MODEL_EDUCATION_LEVEL, _('Politicians education level, Visitor Selects range')),
(QTYPE_MODEL_PROFILE_QUESTION_WEIGHT, _('Politicians Question Themes, Visitor Selects Theme')),
(QTYPE_MODEL_POLITICAL_EXPERIENCE_YEARS, _('Politicians political experience years, Visitor Selects range')),
(QTYPE_MODEL_PARTY, _('Politicians work experience, Visitor Selects multiple from model')),
(QTYPE_NORM_POLONECHOICE_VISONECHOICE, _('Politician Chooses One, Visitor Selects One')),
(QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE, _('Politician Chooses Multiple, Visitor Selects Multiple')),
(QTYPE_NORM_POLBOOL_VISBOOL, _('Both Politician and Visitor selects (yes/no, agree/disagree)')),
(QTYPE_MODEL_POLMULTICHOICE_VISONECHOICE, _('Politcian profile detais are used, Visitor Selects One')),
(QTYPE_MODEL_POLONECHOICE_VISMULTICHOICE, _('Politcian profile detais are used, Visitor Selects Multiple')),
(QTYPE_MODEL_POLMULTICHOICE_VISMULTICHOICE, _('Politcian model information has multiple correct answers, Visitor Selects Miltiple')),
(QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE_MIN_THREE_SECRET, _('Both Politiciian and Visitor selects at least 3 items of a list')),
(QTYPE_NORM_POLONECHOICE_VISONECHOICE_SECRET, _('Politician Chooses One, Secret question')),
)
# Question types that will return multiple answers
MULTIPLE_ANSWER_TYPES = (QTYPE_MODEL_POLITICAL_EXPERIENCE_TYPE,
                         QTYPE_MODEL_WORK_EXPERIENCE_TYPE,
                         QTYPE_MODEL_PROFILE_RELIGION, QTYPE_MODEL_PARTY,
                         QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE,
                         QTYPE_MODEL_POLONECHOICE_VISMULTICHOICE,
                         QTYPE_MODEL_POLMULTICHOICE_VISMULTICHOICE,
                         QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE_MIN_THREE_SECRET)
# Question types to show to the candidate
BACKOFFICE_QUESTION_TYPES = (QTYPE_MODEL_POLMULTICHOICE_VISMULTICHOICE,
                             QTYPE_NORM_POLONECHOICE_VISONECHOICE_RANGE,
                             QTYPE_NORM_POLONECHOICE_VISONECHOICE,
                             QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE,
                             QTYPE_NORM_POLBOOL_VISBOOL,
                             QTYPE_NORM_POLONECHOICE_VISONECHOICE_SECRET,
                             QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE_MIN_THREE_SECRET)
# Question types to show to the visitor
FRONTOFFICE_QUESTION_TYPES= (QTYPE_MODEL_POLMULTICHOICE_VISMULTICHOICE,
                             QTYPE_MODEL_POLITICAL_EXPERIENCE_TYPE,
                             QTYPE_MODEL_WORK_EXPERIENCE_TYPE,
                             QTYPE_MODEL_PROFILE_QUESTION_WEIGHT,
                             QTYPE_NORM_POLONECHOICE_VISONECHOICE_RANGE,
                             QTYPE_MODEL_POLITICAL_EXPERIENCE_YEARS,
                             QTYPE_MODEL_EDUCATION_LEVEL,
                             QTYPE_MODEL_PROFILE_RELIGION,
                             QTYPE_MODEL_PROFILE_AGE,
                             QTYPE_MODEL_PROFILE_GENDER, QTYPE_MODEL_PARTY,
                             QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE,
                             QTYPE_NORM_POLONECHOICE_VISONECHOICE,
                             QTYPE_NORM_POLBOOL_VISBOOL,
                             QTYPE_MODEL_POLMULTICHOICE_VISONECHOICE,
                             QTYPE_MODEL_POLONECHOICE_VISMULTICHOICE,
                             QTYPE_MODEL_POLMULTICHOICE_VISMULTICHOICE,
                            )



