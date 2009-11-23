"""
Holds validation functions
"""

def is_valid_tag(tags):
    #letters, numbers, -
    if not re.match('[A-Za-z0-9-,]{3,}$', tags):
        return False
    return True

def is_valid_email(email):
    if len(email) > 7:
        if re.match("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+\.[a-zA-Z]{2,6}$", email) != None:
            return True
    return False

def is_valid_phonenumber(phone):
    if len(phone) > 10:
        if re.match('[0-9 -]{9,}$', phone) != None: #hope
            return True
    return False

def is_valid_groupname(groupname):
    #letters, numbers, _,- and + only
    return re.match('[_A-Za-z0-9-]{3,}$', groupname)

def is_valid_zipcode(zipcode):
    return re.match('^[1-9]{1}[0-9]{3}\s?[A-Z]{2}$', zipcode)
