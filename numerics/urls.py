from django.conf.urls import patterns, url

from numerics import views

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'worklogger.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.IndexView.as_view(), name='numerics-index'),
)
