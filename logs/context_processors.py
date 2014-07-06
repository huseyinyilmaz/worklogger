from logs.models import Log


def running_logs(request):
    user = request.user
    running_logs = Log.objects.filter(user=user, finish__isnull=True)
    if running_logs:
        result = {'has_current_log': True,
                  'current_log': running_logs[0]}
    else:
        result = {'has_current_job': False,
                  'current_job': None}

    return result
