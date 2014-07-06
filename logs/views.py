from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic.dates import DayArchiveView
from django.views.generic.dates import MonthArchiveView
from django.views.generic.dates import YearArchiveView
from core.viewutils import LoginRequiredMixin


from logs.forms import LogForm
from logs.models import Log
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


class CreateLogView(CreateView):
    template_name = "log_form.html"
    form = LogForm

    def get_context_data(self, **kwargs):
        context = super(CreateLogView, self).get_context_data(**kwargs)
        return context

    def get_form_kwargs(self):
        kwargs = super(CreateLogView, self).get_form_kwargs()
        return kwargs

    def form_valid(self, form):
        instance = form.save()
        # do a redirect here
        return render(self.request,
                      self.complete_template_name,
                      {'pm': self.landing_page, 'lead': instance})
