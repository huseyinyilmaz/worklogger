from django.conf.urls import patterns, url
from django.contrib import admin

from core import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'worklogger.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.LogIndexArchiveView.as_view(), name='core-index'),
    url(r'^logs/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        views.LogDayArchiveView.as_view(),
        name="logs-day"),
    url(r'^logs/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$',
        views.LogMonthArchiveView.as_view(),
        name="logs-month"),
    url(r'^logs/(?P<year>[0-9]{4})/$',
        views.LogYearArchiveView.as_view(),
        name="logs-year"),
)
