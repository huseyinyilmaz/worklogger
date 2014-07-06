from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.generic.dates import DayArchiveView
from django.views.generic.dates import MonthArchiveView
from django.views.generic.dates import YearArchiveView
from django.views.generic import ListView

from core.viewutils import LoginRequiredMixin
from django.utils import timezone

from logs.forms import LogForm
from logs.forms import JobForm
from logs.models import Log
from logs.models import Job
# Create your views here.


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


class DeleteLogView(DeleteView):
    model = Log
    template_name = 'logs/generic_delete.html'

    def get_success_url(self):
        dt = self.object.start
        return reverse('logs-day',
                       kwargs={'year': dt.year,
                               'month': dt.month,
                               'day': dt.day})


class BaseLogMixin(LoginRequiredMixin):
    model = Log
    form_class = LogForm
    template_name = 'logs/generic_form.html'

    def get_context_data(self, **kwargs):
        context = super(BaseLogMixin, self).get_context_data(**kwargs)
        context['form_title'] = self.form_title
        return context

    def form_valid(self, form):
        instance = form.save()
        dt = instance.start
        # # do a redirect here
        return HttpResponseRedirect(reverse('logs-day',
                                            kwargs={'year': dt.year,
                                                    'month': dt.month,
                                                    'day': dt.day}))


class CreateLogView(BaseLogMixin, CreateView):
    # template_name = "log_form.html"
    form_title = 'Create Log'
    template_name = 'logs/generic_form.html'

    def get_initial(self):
        initial = {'user': self.request.user,
                   'start': timezone.now()}
        try:
            latest = Log.objects.latest()
            initial['job'] = latest.job
        except Log.DoesNotExist:
            pass

        return initial


class UpdateLogView(BaseLogMixin, UpdateView):
    form_title = 'Update Log'

    def get_initial(self):
        if self.object.finish:
            result = {}
        else:
            result = {'finish': timezone.now()}

        return result


class BaseJobMixin(object):
    model = Job
    form_class = JobForm
    template_name = 'logs/generic_form.html'

    def get_success_url(self):
        return reverse('logs-jobs')

    def get_context_data(self, **kwargs):
        context = super(BaseJobMixin, self).get_context_data(**kwargs)
        context['form_title'] = self.form_title
        return context


class CreateJobView(BaseJobMixin, CreateView):
    form_title = 'Create Job'

    def get_initial(self):
        return {'user': self.request.user}


class UpdateJobView(BaseJobMixin, UpdateView):
    form_title = 'Update Job'


class DeleteJobView(DeleteView):
    model = Job
    template_name = 'logs/generic_delete.html'

    def get_success_url(self):
        return reverse('logs-jobs')


class JobListView(ListView):
    def get_queryset(self):
        qs = Job.objects.filter(user=self.request.user)
        return qs
