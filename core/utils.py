def second_to_str(seconds):
    seconds = int(seconds)
    minutes = seconds / 60
    seconds = seconds % 60
    if minutes >= 60:
        hours = minutes / 60
        minutes = minutes % 60
    else:
        hours = 0
    return '{hours:02}:{minutes:02}:{seconds:02}'.format(hours=hours,
                                                         minutes=minutes,
                                                         seconds=seconds)
