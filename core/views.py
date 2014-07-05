from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.dates import DayArchiveView

from logs.models import Log


@login_required
def index(request):
    return render(request, 'index.html', {})


class LogDayArchiveView(DayArchiveView):
    date_field = "start"
    make_object_list = True
    allow_future = True

    month_format = '%m'

    def get_queryset(self):
        return Log.objects.filter(user=self.request.user)
