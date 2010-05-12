from django.utils.translation import ugettext_lazy as _


PROFILE_QUESTION_WEIGHT_OPTIONS = (
('q2', 'Jaren politieke ervaring'),
('q3', 'Expertise'),
('q4', 'Nadruk binnen zijn/haar functie'),
('q5', 'Doelgroep'),
('q6', 'Bezuinigingen'),
('q7', 'Jaren woonachtig in de gemeente'),
('q8_groningen', 'Woonwijk'),
('q8_den haag', 'Woonwijk'),
('q8_haaren', 'Woonwijk'),
('q8_enschede', 'Woonwijk'),
('q8_amsterdam', 'Woonwijk'),
('q8_amsterdam centrum', 'Woonwijk'),
('q8_ten boer', 'Woonwijk'),
('q8_bellingwedde', 'Woonwijk'),
('q8_baarn', 'Woonwijk'),
('q8_amersfoort', 'Woonwijk'),
('q12', 'Bezigheden dagelijks leven'),
('q10', 'Opleiding'),
('q11', 'Geloofsgemeenschap'),
('q9', 'Hobby'),
('q13', 'Leeftijd'),
('q14', 'Man of Vrouw'),
('q1_he', 'Megastallen'),
('q2_he', 'Woonruimtes voor jongeren'),
('q3_he', 'Gemeentelijke herindeling'),
('q4_he', 'Optimale gemeentelijke dienstverlening'),
('q5_he', 'Financiering bedrijven en burger initiatieven'),
)


QTYPE_NORM_POLONECHOICE_VISONECHOICE = 'C'
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

)
# Question types that will return multiple answers
MULTIPLE_ANSWER_TYPES = (QTYPE_MODEL_POLITICAL_EXPERIENCE_TYPE, QTYPE_MODEL_WORK_EXPERIENCE_TYPE, QTYPE_MODEL_PROFILE_RELIGION, QTYPE_MODEL_PARTY, QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE, QTYPE_MODEL_POLONECHOICE_VISMULTICHOICE, QTYPE_MODEL_POLMULTICHOICE_VISMULTICHOICE)
# Question types to show to the candidate
BACKOFFICE_QUESTION_TYPES = (QTYPE_MODEL_POLITICAL_EXPERIENCE_TYPE, QTYPE_MODEL_WORK_EXPERIENCE_TYPE, QTYPE_NORM_POLONECHOICE_VISONECHOICE_RANGE, QTYPE_NORM_POLONECHOICE_VISONECHOICE, QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE, QTYPE_NORM_POLBOOL_VISBOOL)
# Question types to show to the visitor
FRONTOFFICE_QUESTION_TYPES= (QTYPE_MODEL_PROFILE_QUESTION_WEIGHT, QTYPE_NORM_POLONECHOICE_VISONECHOICE_RANGE, QTYPE_MODEL_POLITICAL_EXPERIENCE_YEARS, QTYPE_MODEL_EDUCATION_LEVEL, QTYPE_MODEL_PROFILE_RELIGION, QTYPE_MODEL_PROFILE_AGE, QTYPE_MODEL_PROFILE_GENDER, QTYPE_MODEL_PARTY, QTYPE_NORM_POLMULTICHOICE_VISMULTICHOICE, QTYPE_NORM_POLONECHOICE_VISONECHOICE, QTYPE_NORM_POLBOOL_VISBOOL, QTYPE_MODEL_POLMULTICHOICE_VISONECHOICE, QTYPE_MODEL_POLONECHOICE_VISMULTICHOICE, QTYPE_MODEL_POLMULTICHOICE_VISMULTICHOICE)



