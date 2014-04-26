from django.conf.urls import patterns, url
from django.contrib import admin

from core import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'worklogger.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.root_page, name='root_page'),
)
