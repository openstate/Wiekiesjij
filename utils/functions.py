import sys
import random

def move_down(instance, field, limit, kwargs={}):
    '''
    Changes the position of the current item with position of the next one.
    Returns changed posotion of the current element on success or boolean False on failure.
    @return int

    Example of usage:
        def my_move_down(self):
            return move_down(self, 'position', length)
    '''
    value = getattr(instance, field, '')
    if not value:
        return False
        #raise Exception
    if value >= limit:
        return False

    kwargs.update({field + '__gt': value})

    try:
        next = instance.__class__.objects.filter(**kwargs).order_by(field)[0]
    except IndexError:
        next = None
    if not next or getattr(next, field) > value + 1:
        setattr(instance, field, value + 1)
        instance.save()
        return getattr(instance, field)
    else:
        tmp_pos = random.randint(10000, sys.maxint) #Small hack to prevent DB errors. 10.000 is pretty save
        current_position = getattr(instance, field)
        next_position = getattr(next, field)
        
        setattr(next, field, tmp_pos) #Move next to tmp_pos
        next.save()
        setattr(instance, field, next_position) #Move instance to it's new position
        instance.save()
        setattr(next, field, current_position) #Move next to instance's old position
        next.save()
        return getattr(instance, field)

def move_up(instance, field, limit, kwargs={}):
    '''
    Changes the position of the current item with position of the previous one.
    Returns changed posotion of the current element on success or boolean False on failure.
    @return int
    '''
    value = getattr(instance, field, '')
    if not value:
        return False
        #raise Exception
    if value <= limit:
        return False

    kwargs.update({field + '__lt': value})

    try:
        previous = instance.__class__.objects.filter(**kwargs).order_by('-' + field)[0]
    except IndexError:
        previous = None
    if not previous or getattr(previous, field) < value - 1:
        setattr(instance, field, value - 1)
        instance.save()
        return getattr(instance, field)
    else:
        tmp_pos = random.randint(10000, sys.maxint) #Small hack to prevent DB errors. 10.000 is pretty save
        current_position = getattr(instance, field)
        previous_position = getattr(previous, field)


        setattr(previous, field, tmp_pos) #Move previous to tmp_pos
        previous.save()
        setattr(instance, field, previous_position) #Move instance to it's new position
        instance.save()
        setattr(previous, field, current_position) #Move previous to instance's old position
        previous.save()

    return getattr(instance, field)


def list_unique_order_preserving(seq, idfun=None):
    """Takes a list and returns a list with no duplicate objects in the same
    order as it was recieved"""
    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result