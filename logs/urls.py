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
)
