from django.conf.urls import patterns, include, url
from django.contrib import admin

import accounts.urls
import core.urls
import logs.urls

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'worklogger.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'', include(core.urls)),
    url(r'^logs/', include(logs.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include(accounts.urls)),

    url('', include('social.apps.django_app.urls', namespace='social')),
)
