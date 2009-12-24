from utils.unicode_csv import UnicodeReader
from django.conf import settings

def get_candidates_from_csv(session):
    candidates = []

    #Get file from session and read it
    file = open(settings.TMP_ROOT + '/' + session['csv_candidate_filename'] , 'rb')

    count_commas = 0 #number of commas
    count_semis  = 0 #number of semicolons

    for line in file:
        count_commas += line.count(',')
        count_semis += line.count(';')
    file.close()

    if count_semis < count_commas:
        delimiter = ','
    else:
        delimiter = ';'

    #Open file and read it with csv this time
    lines = UnicodeReader(open(settings.TMP_ROOT + '/' + session['csv_candidate_filename'] , 'rb'), delimiter=delimiter)
    for line in lines:
        candidate_data = dict(zip(('position', 'last_name', 'middle_name', 'first_name', 'initials', 'email', 'gender'),
            (line[0], line[1], line[2], line[3], line[4], line[5], line[6])))

        candidates.append(candidate_data)

    return candidates

def get_parties_from_csv(session):
    parties = []

    #Get file from session and read it
    file = open(settings.TMP_ROOT + '/' + session['csv_party_filename'] , 'rb')

    count_commas = 0 #number of commas
    count_semis  = 0 #number of semicolons

    for line in file:
        count_commas += line.count(',')
        count_semis += line.count(';')
    file.close()

    if count_semis < count_commas:
        delimiter = ','
    else:
        delimiter = ';'

    #Open file and read it with csv this time
    lines = UnicodeReader(open(settings.TMP_ROOT + '/' + session['csv_party_filename'] , 'rb'), delimiter=delimiter)
    for line in lines:
        party_data = dict(zip(('list', 'name', 'abbreviation', 'contact_last_name',
            'contact_middle_name', 'contact_first_name', 'contact_email', 'contact_gender'),
            (line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7])))

        parties.append(party_data)

    return parties