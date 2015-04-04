def second_to_str(seconds):
    seconds = int(seconds)
    minutes = seconds // 60
    seconds = seconds % 60
    if minutes >= 60:
        hours = minutes // 60
        minutes = minutes % 60
    else:
        hours = 0
    return '{hours:02}:{minutes:02}:{seconds:02}'.format(hours=hours,
                                                         minutes=minutes,
                                                         seconds=seconds)


def move_by_month(month, offset):
    """Get the month with given offset raletive to current month."""
    return (((month - 1) + offset) % 12) + 1
