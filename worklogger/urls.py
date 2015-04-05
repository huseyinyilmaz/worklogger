"""Main urls.py file for project."""
from django.conf.urls import patterns, include, url
from django.contrib import admin

import accounts.urls
import core.urls
import logs.urls
import djangonumerics.urls

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'', include(core.urls)),
    url(r'^logs/', include(logs.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include(accounts.urls)),
    url(r'^numerics/', include(djangonumerics.urls)),
)
