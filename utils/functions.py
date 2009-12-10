def move_down(instance, field):
    '''
    Changes the position of the current item with position of the previous one.
    Returns changed posotion of the current element on success or boolean False on failure.
    @return int

    Example of usage:
        def my_move_down(self):
            return move_down(self, 'position')
    '''
    value = getattr(instance, field, '')
    if not value:
        raise Exception

    kwargs = {field + '__lt': value}

    previous = instance.__class__.objects.filter(**kwargs).order_by('-' + field)[:1]
    if not previous:
        return False
    else:
        previous = previous[0]
        current_position = getattr(instance, field)
        setattr(instance, field, getattr(previous, field))
        setattr(previous, field, current_position)
        instance.save()
        previous.save()
        return instance.position

def move_up(instance, field):
    '''
    Changes the position of the current item with position of the next one.
    Returns changed posotion of the current element on success or boolean False on failure.
    @return int
    '''
    value = getattr(instance, field, '')
    if not value:
        raise Exception

    kwargs = {field + '__gt': value}
    
    next = instance.__class__.objects.filter(**kwargs).order_by(field)[:1]
    if not next:
        return False
    else:
        next = next[0]
        current_position = getattr(instance, field)
        setattr(instance, field, getattr(next, field))
        setattr(next, field, current_position)
        instance.save()
        next.save()
        return instance.position