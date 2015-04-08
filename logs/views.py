"""View implementations for log app."""

from django.contrib.auth.models import User
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
from core.utils import second_to_str
from django.utils import timezone

from logs.forms import LogForm
from logs.forms import JobForm
from logs.models import Log
from logs.models import Job

from djangonumerics.api import register
from djangonumerics import LabelResponse
from djangonumerics import NumberResponse
# Create your views here.


class BaseLogArchiveMixin(LoginRequiredMixin):

    """Base for all archive views."""

    date_field = "start"
    make_object_list = True
    allow_future = True

    month_format = '%m'

    def get_queryset(self):
        """Filter all logs by user."""
        qs = Log.objects.filter(user=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        """Add summary data for current queryset."""
        context = super(BaseLogArchiveMixin, self).get_context_data(**kwargs)
        logs = context['object_list']
        context['job_summary'] = logs.summary_by_job()
        context['total_duration'] = logs.total_duration_display()
        context['date_name'] = self.date_name
        context['date_display'] = self.get_date_display(context)
        return context


class LogDayArchiveView(BaseLogArchiveMixin, DayArchiveView):

    """Day view."""

    date_name = 'Day'

    def get_date_display(self, context):
        """Return current display for current day."""
        return '{year}/{month}/{day}'.format(
            year=self.get_year(),
            month=self.get_month().zfill(2),
            day=self.get_day().zfill(2))


class LogMonthArchiveView(BaseLogArchiveMixin, MonthArchiveView):

    """Month view."""

    date_name = 'Month'

    def get_date_display(self, context):
        """Display for current month."""
        return '{year}/{month}'.format(year=self.get_year(),
                                       month=self.get_month().zfill(2))


class LogYearArchiveView(BaseLogArchiveMixin, YearArchiveView):

    """Year view."""

    date_name = 'Year'

    def get_date_display(self, context):
        """Dispaly for current year."""
        return '{year}'.format(year=self.get_year())


class DeleteLogView(DeleteView):

    """Delete log view."""

    model = Log
    template_name = 'logs/generic_delete.html'

    def get_success_url(self):
        """After delete is complete return to latest log day view."""
        dt = Log.objects.latest().start
        return reverse('logs-day',
                       kwargs={'year': dt.year,
                               'month': dt.month,
                               'day': dt.day})


class BaseLogMixin(LoginRequiredMixin):

    """Base Mixin for update/create log views."""

    model = Log
    form_class = LogForm
    template_name = 'logs/generic_form.html'

    def get_context_data(self, **kwargs):
        """Add Form title to context."""
        context = super(BaseLogMixin, self).get_context_data(**kwargs)
        context['form_title'] = self.form_title
        return context

    def form_valid(self, form):
        """If form is valid, save and return the date for current object."""
        instance = form.save()
        dt = instance.start
        # # do a redirect here
        return HttpResponseRedirect(reverse('logs-day',
                                            kwargs={'year': dt.year,
                                                    'month': dt.month,
                                                    'day': dt.day}))


class CreateLogView(BaseLogMixin, CreateView):

    """Create log view."""

    # template_name = "log_form.html"
    form_title = 'Create Log'
    template_name = 'logs/generic_form.html'

    def get_initial(self):
        """Set current user and set starts date to now."""
        initial = {'user': self.request.user,
                   'start': timezone.now()}
        try:
            latest = Log.objects.latest()
            initial['job'] = latest.job
        except Log.DoesNotExist:
            pass

        return initial


class UpdateLogView(BaseLogMixin, UpdateView):

    """Update log view."""

    form_title = 'Update Log'

    def get_initial(self):
        """Set finish date to now."""
        if self.object.finish:
            result = {}
        else:
            result = {'finish': timezone.now()}

        return result


class BaseJobMixin(object):

    """Base for create and update job views."""

    model = Job
    form_class = JobForm
    template_name = 'logs/generic_form.html'

    def get_success_url(self):
        """After operation is complete, return jobs list page."""
        return reverse('logs-jobs')

    def get_context_data(self, **kwargs):
        """Add form title to context."""
        context = super(BaseJobMixin, self).get_context_data(**kwargs)
        context['form_title'] = self.form_title
        return context


class CreateJobView(BaseJobMixin, CreateView):

    """Create Job view."""

    form_title = 'Create Job'

    def get_initial(self):
        """Add current user to initial data."""
        return {'user': self.request.user}


class UpdateJobView(BaseJobMixin, UpdateView):

    """Update Job view."""

    form_title = 'Update Job'


class DeleteJobView(LoginRequiredMixin, DeleteView):

    """Delete Job view."""

    model = Job
    template_name = 'logs/generic_delete.html'

    def get_success_url(self):
        """After operation is complete, return to jobs list view."""
        return reverse('logs-jobs')


class JobListView(LoginRequiredMixin, ListView):

    """Jobs list view."""

    def get_queryset(self):
        """Filter jobs by current user."""
        qs = Job.objects.filter(user=self.request.user)
        return qs

#####################
# NUMERIC ENDPOINTS #
#####################


def last_day_hours(user):
    """Total hours for latest day.

    Currently active job is also included to calculation.
    """
    try:
        latest_log = user.log_set.latest()
    except Log.DoesNotExist:
        return LabelResponse('No Data Available')
    latest_day = user.log_set.by_day(latest_log.start)
    duration = latest_day.total_duration()
    # check if there is any unfinished logs
    logs = user.log_set.filter(finish__isnull=True)[:1]
    # if there is an unfinished log and unfinished log has the same date
    # is latest_log add unfinished log to result
    if logs and logs[0].start.date() == latest_log.start.date():
        duration += logs[0].get_duration()
    latest_day_display = str(timezone.localtime(latest_log.start).date())
    return LabelResponse(second_to_str(duration),
                         latest_day_display)


def previous_month_hours(user):
    """Total hours for latest month.

    Currently active job is also included to calculation.
    """
    months = user.log_set.datetimes('start', 'month', order='DESC')[:2]
    if len(months) == 2:
        month = months[1]
    else:
        return LabelResponse('No Data Available')

    previous_month = user.log_set.by_month(month)
    duration = previous_month.total_duration()
    previous_log = previous_month[0]
    # check if there is any unfinished logs
    logs = user.log_set.filter(finish__isnull=True)[:1]
    # if there is an unfinished log and unfinished log has the same date
    # is latest_log add unfinished log to result
    if logs and logs[0].start.date() == previous_log.start.date():
        duration += logs[0].get_duration()

    postfix = timezone.localtime(previous_log.start).strftime('%B %Y')
    return LabelResponse(second_to_str(duration), postfix)


def last_month_hours(user):
    """Total hours for latest month.

    Currently active job is also included to calculation.
    """
    latest_log = user.log_set.latest()
    latest_month = user.log_set.by_month(latest_log.start)
    duration = latest_month.total_duration()

    # check if there is any unfinished logs
    logs = user.log_set.filter(finish__isnull=True)[:1]
    # if there is an unfinished log and unfinished log has the same date
    # is latest_log add unfinished log to result
    if logs and logs[0].start.date() == latest_log.start.date():
        duration += logs[0].get_duration()
    postfix = timezone.localtime(latest_log.start).strftime('%B %Y')
    response = LabelResponse(second_to_str(duration), postfix)
    return response


def current_job(user):
    """Currntly active job information.

    Info includes name of the job and total time spent for this job.
    If there is no active log, 'Not Working' will be returned.
    """
    logs = user.log_set.filter(finish__isnull=True)[:1]
    if logs:
        log = logs[0]
        result = LabelResponse(log.job.name,
                               log.get_duration_display())
    else:
        log = user.log_set.latest()
        result = LabelResponse('Not Working',
                               str(timezone.localtime(log.start).date()))

    return result


def total_users(user):
    """Return total number of users."""
    user_count = User.objects.filter(active=True).count()

    return NumberResponse('Total number of users', user_count)


register('total-users', total_users)
register('last-day-hours', last_day_hours)
register('last-month-hours', last_month_hours)
register('previous-month-hours', previous_month_hours,
         cache_timeout=60*60)  # one hour
register('current-job', current_job)
