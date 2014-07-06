from django.conf.urls import patterns, url
from django.contrib import admin
from accounts import views
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'worklogger.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'login/$', 'django.contrib.auth.views.login', name='accounts-login'),
    url(r'logout/$', views.logout_view, name='accounts-logout'),
)