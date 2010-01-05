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
        current_position = getattr(instance, field)
        next_position = getattr(next, field)
        setattr(instance, field, next_position)
        setattr(next, field, current_position)
        instance.save()
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
        current_position = getattr(instance, field)
        previous_position = getattr(previous, field)
        setattr(instance, field, previous_position)
        setattr(previous, field, current_position)
        instance.save()
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