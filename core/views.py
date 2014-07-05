from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.dates import DayArchiveView
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.dates import MonthArchiveView
from django.views.generic.dates import YearArchiveView
from django.utils.decorators import method_decorator

from logs.models import Log


@login_required
def index(request):
    return render(request, 'index.html', {})


# https://djangosnippets.org/snippets/2442/
class LoginRequiredMixin(object):
    u"""Ensures that user must be authenticated in order to access view."""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class LogIndexArchiveView(ArchiveIndexView):
    date_field = "start"
    make_object_list = True
    allow_future = True

    def get_queryset(self):
        qs = Log.objects.filter(user=self.request.user)
        return qs


class BaseLogArchiveMixin(LoginRequiredMixin):
    date_field = "start"
    make_object_list = True
    allow_future = True

    month_format = '%m'

    def get_queryset(self):
        qs = Log.objects.filter(user=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super(BaseLogArchiveMixin, self).get_context_data(**kwargs)
        logs = context['object_list']

        context['job_summary'] = logs.summary_by_job()
        context['total_duration'] = logs.total_duration_display()
        context['date_name'] = self.date_name
        context['date_display'] = self.get_date_display(context)
        return context


class LogDayArchiveView(BaseLogArchiveMixin, DayArchiveView):
        date_name = 'Day'

        def get_date_display(self, context):
            return '{year}/{month}/{day}'.format(
                year=self.get_year(),
                month=self.get_month().zfill(2),
                day=self.get_day().zfill(2))


class LogMonthArchiveView(BaseLogArchiveMixin, MonthArchiveView):
        date_name = 'Month'

        def get_date_display(self, context):
            return '{year}/{month}'.format(year=self.get_year(),
                                           month=self.get_month().zfill(2))


class LogYearArchiveView(BaseLogArchiveMixin, YearArchiveView):
        date_name = 'Year'

        def get_date_display(self, context):
            return '{year}'.format(year=self.get_year())
