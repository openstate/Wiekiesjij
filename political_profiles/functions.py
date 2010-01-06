from utils.unicode_csv import UnicodeReader
from django.conf import settings
from django.forms.fields import email_re
from datetime import timedelta, datetime, date
import monthdelta
from dateutil import relativedelta
from utils.functions import list_unique_order_preserving

def cal_political_experience_days(sender, instance, **kwargs):
    all_months = []
    #Get all politican political experience instances
    for experience in instance.politician.political.all():
        # when saving a new instance it saves the object first to get and idThis makes sure that the code is only 
        # done on instances that are fully complete.
        if experience.startdate:
            # check if they are currently getting experience or if they have an end date
            if experience.enddate:
                end = experience.enddate
            else:
                end = date.today()
            #Find out how many months that this period represents
            months = monthdelta.monthmod(experience.startdate, end)
            # add all months in the range to a list
            for month in range(0,(months[0].months + 1)):
                all_months.append(experience.startdate + relativedelta.relativedelta(months=+month))
    # remove duplicates from list
    num_months = len(list_unique_order_preserving(all_months))
    # calculate roughly how many days this is
    instance.politician.political_experience_days = num_months * (365 / 12)
    # save politician with newly calculated number of days
    instance.politician.save()


def cal_work_experience_days(sender, instance, **kwargs):
    """ calculates the amount of days experience working - roughly"""
    all_months = []
    #Get all politican work experience instances
    for experience in instance.politician.work.all():
        # when saving a new instance it saves the object first to get and idThis makes sure that the code is only
        # done on instances that are fully complete.
        if experience.startdate:
            # check if they are currently getting experience or if they have an end date
            if experience.enddate:
                end = experience.enddate
            else:
                end = date.today()
            #Find out how many months that this period represents
            months = monthdelta.monthmod(experience.startdate, end)
            # add all months in the range to a list
            for month in range(0,(months[0].months + 1)):
                all_months.append(experience.startdate + relativedelta.relativedelta(months=+month))
    # remove duplicates from list
    num_months = len(list_unique_order_preserving(all_months))
    # calculate roughly how many days this is
    instance.politician.work_experience_days  = num_months * (365 / 12)
    # save politician with newly calculated number of days
    instance.politician.save()


def get_candidates_from_csv(session, skip_positions=[]):
    candidates = {}

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
            
        # extra validation
        if not email_re.match(candidate_data['email']):
            continue
        try:
            position = int(candidate_data['position'])
        except ValueError:
            continue
        if candidate_data['gender'] not in ['Female', 'Male']:
            continue
        
        if not int(candidate_data['position']) in skip_positions:
            candidates.update({candidate_data['position']: candidate_data})

    return candidates

def get_parties_from_csv(session, skip_lists=[]):
    parties = {}

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
            
        # extra validation
        if not email_re.match(party_data['contact_email']):
            continue
        try:
            pos = int(party_data['list'])
        except ValueError:
            continue
        if party_data['contact_gender'] not in ['Female', 'Male']:
            continue
                
        if not int(party_data['list']) in skip_lists:
            parties.update({party_data['list']: party_data})

    return parties