from django.conf.urls import patterns, url
from django.contrib import admin

from logs import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'worklogger.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        views.LogDayArchiveView.as_view(),
        name="logs-day"),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$',
        views.LogMonthArchiveView.as_view(),
        name="logs-month"),
    url(r'^(?P<year>[0-9]{4})/$',
        views.LogYearArchiveView.as_view(),
        name="logs-year"),
    url(r'^log/create/$',
        views.CreateLogView.as_view(),
        name="logs-log-create"),
    url(r'^log/update/(?P<pk>[\w-]+)$',
        views.UpdateLogView.as_view(),
        name="logs-log-update"),
    url(r'^log/delete/(?P<pk>[\w-]+)$',
        views.DeleteLogView.as_view(),
        name="logs-log-delete"),

    url(r'^job/create/$',
        views.CreateJobView.as_view(),
        name="logs-job-create"),
    url(r'^job/update/(?P<pk>[\w-]+)$',
        views.UpdateJobView.as_view(),
        name="logs-job-update"),
    url(r'^job/delete/(?P<pk>[\w-]+)$',
        views.DeleteJobView.as_view(),
        name="logs-job-delete"),

    url(r'^jobs/$',
        views.JobListView.as_view(),
        name="logs-jobs"),


)
