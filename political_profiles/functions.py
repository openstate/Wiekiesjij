import csv
from django.conf import settings

def get_candidates_from_csv(session):
    candidates = []

    #Get file from session and read it
    lines = csv.reader(open(settings.TMP_ROOT + '/' + session['csv_filename'] , 'rb'))
    for line in lines:
        candidate_data = dict(zip(('position', 'last_name', 'middle_name', 'first_name', 'initials', 'email', 'gender'),
            (line[0], line[1], line[2], line[3], line[4], line[5], line[6])))

        candidates.append(candidate_data)

    return candidates