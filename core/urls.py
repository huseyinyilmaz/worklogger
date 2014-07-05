from django.conf.urls import patterns, url
from django.contrib import admin

from core import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'worklogger.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index, name='core-index'),
    url(r'^logs/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        views.LogDayArchiveView.as_view(),
        name="log_day"),
)
