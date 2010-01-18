from django.utils.translation import ugettext_lazy as _

#QUESTION_TYPE_MULTIPLECHOICE = 'C'
#QUESTION_TYPE_MULTIPLEANSWER = 'A'
#QUESTION_TYPE_BOOLEAN = 'B'
#QUESTION_TYPE_RATING = 'R'
#QUESTION_TYPE_MODEL = 'M'
#
#QUESTION_TYPE_CHOICES = (
#    (QUESTION_TYPE_MULTIPLEANSWER, _('Multiple answers')),
#    (QUESTION_TYPE_BOOLEAN, _('Boolean (yes/no, agree/disagree)')),
#    (QUESTION_TYPE_MULTIPLECHOICE, _('Multiple choice')),
#    (QUESTION_TYPE_MODEL, _('Model')),
#)
#
## Question types to show to the candidate
#BACKOFFICE_QUESTION_TYPES = (QUESTION_TYPE_MULTIPLECHOICE, QUESTION_TYPE_MULTIPLEANSWER, QUESTION_TYPE_BOOLEAN)
## Question types to show to the visitor
#FRONTOFFICE_QUESTION_TYPES= (QUESTION_TYPE_MODEL, QUESTION_TYPE_MULTIPLECHOICE, QUESTION_TYPE_MULTIPLEANSWER, QUESTION_TYPE_BOOLEAN)


QTYPE_NORM_POLMULTICHOICE_VISONECHOICE = 'C'
QTYPE_NORM_POLONECHOICE_VISMULTICHOICE = 'A'
QTYPE_NORM_POLONECHOICE_VISONECHOICE = 'H'
QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE = 'I'
QTYPE_NORM_POLBOOL_VISBOOL = 'B'
QTYPE_MODEL_POLMULTICHOICE_VISONECHOICE = 'D'
QTYPE_MODEL_POLONECHOICE_VISMULTICHOICE = 'E'
QTYPE_SYSTEM_POLMULTICHOICE_VISONECHOICE = 'F'
QTYPE_SYSTEM_POLONECHOICE_VISMULTICHOICE = 'G'
QTYPE_MODEL_PARTY = 'Z'
QTYPE_MODEL_WORK_EXPERIENCE_YEARS = 'Y'
QTYPE_MODEL_EDUCATION_LEVEL = 'X'
QTYPE_MODEL_PROFILE_RELIGION = 'W'
QTYPE_MODEL_PROFILE_HOBBY ='V'
QTYPE_MODEL_PROFILE_AGE ='U'
QTYPE_MODEL_PROFILE_GENDER ='T'


QUESTION_TYPE_CHOICES = (
(QTYPE_MODEL_PROFILE_AGE, _('Politicians Age, Visitor Selects age range')),
(QTYPE_MODEL_PROFILE_GENDER, _('Politicians gender, Visitor Selects gender')),
(QTYPE_MODEL_PROFILE_HOBBY, _('Politicians hobby, Visitor Selects hobbies')),
(QTYPE_MODEL_PROFILE_RELIGION, _('Politicians religon, Visitor Selects religons')),
(QTYPE_MODEL_EDUCATION_LEVEL, _('Politicians education level, Visitor Selects range')),
(QTYPE_MODEL_WORK_EXPERIENCE_YEARS, _('Politicians work experience years, Visitor Selects range')),
(QTYPE_MODEL_PARTY, _('Politicians work experience, Visitor Selects multiple from model')),
(QTYPE_NORM_POLMULTICHOICE_VISONECHOICE, _('Politician Chooses Multiple, Visitor Selects One')),
(QTYPE_NORM_POLONECHOICE_VISMULTICHOICE, _('Politician Chooses One, Visitor Selects Many')),
(QTYPE_NORM_POLONECHOICE_VISONECHOICE, _('Politician Chooses One, Visitor Selects One')),
(QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE, _('Politician Chooses Multiple, Visitor Selects Multiple')),
(QTYPE_NORM_POLBOOL_VISBOOL, _('Both Politician and Visitor selects (yes/no, agree/disagree)')),
(QTYPE_MODEL_POLMULTICHOICE_VISONECHOICE, _('Politcian profile detais are used, Visitor Selects One')),
(QTYPE_MODEL_POLONECHOICE_VISMULTICHOICE, _('Politcian profile detais are used, Visitor Selects Multiple')),
(QTYPE_SYSTEM_POLMULTICHOICE_VISONECHOICE, _('Politcian profile information is used to make statistics, Visitor Selects One')),
(QTYPE_SYSTEM_POLONECHOICE_VISMULTICHOICE, _('Politcian profile information is used to make statistics, Visitor Selects Multiple')),


)

# Question types to show to the candidate
BACKOFFICE_QUESTION_TYPES = (QTYPE_NORM_POLMULTICHOICE_VISONECHOICE, QTYPE_NORM_POLONECHOICE_VISMULTICHOICE, QTYPE_NORM_POLONECHOICE_VISONECHOICE, QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE, QTYPE_NORM_POLBOOL_VISBOOL)
# Question types to show to the visitor
FRONTOFFICE_QUESTION_TYPES= (QTYPE_MODEL_WORK_EXPERIENCE_YEARS, QTYPE_MODEL_EDUCATION_LEVEL, QTYPE_MODEL_PROFILE_RELIGION, QTYPE_MODEL_PROFILE_HOBBY, QTYPE_MODEL_PROFILE_AGE, QTYPE_MODEL_PROFILE_GENDER, QTYPE_MODEL_PARTY, QTYPE_NORM_POLMULTICHOICE_VISONECHOICE, QTYPE_NORM_POLONECHOICE_VISMULTICHOICE, QTYPE_NORM_POLONECHOICE_VISONECHOICE, QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE, QTYPE_NORM_POLBOOL_VISBOOL, QTYPE_MODEL_POLMULTICHOICE_VISONECHOICE, QTYPE_MODEL_POLONECHOICE_VISMULTICHOICE, QTYPE_SYSTEM_POLMULTICHOICE_VISONECHOICE)